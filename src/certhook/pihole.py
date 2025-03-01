"""
Module for converting a Let's Encrypt certificates for use with Pi-hole v6+ web panel.
"""

import os
import shutil
from .base import BaseCertManager


class PiHoleCertManager(BaseCertManager):
    """
    Creates and manages SSL certificates for Pi-hole FTL service
    """
    def __init__(self, cert_name: str, user: str = 'pihole', group: str = 'ssl-certs', verbose: bool = False):
        """
        Initialize the Pi-hole certificate manager

        Args:
            cert_name: Name of the certificate (domain name)
            user: User to own the certificate files (default: pihole)
            group: Group to own the certificate files (default: ssl-certs)
            verbose: Whether to print verbose output
        """
        super().__init__(cert_name, verbose)
        self.user = user
        self.group = group
        self.cert_dir = f'/etc/letsencrypt/live/{cert_name}'

    @property
    def pihole_cert(self) -> str:
        """Path to the combined certificate file"""
        return f'{self.cert_dir}/pihole.pem'

    def __call__(self) -> None:
        """
        Execute all certificate management operations
        """
        if self.verbose:
            print(f'Setting up Pi-hole certificate for {self.cert_name}')
        self.delete_existing_cert()
        self.create_combined_cert()
        self.set_permissions()
        self.restart_service()

    def delete_existing_cert(self) -> None:
        """
        Delete existing certificate files
        """
        if self.verbose:
            print(f'Deleting existing certificate files for {self.cert_name}')
        
        # Delete combined certificate file
        if os.path.exists(self.pihole_cert):
            os.remove(self.pihole_cert)

    def create_combined_cert(self) -> None:
        """
        Create combined certificate file for Pi-hole
        """
        fullchain = f'{self.cert_dir}/fullchain.pem'
        privkey = f'{self.cert_dir}/privkey.pem'

        # Copy fullchain.pem to pihole.pem
        if self.verbose:
            print(f'Creating combined certificate at {self.pihole_cert}')
        
        shutil.copy2(fullchain, self.pihole_cert)

        # Append privkey.pem to pihole.pem
        with open(privkey, 'r') as priv, open(self.pihole_cert, 'a') as dest:
            dest.write('\n')  # Add newline between cert and key
            shutil.copyfileobj(priv, dest)

    def set_permissions(self) -> None:
        """
        Set proper ownership and permissions on the certificate file
        """
        if self.verbose:
            print(f'Setting ownership to {self.user}:{self.group}')
        
        # Use chown command as it's more reliable for system users/groups
        self.run(['chown', f'{self.user}:{self.group}', self.pihole_cert])
        
        # Set secure permissions (readable only by owner and group)
        os.chmod(self.pihole_cert, 0o640)

    def restart_service(self) -> None:
        """
        Restart the pihole-FTL service
        """
        if self.verbose:
            print('Restarting pihole-FTL service')
        
        self.run(['systemctl', 'restart', 'pihole-FTL'])

    def cert_cmds(self) -> None:
        """
        Override cert_cmds method since we don't just have a list
        of subprocess commands for execution.
        """
        pass