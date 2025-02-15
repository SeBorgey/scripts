#!/bin/bash
sudo killall apt apt-get
sudo apt -f remove 'dotnet*' 'aspnet*' 'netstandard*'
sudo rm -f /etc/apt/sources.list.d/microsoft-prod.list
sudo apt -f install dotnet-sdk-7.0
wget https://github.com/OpenTabletDriver/OpenTabletDriver/releases/latest/download/OpenTabletDriver.deb
sudo apt update
sudo apt -f install ./OpenTabletDriver.deb
rm -f OpenTabletDriver.deb
