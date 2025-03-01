"""
Tests for the EmbyCertManager class
"""

from unittest.mock import patch, MagicMock
from certhook import EmbyCertManager


def test_init():
    """Test initialization of EmbyCertManager"""
    manager = EmbyCertManager(cert_name="example.com")
    assert manager.cert_name == "example.com"
    assert manager.verbose is False
    assert isinstance(manager.cmds, list)


def test_init_verbose():
    """Test initialization with verbose flag"""
    manager = EmbyCertManager(cert_name="example.com", verbose=True)
    assert manager.verbose is True


def test_cert_cmds():
    """Test command generation"""
    manager = EmbyCertManager(cert_name="example.com")
    expected_cmds = [
        [
            '/usr/bin/openssl', 'pkcs12', '-export',
            '-inkey', '/etc/letsencrypt/live/example.com/privkey.pem',
            '-in', '/etc/letsencrypt/live/example.com/fullchain.pem',
            '-out', '/etc/letsencrypt/live/example.com/fullchain.p12',
            '-password', 'pass:'
        ],
        ['/usr/bin/chown', 'root:ssl-certs', '/etc/letsencrypt/live/example.com/fullchain.p12'],
        ['/usr/bin/chmod', '0770', '/etc/letsencrypt/live/example.com/fullchain.p12'],
        ['/usr/sbin/service', 'emby-server', 'restart']
    ]
    assert manager.cmds == expected_cmds


@patch('subprocess.run')
def test_run_command(mock_run):
    """Test command execution"""
    manager = EmbyCertManager(cert_name="example.com")
    mock_process = MagicMock()
    mock_process.stdout = b"test output"
    mock_process.stderr = b""
    mock_run.return_value = mock_process
    
    test_cmd = ['test', 'command']
    result = manager.run(test_cmd)
    
    mock_run.assert_called_once_with(test_cmd, capture_output=True, check=True)
    assert result == mock_process


@patch('subprocess.run')
def test_run_command_verbose(mock_run):
    """Test command execution with verbose output"""
    manager = EmbyCertManager(cert_name="example.com", verbose=True)
    mock_process = MagicMock()
    mock_process.stdout = b"test output"
    mock_process.stderr = b"test error"
    mock_process.args = ['test', 'command']
    mock_run.return_value = mock_process
    
    test_cmd = ['test', 'command']
    with patch('builtins.print') as mock_print:
        result = manager.run(test_cmd)
    
    mock_run.assert_called_once_with(test_cmd, capture_output=True, check=True)
    assert result == mock_process
    mock_print.assert_any_call('command: test command')
    mock_print.assert_any_call('stdout: test output')
    mock_print.assert_any_call('stderr: test error')


@patch('certhook.emby.EmbyCertManager.run')
def test_call_executes_all_commands(mock_run):
    """Test that __call__ executes all commands"""
    manager = EmbyCertManager(cert_name="example.com")
    manager()
    
    assert mock_run.call_count == len(manager.cmds)
    for cmd in manager.cmds:
        mock_run.assert_any_call(cmd)

