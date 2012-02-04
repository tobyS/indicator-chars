===============
indicator-chars
===============

:Author: Tobias Schlitt <toby@php.net>

App indicator to provide a menu with (potentially funny UTF-8) characters for
simple copying them to clipboard (similar to original characters applet).

Create a file .indicator-chars in your home directory with lines of
characters to be selectable.

-------
Install
-------

- Checkout source code

- Create ~/.indicator-chars

  - Each row corresponds to a set of chars

  - Optional submenu title prefix: "[title]" (trailing spaces stripped)

  - Optional descriptions after chars: "(description)" (leading &
    trailing spaces stripped)

  - Spaces (apart from above) also count as chars

  - Make sure to use UTF-8 encoding

- Put indicator-chars.py into auto start

-----------
Open issues
-----------

- If anyone could design a nice, unity style indicator icon?

- Maybe there is a way to use multiple click buttons in menu items?

  - No standard Gtk way does not work.
