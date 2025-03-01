"""
Tests for the main CLI interface.
"""
import pytest
from unittest.mock import patch, MagicMock
from certhook.main import main, APP_MANAGERS


def test_cli_required_args():
    """Test CLI fails without required arguments"""
    with pytest.raises(SystemExit):
        with patch('sys.argv', ['certhook']):
            main()


def test_cli_invalid_app():
    """Test CLI fails with invalid app"""
    with pytest.raises(SystemExit):
        with patch('sys.argv', ['certhook', 'invalid', 'example.com']):
            main()


@patch('certhook.base.subprocess.run')
def test_cli_unifi(mock_run):
    """Test CLI with unifi app"""
    # Set up mock manager class
    mock_manager_class = MagicMock()
    mock_instance = MagicMock()
    mock_manager_class.return_value = mock_instance
    mock_instance.return_value = None
    
    # Set up mock run to return success
    mock_run.return_value.returncode = 0
    
    # Patch UnifiCertManager in APP_MANAGERS
    with patch.dict(APP_MANAGERS, {'unifi': mock_manager_class}):
        test_args = ['certhook', 'unifi', 'example.com', '--verbose']
        with patch('sys.argv', test_args):
            main()
    
    mock_manager_class.assert_called_once_with(cert_name='example.com', verbose=True)
    mock_instance.assert_called_once_with()


@patch('certhook.base.subprocess.run')
def test_cli_pihole(mock_run):
    """Test CLI with pihole app"""
    # Set up mock manager class
    mock_manager_class = MagicMock()
    mock_instance = MagicMock()
    mock_manager_class.return_value = mock_instance
    mock_instance.return_value = None
    
    # Set up mock run to return success
    mock_run.return_value.returncode = 0
    
    # Patch PiHoleCertManager in APP_MANAGERS
    with patch.dict(APP_MANAGERS, {'pihole': mock_manager_class}):
        test_args = ['certhook', 'pihole', 'example.com']
        with patch('sys.argv', test_args):
            main()
    
    mock_manager_class.assert_called_once_with(cert_name='example.com', verbose=False)
    mock_instance.assert_called_once_with()


@patch('certhook.base.subprocess.run')
def test_cli_emby(mock_run):
    """Test CLI with emby app"""
    # Set up mock manager class
    mock_manager_class = MagicMock()
    mock_instance = MagicMock()
    mock_manager_class.return_value = mock_instance
    mock_instance.return_value = None
    
    # Set up mock run to return success
    mock_run.return_value.returncode = 0
    
    # Patch EmbyCertManager in APP_MANAGERS
    with patch.dict(APP_MANAGERS, {'emby': mock_manager_class}):
        test_args = ['certhook', 'emby', 'example.com']
        with patch('sys.argv', test_args):
            main()
    
    mock_manager_class.assert_called_once_with(cert_name='example.com', verbose=False)
    mock_instance.assert_called_once_with()


@patch('certhook.base.subprocess.run')
def test_cli_freepbx(mock_run):
    """Test CLI with freepbx app"""
    # Set up mock manager class
    mock_manager_class = MagicMock()
    mock_instance = MagicMock()
    mock_manager_class.return_value = mock_instance
    mock_instance.return_value = None
    
    # Set up mock run to return success
    mock_run.return_value.returncode = 0
    
    # Patch FreePBXCertManager in APP_MANAGERS
    with patch.dict(APP_MANAGERS, {'freepbx': mock_manager_class}):
        test_args = ['certhook', 'freepbx', 'example.com']
        with patch('sys.argv', test_args):
            main()
    
    mock_manager_class.assert_called_once_with(cert_name='example.com', verbose=False)
    mock_instance.assert_called_once_with()
