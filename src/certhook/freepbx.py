"""
Module for setting up a Let's Encrypt certificates for use with FreePBX/Asterisk
"""

from .base import BaseCertManager


class FreePBXCertManager(BaseCertManager):
    """
    Copies and executes the commands required to set an SSL certificate
    for use with Asterisk on FreePBX.
    """

    def cert_cmds(self) -> None:
        """
        Creates all the commands needed to import the certificate into Asterisk.
        """
        # Copy certificates to Asterisk keys directory
        self.cmds.extend([
            ['cp', f'/etc/letsencrypt/live/{self.cert_name}/cert.pem',
             f'/etc/asterisk/keys/{self.cert_name}.crt'],
            ['cp', f'/etc/letsencrypt/live/{self.cert_name}/privkey.pem',
             f'/etc/asterisk/keys/{self.cert_name}.key']
        ])

        # Set proper ownership and permissions
        self.cmds.extend([
            ['chmod', '-R', '0700', '/etc/asterisk/keys/'],
            ['chown', '-R', 'asterisk:asterisk', '/etc/asterisk/keys/']
        ])

        # Configure Asterisk/FreePBX to use the new certificate
        self.cmds.extend([
            ['/usr/sbin/fwconsole', 'certificate', '--import'],
            ['/usr/sbin/fwconsole', 'certificate', '--default=0'],
            ['/usr/sbin/fwconsole', 'sysadmin', 'installHttpsCert', 'default'],
            ['/usr/sbin/fwconsole', 'sysadmin', 'updatecert'],
            ['/usr/sbin/service', 'apache2', 'restart']
        ])
