===============
indicator-chars
===============

Forked from: https://github.com/tobyS/indicator-chars

:Original Author:Tobias Schlitt <toby@php.net>

App indicator to provide a menu with special characters for
simple copying them to clipboard (similar to original characters applet).

-------
Install
-------

- Checkout source files ( especially the DEB package ;-)

- Create/Edit ~/.indicator-chars

  - Each row corresponds to a set of chars

  - Optional submenu title prefix: "[title]" (trailing spaces stripped)

  - Optional descriptions after chars: "(description)" (leading &
    trailing spaces stripped)

  - Spaces (apart from above) also count as chars

  - Make sure to use UTF-8 encoding

-----------
Open issues
-----------

- Clicking an item copies it to clipboard?

- Maybe there is a way to use multiple click buttons in menu items?

- No standard Gtk way does not work.

-----------
Changelog
-----------

1.2 Another menu item added to edit user config file with zenity, etc.

1.1 Issue of root password requirement to change icon resolved, etc.

1.0 Original code forked: sample user config file added, icon made available also for dark themes, menu item added to change icon, DEB file added, etc.
