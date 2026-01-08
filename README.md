Step-by-Step Guide: Secure OpenVPN on macOS (Generic)

Step 1: Install Homebrew (if needed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew --version

Step 2: Install OpenVPN
brew install openvpn


Check OpenVPN path:

which openvpn


Use this path in OPENVPN_BIN in the script.

Step 3: Place your OpenVPN config file

Copy your .ovpn file somewhere convenient (e.g., $HOME/vpnconfig.ovpn)

Update CONFIG_FILE in the script with this path.

Step 4: Create credentials file
nano ~/.openvpn-auth

Line 1 → VPN username

Line 2 → Static password (without OTP)

Example:

myusername
mypassword


Set file permissions:

chmod 600 ~/.openvpn-auth


This ensures only your user can read/write the file.

Step 5: Save and make script executable

Save the connectVPN.sh script to your home folder.

Make it executable:

chmod +x ~/connectVPN.sh

Step 6: Connect to VPN
~/connectVPN.sh 123456


Replace 123456 with your OTP

The script reads your username and static password from .openvpn-auth

Temporary file is automatically deleted after use

Only macOS sudo password and OTP are needed