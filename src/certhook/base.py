"""
Base module for certificate managers.
"""

import subprocess
from typing import List

class BaseCertManager:
    """
    Base class for certificate managers that provides common functionality
    for managing SSL certificates.
    """

    def __init__(self, cert_name: str, verbose: bool = False):
        """
        Set up the base variables.

        Args:
            cert_name: Name of the certificate
            verbose: Whether to print verbose output
        """
        self.verbose = verbose
        self.cert_name = cert_name
        # Variable to hold all the commands
        self.cmds: List[list] = []
        self.cert_cmds()

    def __call__(self) -> None:
        """
        Execute all the commands.
        """
        if self.verbose:
            print(f'Processing certificate {self.cert_name}')
        for cmd in self.cmds:
            self.run(cmd)

    def run(self, cmd: list) -> subprocess.CompletedProcess:
        """
        Executes the provided command using subprocess.
        stdout/stderr only show when verbose is enabled.

        Args:
            cmd: Command to execute

        Returns:
            CompletedProcess instance with execution results
        """
        results = subprocess.run(cmd, capture_output=True, check=True)
        if self.verbose:
            print('command: %s' % (' '.join(results.args)))
            print('stdout: %s' % (results.stdout.decode('UTF-8')))
            if results.stderr:
                print('stderr: %s' % (results.stderr.decode('UTF-8')))
        return results

    def cert_cmds(self) -> None:
        """
        Method typically overridden by child classes.
        """
        pass