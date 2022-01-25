#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Hacked by Cyrille37 on 2016-02-03
# Hacked by Cyrille37 on 2021-01-25 Python3 and Gtk3
#
# Very simple chars indicator.
# Author: Tobias Schlitt <toby@php.net>
#
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
import signal
import subprocess

#import gtk
#from gi.repository import Gtk, GObject
# sudo apt-get install python-appindicator
#import appindicator

# sudo apt-get install gir1.2-appindicator3
import gi
gi.require_version('Gtk', '3.0')
try:
	gi.require_version('AppIndicator3', '0.1')
	from gi.repository import AppIndicator3 as appindicator
except ImportError:
	from gi.repository import AppIndicator as appindicator

from gi.repository import Gtk as gtk, Gdk, GLib, GObject, Gio as gio

APP_NAME = 'indicator-chars'
APP_VERSION = '0.3'

class IndicatorChars:
    CHARS_PATH = os.path.join(os.getenv('HOME'), '.indicator-chars')
    SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))

    submenu_title_pattern = re.compile(r'\[([^]]+)\] *')
    description_pattern = re.compile(r' *(\([^)]+\)) *')

    def __init__(self):
        self.ind = appindicator.Indicator.new(
            # Custom icon seems to doesn't work on my Ubuntu 12.04 LTS running Unity 2D
            #"Chars", os.path.join(self.SCRIPT_DIR, 'light16x16.png'),
            # So fallback to an referenced theme's icon name
            "Chars", "accessories-character-map",
            # https://gjs-docs.gnome.org/appindicator301~0.1_api/appindicator3.indicatorcategory
            appindicator.IndicatorCategory. APPLICATION_STATUS)
        self.ind.set_status(appindicator.IndicatorStatus.ACTIVE)        

        self.update_menu()

    def create_menu_item(self, label):
        item = gtk.MenuItem()
        item.set_label(label)
        return item

    def on_chars_changed(self, filemonitor, file, other_file, event_type):
        if event_type == gio.FileMonitorEvent.CHANGES_DONE_HINT:
            print( 'Characters changed, updating menu...' )
            self.update_menu()

    def update_menu(self, widget = None, data = None):
        try:
            charDef = open(self.CHARS_PATH).readlines()
        except IOError:
            charDef = []

        # Create menu
        menu = gtk.Menu()

        for charLine in charDef:
            charLine = str(charLine).strip()
            if charLine == '' :
            	continue
            submenu_match = self.submenu_title_pattern.match(charLine)
            if submenu_match:
                submenu_title = submenu_match.group(1)
                # remove title part from remainder:
                charLine = charLine[submenu_match.end():]
            else:
                submenu_title = ''.join(
                    self.description_pattern.split(charLine)[::2])
            parentItem = self.create_menu_item(submenu_title)
            subMenu = gtk.Menu()
            while charLine:
                char = charLine[0]
                charLine = charLine[1:]
                description_match = self.description_pattern.match(charLine)
                if description_match:
                    item_title = char + ' ' + description_match.group(1)
                    # remove description part from remainder:
                    charLine = charLine[description_match.end():]
                else:
                    item_title = char
                subItem = self.create_menu_item(item_title)
                subItem.connect("activate", self.on_char_click, char)
                subMenu.append(subItem)
            parentItem.set_submenu(subMenu)
            menu.append(parentItem)

        menu.append(gtk.SeparatorMenuItem())
        quit_item = self.create_menu_item('Quit')
        quit_item.connect("activate", self.on_quit)
        menu.append(quit_item)

        # Show the menu
        self.ind.set_menu(menu)
        menu.show_all()

    def on_char_click(self, widget, char):
        #cb = gtk.Clipboard(selection="PRIMARY")
        cb = gtk.Clipboard.get(Gdk.SELECTION_PRIMARY)
        cb.set_text(char, -1)
        #cb = gtk.Clipboard(selection="CLIPBOARD")
        cb = gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        cb.set_text(char, -1)

    def on_quit(self, widget):
        gtk.main_quit()


if __name__ == "__main__":
    # Catch CTRL-C
    signal.signal(signal.SIGINT, lambda signal, frame: gtk.main_quit())

    # Run the indicator
    i = IndicatorChars()
    
    # Monitor config file changes 
    file = gio.File.new_for_path(i.CHARS_PATH)
    monitor = file.monitor_file( gio.FileMonitorFlags.NONE, None )
    monitor.connect("changed", i.on_chars_changed)            
    
    # Main gtk loop
    gtk.main()
