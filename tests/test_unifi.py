"""
Tests for the UnifiCertManager class
"""

import pytest
from unittest.mock import patch, MagicMock
from certhook import UnifiCertManager


@pytest.fixture
def cert_name():
    return "example.com"


def test_init(cert_name):
    """Test initialization of UnifiCertManager"""
    manager = UnifiCertManager(cert_name=cert_name)
    assert manager.cert_name == cert_name
    assert manager.verbose is False
    assert isinstance(manager.cmds, list)


def test_init_verbose(cert_name):
    """Test initialization with verbose flag"""
    manager = UnifiCertManager(cert_name=cert_name, verbose=True)
    assert manager.verbose is True


def test_cert_cmds(cert_name):
    """Test command generation"""
    manager = UnifiCertManager(cert_name=cert_name)
    manager.cert_cmds()
    
    # Test openssl command
    expected_cmd1 = [
        '/usr/bin/openssl', 'pkcs12', '-export',
        '-inkey', f'/etc/letsencrypt/live/{cert_name}/privkey.pem',
        '-in', f'/etc/letsencrypt/live/{cert_name}/fullchain.pem',
        '-out', f'/etc/letsencrypt/live/{cert_name}/fullchain.p12',
        '-name', 'unifi', '-password', 'pass:unifi'
    ]
    assert manager.cmds[0] == expected_cmd1

    # Test keytool command
    expected_cmd2 = [
        '/usr/bin/keytool', '-importkeystore',
        '-deststorepass', 'aircontrolenterprise',
        '-destkeypass', 'aircontrolenterprise',
        '-destkeystore', '/data/unifi/data/keystore',
        '-srckeystore', f'/etc/letsencrypt/live/{cert_name}/fullchain.p12',
        '-srcstoretype', 'PKCS12',
        '-srcstorepass', 'unifi', '-noprompt'
    ]
    assert manager.cmds[1] == expected_cmd2

    # Test service restart commands
    assert manager.cmds[2] == ['/usr/sbin/service', 'unifi-core', 'restart']
    assert manager.cmds[3] == ['/usr/sbin/service', 'unifi', 'restart']


@patch('subprocess.run')
def test_run_command(mock_run, cert_name):
    """Test command execution"""
    manager = UnifiCertManager(cert_name=cert_name)
    mock_process = MagicMock()
    mock_process.stdout = b"test output"
    mock_process.stderr = b""
    mock_run.return_value = mock_process
    
    test_cmd = ['test', 'command']
    result = manager.run(test_cmd)
    
    mock_run.assert_called_once_with(test_cmd, capture_output=True, check=True)
    assert result == mock_process


@patch('subprocess.run')
def test_run_command_verbose(mock_run, cert_name):
    """Test command execution with verbose output"""
    manager = UnifiCertManager(cert_name=cert_name, verbose=True)
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
