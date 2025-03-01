"""
Module for converting a Let's Encrypt certificates for use with Emby Server.
"""

from .base import BaseCertManager


class EmbyCertManager(BaseCertManager):
    """
    Creates and executes the commands required to convert an SSL certificate
    for use with Emby.
    """
    def cert_cmds(self) -> None:
        """
        Creates the commands required to convert the cert for use with Emby.
        """
        # Convert certificate to .p12
        self.cmds.append([
            '/usr/bin/openssl', 'pkcs12', '-export',
            '-inkey', f'/etc/letsencrypt/live/{self.cert_name}/privkey.pem',
            '-in', f'/etc/letsencrypt/live/{self.cert_name}/fullchain.pem',
            '-out', f'/etc/letsencrypt/live/{self.cert_name}/fullchain.p12',
            '-password', 'pass:'
        ])

        # Set permissions.
        self.cmds.append(['/usr/bin/chown', 'root:ssl-certs', f'/etc/letsencrypt/live/{self.cert_name}/fullchain.p12'])
        self.cmds.append(['/usr/bin/chmod', '0770', f'/etc/letsencrypt/live/{self.cert_name}/fullchain.p12'])

        # Restart Emby service
        self.cmds.append(['/usr/sbin/service', 'emby-server', 'restart'])
