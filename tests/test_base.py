"""
Tests for the base certificate manager module.
"""

import pytest
import subprocess
from unittest.mock import patch, MagicMock
from certhook.base import BaseCertManager

def test_base_cert_manager_init():
    """Test initialization of BaseCertManager."""
    cert_name = "test-cert"
    manager = BaseCertManager(cert_name)
    assert manager.cert_name == cert_name
    assert manager.verbose is False
    assert manager.cmds == []

def test_base_cert_manager_init_verbose():
    """Test initialization of BaseCertManager with verbose flag."""
    cert_name = "test-cert"
    manager = BaseCertManager(cert_name, verbose=True)
    assert manager.verbose is True

def test_cert_cmds_default_behavior():
    """Test that cert_cmds passes by default and initializes empty command list."""
    manager = BaseCertManager("test-cert")
    manager.cert_cmds()
    assert manager.cmds == []

@patch('subprocess.run')
def test_run_command(mock_run):
    """Test running a command."""
    mock_result = MagicMock()
    mock_result.stdout = b"test output"
    mock_result.stderr = b""
    mock_run.return_value = mock_result
    
    manager = BaseCertManager("test-cert")
    cmd = ["echo", "test"]
    result = manager.run(cmd)
    
    mock_run.assert_called_once_with(cmd, capture_output=True, check=True)
    assert result == mock_result

@patch('subprocess.run')
def test_run_command_verbose(mock_run):
    """Test running a command with verbose output."""
    mock_result = MagicMock()
    mock_result.stdout = b"test output\n"
    mock_result.stderr = b"test error\n"
    mock_result.args = ["echo", "test"]
    mock_run.return_value = mock_result
    
    manager = BaseCertManager("test-cert", verbose=True)
    cmd = ["echo", "test"]
    
    with patch('builtins.print') as mock_print:
        result = manager.run(cmd)
        
        # Verify all print calls were made
        mock_print.assert_any_call('command: echo test')
        mock_print.assert_any_call('stdout: test output\n')
        mock_print.assert_any_call('stderr: test error\n')

@patch('subprocess.run')
def test_call_executes_commands(mock_run):
    """Test that __call__ executes all commands in the queue."""
    class TestCertManager(BaseCertManager):
        def cert_cmds(self):
            self.cmds = [
                ["cmd1", "arg1"],
                ["cmd2", "arg2"]
            ]
    
    mock_result = MagicMock()
    mock_result.stdout = b""
    mock_result.stderr = b""
    mock_run.return_value = mock_result
    
    manager = TestCertManager("test-cert")
    manager()
    
    assert mock_run.call_count == 2
    mock_run.assert_any_call(["cmd1", "arg1"], capture_output=True, check=True)
    mock_run.assert_any_call(["cmd2", "arg2"], capture_output=True, check=True)

def test_subprocess_error_handling():
    """Test that subprocess errors are propagated."""
    manager = BaseCertManager("test-cert")
    with pytest.raises((subprocess.CalledProcessError, FileNotFoundError)):
        # Running a command that should fail
        manager.run(["nonexistent_command"])
