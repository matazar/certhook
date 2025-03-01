"""
Main CLI entry point for certhook.
"""

import argparse
import sys
from . import unifi
from . import pihole
from . import emby
from . import freepbx

APP_MANAGERS = {
    'unifi': unifi.UnifiCertManager,
    'pihole': pihole.PiHoleCertManager,
    'emby': emby.EmbyCertManager,
    'freepbx': freepbx.FreePBXCertManager
}

def main():
    """Main entry point for the certhook CLI."""
    parser = argparse.ArgumentParser(description='Certificate management tool')
    parser.add_argument('app', choices=list(APP_MANAGERS.keys()),
                      help='Application to manage certificates for')
    parser.add_argument('cert_name',
                      help='Name of the certificate (e.g., example.com)')
    parser.add_argument('--verbose', action='store_true',
                      help='Enable verbose output')

    args = parser.parse_args()

    # Get the manager class for the selected app
    manager_class = APP_MANAGERS[args.app]
    
    # Create and run the manager
    manager = manager_class(cert_name=args.cert_name, verbose=args.verbose)
    manager()

if __name__ == '__main__':
    sys.exit(main())
