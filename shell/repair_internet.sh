#!/bin/bash
sudo kill -9 $(pgrep -f outline)
sudo iptables -F
sudo ip6tables -F
sudo iptables -t nat -F
sudo systemctl stop systemd-resolved
sudo rm /etc/resolv.conf
echo "nameserver 8.8.8.8" | sudo tee /etc/resolv.conf
sudo systemctl start systemd-resolved
sudo dhclient -r && sudo dhclient wlo1
sudo systemctl restart outline_proxy_controller.service
(cd ~/Downloads && ./Outline-Client.AppImage) &
