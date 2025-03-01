"""
A Python package for managing Let's Encrypt SSL certificates for various applications.
"""

from .base import BaseCertManager
from .unifi import UnifiCertManager
from .pihole import PiHoleCertManager
from .emby import EmbyCertManager
from .freepbx import FreePBXCertManager

__version__ = "0.1.0"
__all__ = ["BaseCertManager", "UnifiCertManager", "PiHoleCertManager", "EmbyCertManager", "FreePBXCertManager"]
