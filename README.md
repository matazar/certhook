# CertHook

A Python package for managing Let's Encrypt SSL certificates for various applications.

## Installation

1. Download package from GitHub
2. Install with pip:
    ```pip install certhook-<version>-py3-none-any.whl```
    e.g.
    ```pip install certhook-0.1.0-py3-none-any.whl```

## Usage

### Command Line Interface

The command line interface follows this pattern:
```certhook [options] <app> <certificate-name>```

Supported apps:
- unifi: Manage certificates for UniFi OS
- pihole: Manage certificates for Pi-hole
- emby: Manage certificates for Emby
- freepbx: Manage certificates for FreePBX

Examples:
```
# Update UniFi Controller certificate
certhook unifi example.com

# Update Pi-hole certificate
certhook pihole example.com

# Update Emby certificate
certhook emby example.com

# Update FreePBX certificate
certhook freepbx example.com

# Help
certhook --help
```

## Requirements

- Python 3.6 or higher
- OpenSSL
- Let's Encrypt certificates in `/etc/letsencrypt/live/`

## License

MIT License
