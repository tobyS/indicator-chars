#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#
# Very simple chars indicator.
# Author: Tobias Schlitt <toby@php.net>
#
# Copyright (c) 2011, Tobias Schlitt
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer.  Redistributions
# in binary form must reproduce the above copyright notice, this list of
# conditions and the following disclaimer in the documentation and/or
# other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
# INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE
# USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH
# DAMAGE.

import os
import re
import gtk
import gio
import signal
import subprocess
import appindicator
import sys

APP_NAME = 'indicator-chars'
APP_VERSION = '1.3'

class IndicatorChars:
    CHARS_PATH = os.path.join(os.getenv('HOME'), '.indicator-chars')
    SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))

    def __init__(self):
        self.ind = appindicator.Indicator(
            'Chars', os.path.join(self.SCRIPT_DIR, 'indicator-chars-icon.png'),
            appindicator.CATEGORY_APPLICATION_STATUS)
        self.ind.set_status(appindicator.STATUS_ACTIVE)

        self.update_menu()

    def create_menu_item(self, label):
        item = gtk.MenuItem()
        item.set_label(label)
        return item

    def on_chars_changed(self, filemonitor, file, other_file, event_type):
        if event_type == gio.FILE_MONITOR_EVENT_CHANGES_DONE_HINT:
            #print 'Characters changed, updating menu...'
            self.update_menu()

    @staticmethod
    def parse_line(line):
        '''Parses a line from the configuration file.

        Returns a tuple (title, items), where items is a list of tuples
        (character, label).

        >>> IndicatorChars.parse_line('abc')
        (u'abc', [(u'a', u'a'), (u'b', u'b'), (u'c', u'c')])
        >>> IndicatorChars.parse_line('  a  b  c  ')
        (u'abc', [(u'a', u'a'), (u'b', u'b'), (u'c', u'c')])
        >>> IndicatorChars.parse_line(' [ title ]  a  b  c  ')
        (u' title ', [(u'a', u'a'), (u'b', u'b'), (u'c', u'c')])
        >>> IndicatorChars.parse_line(' [ title ]  a  b   (foobar)    c  ')
        (u' title ', [(u'a', u'a'), (u'b', u'b (foobar)'), (u'c', u'c')])
        >>> IndicatorChars.parse_line(' [ title ]  ab(foobar)c  ')
        (u' title ', [(u'a', u'a'), (u'b', u'b (foobar)'), (u'c', u'c')])
        >>>
        '''
        title = None
        items = []

        submenu_title_pattern = re.compile(r'\[([^]]+)\] *')
        description_pattern = re.compile(r'(.) *(\([^)]+\))? *')

        # Making sure the string is unicode and removing extra whitespace.
        line = unicode(line, 'utf8', 'replace').strip()

        # Checking for '[title]'.
        submenu_match = submenu_title_pattern.match(line)
        if submenu_match:
            title = submenu_match.group(1)
            # Removing title part from line.
            line = line[submenu_match.end():].strip()

        # Iterating over line to get all characters.
        while line:
            description_match = description_pattern.match(line)
            if not description_match:
                # Something very wrong happened.
                pass

            char = description_match.group(1)
            description = description_match.group(2)
            if description is None:
                description = char
            else:
                description = char + u' ' + description

            # Adding the item.
            items.append((char, description))

            # Removing item from line.
            line = line[description_match.end():].strip()

        if title is None:
            # Auto-generating a title by concatenating all chars.
            title = u''.join(item[0] for item in items)

        return (title, items)

    def parse_config_file(self):
        try:
            with open(self.CHARS_PATH) as f:
                # Reading and ignoring whitespace.
                charDef = [ line.strip() for line in f.readlines() ]
                # Ignoring blank lines and comments.
                charDef = [ line for line in charDef if line and line[0] != '#' ]
        except IOError:
            charDef = []

        for charLine in charDef:
            yield self.parse_line(charLine)

    def update_menu(self, widget=None, data=None):
        # Create menu
        menu = gtk.Menu()

        for title, items in self.parse_config_file():
            parentItem = self.create_menu_item(title)
            subMenu = gtk.Menu()

            for char, desc in items:
                subItem = self.create_menu_item(desc)
                subItem.connect('activate', self.on_char_click, char)
                subMenu.append(subItem)

            parentItem.set_submenu(subMenu)
            menu.append(parentItem)

        menu.append(gtk.SeparatorMenuItem())
        EditConfig_item = self.create_menu_item('Edit chars menu')
        EditConfig_item.connect("activate", self.EditConfig)
        menu.append(EditConfig_item)
        menu.append(gtk.SeparatorMenuItem())
        DarkTheme_item = self.create_menu_item('Use dark theme icon')
        DarkTheme_item.connect("activate", self.DarkTheme)
        menu.append(DarkTheme_item)
        LightTheme_item = self.create_menu_item('Use light theme icon')
        LightTheme_item.connect("activate", self.LightTheme)
        menu.append(LightTheme_item)
        quit_item = self.create_menu_item('Quit')
        quit_item.connect('activate', self.on_quit)
        menu.append(quit_item)

        # Show the menu
        self.ind.set_menu(menu)
        menu.show_all()

    def on_char_click(self, widget, char):
        cb = gtk.Clipboard(selection='PRIMARY')
        cb.set_text(char)
        cb = gtk.Clipboard(selection='CLIPBOARD')
        cb.set_text(char)
        cb = gtk.Clipboard(selection="CLIPBOARD")
        cb.set_text(char)

    def EditConfig(self, dude):
	os.system("/usr/local/indicator-chars/edit-user-config")

    def DarkTheme(self, dude):
	os.system("sudo /usr/local/indicator-chars/dark-theme-icon && /usr/local/indicator-chars/restart")

    def LightTheme(self, dude):
	os.system("sudo /usr/local/indicator-chars/light-theme-icon && /usr/local/indicator-chars/restart")

    def on_quit(self, widget):
        gtk.main_quit()


if __name__ == '__main__':
    if len(sys.argv) >= 2 and sys.argv[1] == '--test':
        import doctest
        failure_count, test_count = doctest.testmod()
        print '{0} of {1} tests have failed'.format(failure_count, test_count)
        if failure_count > 0:
            sys.exit(1)
        else:
            sys.exit(0)

    # Catch CTRL-C
    signal.signal(signal.SIGINT, lambda signal, frame: gtk.main_quit())

    # Run the indicator
    i = IndicatorChars()

    # Monitor bookmarks changes
    file = gio.File(i.CHARS_PATH)
    monitor = file.monitor_file()
    monitor.connect('changed', i.on_chars_changed)

    # Main gtk loop
    gtk.main()
