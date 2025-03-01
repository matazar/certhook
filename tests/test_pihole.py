"""
Tests for the PiHoleCertManager class
"""

from unittest.mock import patch, mock_open, MagicMock
from certhook import PiHoleCertManager


def test_init():
    """Test initialization of PiHoleCertManager"""
    manager = PiHoleCertManager(cert_name="example.com")
    assert manager.cert_name == "example.com"
    assert manager.user == "pihole"
    assert manager.group == "ssl-certs"
    assert manager.verbose is False


def test_init_custom_user_group():
    """Test initialization with custom user and group"""
    manager = PiHoleCertManager(
        cert_name="example.com",
        user="custom_user",
        group="custom_group",
        verbose=True
    )
    assert manager.user == "custom_user"
    assert manager.group == "custom_group"
    assert manager.verbose is True


@patch('shutil.copy2')
@patch('builtins.open', new_callable=mock_open, read_data='private key content')
def test_create_combined_cert(mock_file, mock_copy):
    """Test certificate combination process"""
    manager = PiHoleCertManager(cert_name="example.com")
    manager.create_combined_cert()
    
    # Check if fullchain.pem was copied
    mock_copy.assert_called_once_with(
        '/etc/letsencrypt/live/example.com/fullchain.pem',
        '/etc/letsencrypt/live/example.com/pihole.pem'
    )
    
    # Check if privkey.pem was appended
    mock_file.assert_any_call('/etc/letsencrypt/live/example.com/privkey.pem', 'r')
    mock_file.assert_any_call('/etc/letsencrypt/live/example.com/pihole.pem', 'a')


def test_pihole_cert_property():
    """Test pihole_cert property"""
    manager = PiHoleCertManager(cert_name="example.com")
    expected_path = '/etc/letsencrypt/live/example.com/pihole.pem'
    assert manager.pihole_cert == expected_path


@patch('os.chmod')
@patch('subprocess.run')
def test_set_permissions(mock_run, mock_chmod):
    """Test permission setting"""
    manager = PiHoleCertManager(cert_name="example.com")
    manager.set_permissions()
    
    mock_run.assert_called_once_with(
        ['chown', 'pihole:ssl-certs', '/etc/letsencrypt/live/example.com/pihole.pem'],
        capture_output=True,
        check=True
    )
    mock_chmod.assert_called_once_with(
        '/etc/letsencrypt/live/example.com/pihole.pem',
        0o640
    )


@patch('subprocess.run')
def test_restart_service(mock_run):
    """Test service restart"""
    manager = PiHoleCertManager(cert_name="example.com")
    manager.restart_service()
    
    mock_run.assert_called_once_with(
        ['systemctl', 'restart', 'pihole-FTL'],
        capture_output=True,
        check=True
    )


@patch('certhook.pihole.PiHoleCertManager.restart_service')
@patch('certhook.pihole.PiHoleCertManager.set_permissions')
@patch('certhook.pihole.PiHoleCertManager.create_combined_cert')
def test_call_executes_all_steps(mock_create, mock_perms, mock_restart):
    """Test that __call__ executes all required steps"""
    manager = PiHoleCertManager(cert_name="example.com")
    manager()
    
    mock_create.assert_called_once()
    mock_perms.assert_called_once()
    mock_restart.assert_called_once()
