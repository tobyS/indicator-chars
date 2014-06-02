===============
indicator-chars
===============

Forked from: https://github.com/tobyS/indicator-chars

:Original Author: Tobias Schlitt <toby@php.net>

App indicator to provide a menu with special characters for
simple copying them to clipboard (similar to original characters applet).

-------
Install
-------

- Checkout source files ( especially the DEB package ;-)

- Create/Edit ~/.indicator-chars if the one here isn't good enough for you

  - Each row corresponds to a set of chars

  - Optional submenu title prefix: "[title]" (trailing spaces stripped)

  - Optional descriptions after chars: "(description)" (leading &
    trailing spaces stripped)

  - Spaces (apart from above) also count as chars

  - Make sure to use UTF-8 encoding
  
CAUTION: In case of non-DEB installation, be aware that copying a file to system directory "/etc/sudoers.d" might make it impossible to use the sudo command if there's something wrong with that file. Therefore, it might be a good idea to keep this folder open in a Root Nautilus or Terminal window so that you can remove such a file in case of a problem. It might also be a good idea to extract and copy at least that file from the DEB package.

-----------
Changelog
-----------

1.4: Changed icons
1.3: Changed icons, added "copy to clipboard on click" feature from: https://github.com/Cyrille37/indicator-chars
1.2: Another menu item added to edit user config file with zenity, etc.
1.1: Issue of root password requirement to change icon resolved, etc.
1.0: Original code forked: sample user config file added, icon made available also for dark themes, menu item added to change icon, DEB file added, etc.
