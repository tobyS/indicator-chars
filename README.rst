===============
indicator-chars
===============

:Author: Tobias Schlitt <toby@php.net>
:Author: Cyrille37 <cyrille37@gmail.com>

App indicator to provide a menu with (potentially funny UTF-8) characters for
simple copying them to clipboard (similar to original characters applet).

Short video presentation: https://video.comptoir.net/videos/watch/8671fb9d-ce7d-48d8-a5a5-0ce6f1c1316b

Create a file .indicator-chars in your home directory with lines of
characters to be selectable.

This version run with Python 3.
To run with Python 2 use branch https://github.com/Cyrille37/indicator-chars/tree/python2


-------
Changes
-------
- Porting to Python 3
- take chars examples from https://github.com/Sadi58/indicator-chars
- Works with Ubuntu 20 (use Python2 branch for older Ubuntu)
- add a char copy into Clipboard(selection="CLIPBOARD")
- use env to find the Python engine
- add a configuration file example: "conf-example.indicator-chars"

-------
Install
-------

- Checkout source code
 - Install required packages
  - sudo apt install python3-gi python3-gtk gir1.2-appindicator3-0.1
- Create ~/.indicator-chars
  - Each row corresponds to a set of chars
  - Optional submenu title prefix: "[title]" (trailing spaces stripped)
  - Optional descriptions after chars: "(description)" (leading & trailing spaces stripped)
  - Spaces (apart from above) also count as chars
  - Make sure to use UTF-8 encoding
- Put indicator-chars.py into auto start

-------
Issues
-------

- if icon file does not work, like with Ubuntu 12.04 running Unity 2D, you change the code to use icon from a theme icon name.
