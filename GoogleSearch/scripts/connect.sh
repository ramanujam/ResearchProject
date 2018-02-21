#!/bin/sh
sudo openvpn --config `ls ~/ResearchProject/GoogleSearch/vpn/us*443.ovpn | shuf | head -1` --auth-user-pass auth.txt
