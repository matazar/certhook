"""
Module for converting a Let's Encrypt certificates for use with Unifi OS.
"""

from typing import List
from .base import BaseCertManager


class UnifiCertManager(BaseCertManager):
    """
    Creates and executes the commands required to install SSL certificates
    on Unifi OS, at least for the Unifi Network and Unifi Protect apps.
    """

    def cert_cmds(self) -> None:
        """
        Creates the commands required to install the certificate
        within Unifi OS/Network/Protect.
        """
        # Convert certificate to .p12
        self.cmds.append(['/usr/bin/openssl', 'pkcs12', '-export',
                         '-inkey', f'/etc/letsencrypt/live/{self.cert_name}/privkey.pem',
                         '-in', f'/etc/letsencrypt/live/{self.cert_name}/fullchain.pem',
                         '-out', f'/etc/letsencrypt/live/{self.cert_name}/fullchain.p12',
                         '-name', 'unifi', '-password', 'pass:unifi'])

        # Import certificate into Unifi Network
        self.cmds.append(['/usr/bin/keytool', '-importkeystore',
                          '-deststorepass', 'aircontrolenterprise',
                          '-destkeypass', 'aircontrolenterprise',
                          '-destkeystore', '/data/unifi/data/keystore',
                          '-srckeystore',
                          f'/etc/letsencrypt/live/{self.cert_name}/fullchain.p12',
                          '-srcstoretype', 'PKCS12', '-srcstorepass',
                          'unifi', '-noprompt'])
        # Restart Unifi Core/Network
        self.cmds.append(['/usr/sbin/service', 'unifi-core', 'restart'])
        self.cmds.append(['/usr/sbin/service', 'unifi', 'restart'])