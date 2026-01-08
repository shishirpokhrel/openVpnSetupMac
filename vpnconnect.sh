#!/bin/bash

# -------- CONFIG --------
OPENVPN_BIN="openvpn path"
CONFIG_FILE="openvpn config path"
AUTH_FILE="/Users/yourpchomename/.openvpn-auth"
# new auth file should be created with username and password(username -> linebreak -> password only)
# permission should be 600 to secure file, 600 -> only read+write access to user, no permission for group and other.
# ------------------------

# Check OTP argument
if [[ $# -lt 1 ]]; then
  echo "Usage: $0 <OTP>"
  exit 1
fi
OTP="$1"


# Read username and static password
USERNAME=$(sed -n '1p' "$AUTH_FILE")
STATIC_PASSWORD=$(sed -n '2p' "$AUTH_FILE")
VPN_PASSWORD="${STATIC_PASSWORD}${OTP}"

# Create temporary auth file
TMP_AUTH=$(mktemp)
chmod 600 "$TMP_AUTH"
echo -e "${USERNAME}\n${VPN_PASSWORD}" > "$TMP_AUTH"

# Connect VPN
echo " Starting OpenVPN securely..."
echo "You will be prompted for macOS sudo password."
echo ""

sudo "$OPENVPN_BIN" --config "$CONFIG_FILE" --auth-user-pass "$TMP_AUTH"

# Remove temporary auth file
rm -f "$TMP_AUTH"