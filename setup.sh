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

sudo cp "./color-theme.png" "/usr/local/indicator-chars/"
sudo cp "./dark-theme.png" "/usr/local/indicator-chars/"
sudo cp "./light-theme.png" "/usr/local/indicator-chars/"
sudo cp "./indicator-chars.png" "/usr/local/indicator-chars/"
sudo chmod a+r "/usr/local/indicator-chars/color-theme.png"
sudo chmod a+r "/usr/local/indicator-chars/dark-theme.png"
sudo chmod a+r "/usr/local/indicator-chars/light-theme.png"
sudo chmod a+r "/usr/local/indicator-chars/indicator-chars.png"

sudo cp "./indicator-chars-sudoers" "/etc/sudoers.d/"
sudo chmod 644 "/etc/sudoers.d/indicator-chars-sudoers"

sudo cp -f "./indicator-chars.desktop" "/etc/xdg/autostart/"
sudo cp -f "./indicator-chars.desktop" "/usr/share/applications/"

cp "./.indicator-chars" "/home/$USER/.indicator-chars"
