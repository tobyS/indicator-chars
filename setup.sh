#!/bin/bash
#
pkill -f "/usr/bin/python /usr/local/bin/indicator-chars.py"
sudo rm -Rf "/usr/local/indicator-chars" "/usr/share/indicator-chars"

sudo mkdir -p "/usr/share/indicator-chars"

sudo cp "./indicator-chars.py" "/usr/share/indicator-chars/"
sudo chown root:root "/usr/share/indicator-chars/indicator-chars.py"
sudo chmod 755 "/usr/share/indicator-chars/indicator-chars.py"
sudo ln -sf "/usr/share/indicator-chars/indicator-chars.py" "/usr/local/bin/indicator-chars.py"

sudo cp "./indicator-chars.sh" "/usr/share/indicator-chars/"
sudo chown root:root "/usr/share/indicator-chars/indicator-chars.sh"
sudo chmod a+x "/usr/share/indicator-chars/indicator-chars.sh"

sudo cp "./breeze-dark-theme-icon.svg" "/usr/share/indicator-chars/"
sudo cp "./breeze-light-theme-icon.svg" "/usr/share/indicator-chars/"
sudo cp "./color-theme-icon.svg" "/usr/share/indicator-chars/"
sudo cp "./dark-theme-icon.svg" "/usr/share/indicator-chars/"
sudo cp "./light-theme-icon.svg" "/usr/share/indicator-chars/"
sudo cp "./indicator-chars-icon.svg" "/usr/share/indicator-chars/"
sudo chmod a+rw "/usr/share/indicator-chars/indicator-chars-icon.svg"

sudo cp -f "./indicator-chars.desktop" "/usr/share/applications/"
sudo cp -f "./indicator-chars.desktop" "/etc/xdg/autostart/"
sudo chmod a+x "/etc/xdg/autostart/indicator-chars.desktop"

cp "./.indicator-chars" "/home/$USER/.indicator-chars"
