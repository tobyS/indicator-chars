#!/bin/bash
#
killall indicator-chars.py

sudo rm -f "/usr/local/bin/indicator-chars.py"
sudo rm -Rf "/usr/local/indicator-chars"

sudo mkdir -p "/usr/local/indicator-chars"

sudo cp "./indicator-chars.py" "/usr/local/indicator-chars/"
sudo chown root:root "/usr/local/indicator-chars/indicator-chars.py"
sudo chmod 755 "/usr/local/indicator-chars/indicator-chars.py"
sudo ln -sf "/usr/local/indicator-chars/indicator-chars.py" "/usr/local/bin/indicator-chars.py"

sudo cp "./indicator-chars.sh" "/usr/local/indicator-chars/"
sudo chown root:root "/usr/local/indicator-chars/indicator-chars.sh"
sudo chmod a+x "/usr/local/indicator-chars/indicator-chars.sh"

sudo cp "./color-theme-icon.png" "/usr/local/indicator-chars/"
sudo cp "./dark-theme-icon.png" "/usr/local/indicator-chars/"
sudo cp "./light-theme-icon.png" "/usr/local/indicator-chars/"
sudo cp "./indicator-chars-icon.png" "/usr/local/indicator-chars/"
sudo chmod a+rw "/usr/local/indicator-chars/indicator-chars-icon.png"

sudo cp -f "./indicator-chars.desktop" "/etc/xdg/autostart/"
sudo cp -f "./indicator-chars.desktop" "/usr/share/applications/"

cp "./.indicator-chars" "/home/$USER/.indicator-chars"
