#!/usr/bin/env python3
"""
OpenVPN Connection Script with OTP Support
Connects to OpenVPN using username, static password, and one-time password (OTP)
"""

import sys
import os
import subprocess
import tempfile
from pathlib import Path

# -------- CONFIG --------
# Set your OpenVPN binary path (use 'which openvpn' to find it)
OPENVPN_BIN = "/usr/sbin/openvpn"

# Set your OpenVPN config file path (.ovpn)
CONFIG_FILE = "/mnt/c/Users/eSewa/shishir.pokhrel__ssl_vpn_config.ovpn"

# Path to your credentials file with username and static password
AUTH_FILE = os.path.expanduser("/mnt/c/Users/eSewa/.openvpn-auth")
# Create this file with:
# line 1 -> username
# line 2 -> password
# Permissions must be 600 (read/write only for user)
# ------------------------


def read_credentials(auth_file):
    """Read username and static password from auth file."""
    try:
        with open(auth_file, 'r') as f:
            lines = f.readlines()
            if len(lines) < 2:
                print(f"Error: {auth_file} must contain at least 2 lines (username and password)")
                sys.exit(1)
            username = lines[0].strip()
            static_password = lines[1].strip()
            return username, static_password
    except FileNotFoundError:
        print(f"Error: Auth file not found: {auth_file}")
        print("Create the file with:")
        print("  line 1: username")
        print("  line 2: static password")
        print("Then set permissions: chmod 600 ~/.openvpn-auth")
        sys.exit(1)
    except PermissionError:
        print(f"Error: Permission denied reading {auth_file}")
        sys.exit(1)


def create_temp_auth_file(username, vpn_password):
    """Create a temporary auth file with proper permissions."""
    # Create temporary file
    fd, tmp_path = tempfile.mkstemp(prefix='openvpn-', suffix='.auth')
    
    try:
        # Set permissions to 600 (read/write for user only)
        os.chmod(tmp_path, 0o600)
        
        # Write credentials
        with os.fdopen(fd, 'w') as f:
            f.write(f"{username}\n{vpn_password}\n")
        
        return tmp_path
    except Exception as e:
        # Clean up on error
        try:
            os.close(fd)
        except:
            pass
        try:
            os.unlink(tmp_path)
        except:
            pass
        raise e


def connect_vpn(openvpn_bin, config_file, tmp_auth_file):
    """Connect to OpenVPN using sudo."""
    try:
        print("Starting OpenVPN securely...")
        print("You will be prompted for macOS sudo password.")
        print()
        
        # Run OpenVPN with sudo
        subprocess.run(
            ['sudo', openvpn_bin, '--config', config_file, '--auth-user-pass', tmp_auth_file],
            check=True
        )
    except subprocess.CalledProcessError as e:
        print(f"\nError: OpenVPN connection failed with exit code {e.returncode}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\nConnection interrupted by user")
        sys.exit(0)


def main():
    # Check OTP argument
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <OTP>")
        print("\nExample:")
        print(f"  {sys.argv[0]} 123456")
        sys.exit(1)
    
    otp = sys.argv[1]
    
    # Read username and static password
    username, static_password = read_credentials(AUTH_FILE)
    
    # Combine static password with OTP
    vpn_password = f"{static_password}{otp}"
    
    # Create temporary auth file
    tmp_auth_file = None
    try:
        tmp_auth_file = create_temp_auth_file(username, vpn_password)
        
        # Connect to VPN
        connect_vpn(OPENVPN_BIN, CONFIG_FILE, tmp_auth_file)
        
    finally:
        # Always clean up temporary auth file
        if tmp_auth_file and os.path.exists(tmp_auth_file):
            try:
                os.unlink(tmp_auth_file)
            except Exception as e:
                print(f"Warning: Could not remove temporary file {tmp_auth_file}: {e}")


if __name__ == "__main__":
    main()
