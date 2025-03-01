"""
Pytest configuration and fixtures
"""

import pytest
from pathlib import Path


@pytest.fixture
def cert_name() -> str:
    """Set the certificate name for testing"""
    return "example.com"


@pytest.fixture
def test_certs(cert_name: str, tmp_path: Path) -> Path:
    """Create temporary certificate paths with real self-signed certificates for testing"""
    live_dir = tmp_path / "etc" / "letsencrypt" / "live" / cert_name
    live_dir.mkdir(parents=True)
    
    # Generate CA key and certificate
    ca_key = live_dir / "ca-key.pem"
    ca_cert = live_dir / "ca-cert.pem"
    
    # Generate server key (this will be privkey.pem)
    server_key = live_dir / "privkey.pem"
    server_csr = live_dir / "server.csr"
    server_cert = live_dir / "cert.pem"
    fullchain = live_dir / "fullchain.pem"
    
    # Generate CA key and self-signed certificate
    import subprocess
    subprocess.run([
        'openssl', 'req', '-x509', '-new', '-nodes',
        '-keyout', str(ca_key), '-out', str(ca_cert),
        '-subj', '/CN=Test CA',
        '-days', '365'
    ], check=True)
    
    # Generate server key and CSR
    subprocess.run([
        'openssl', 'req', '-new', '-nodes',
        '-keyout', str(server_key), '-out', str(server_csr),
        '-subj', f'/CN={cert_name}',
    ], check=True)
    
    # Sign the server certificate with CA
    subprocess.run([
        'openssl', 'x509', '-req',
        '-in', str(server_csr), '-CA', str(ca_cert),
        '-CAkey', str(ca_key), '-CAcreateserial',
        '-out', str(server_cert),
        '-days', '365'
    ], check=True)
    
    # Create fullchain by concatenating server cert and CA cert
    with open(fullchain, 'wb') as f:
        f.write(server_cert.read_bytes())
        f.write(ca_cert.read_bytes())
    
    return live_dir
