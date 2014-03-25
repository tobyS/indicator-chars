#!/usr/bin/python
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

APP_NAME = 'indicator-chars'
APP_VERSION = '0.2'

class IndicatorChars:
    CHARS_PATH = os.path.join(os.getenv('HOME'), '.indicator-chars')
    SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))

    submenu_title_pattern = re.compile(r'\[([^]]+)\] *')
    description_pattern = re.compile(r' *(\([^)]+\)) *')

    def __init__(self):
        self.ind = appindicator.Indicator(
            "Chars", os.path.join(self.SCRIPT_DIR, 'indicator-chars.png'),
            appindicator.CATEGORY_APPLICATION_STATUS)
        self.ind.set_status(appindicator.STATUS_ACTIVE)        

        self.update_menu()

    def create_menu_item(self, label):
        item = gtk.MenuItem()
        item.set_label(label)
        return item

    def on_chars_changed(self, filemonitor, file, other_file, event_type):
        if event_type == gio.FILE_MONITOR_EVENT_CHANGES_DONE_HINT:
            print 'Characters changed, updating menu...'
            self.update_menu()
    
    def update_menu(self, widget = None, data = None):
        try:
            charDef = open(self.CHARS_PATH).readlines()
        except IOError:
            charDef = []

        # Create menu
        menu = gtk.Menu()
        
        for charLine in charDef:
            charLine = unicode(charLine)
            charLine = charLine.strip()
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
        quit_item.connect("activate", self.on_quit)
        menu.append(quit_item)

        # Show the menu
        self.ind.set_menu(menu)
        menu.show_all()

    def on_char_click(self, widget, char):
        cb = gtk.Clipboard(selection="PRIMARY")
        cb.set_text(char)

    def EditConfig(self, dude):
	os.system("/usr/local/indicator-chars/edit-user-config")

    def DarkTheme(self, dude):
	os.system("sudo /usr/local/indicator-chars/dark-theme-icon && /usr/local/indicator-chars/restart")

    def LightTheme(self, dude):
	os.system("sudo /usr/local/indicator-chars/light-theme-icon && /usr/local/indicator-chars/restart")

    def on_quit(self, widget):
        gtk.main_quit()


if __name__ == "__main__":
    # Catch CTRL-C
    signal.signal(signal.SIGINT, lambda signal, frame: gtk.main_quit())

    # Run the indicator
    i = IndicatorChars()
    
    # Monitor bookmarks changes 
    file = gio.File(i.CHARS_PATH)
    monitor = file.monitor_file()
    monitor.connect("changed", i.on_chars_changed)            
    
    # Main gtk loop
    gtk.main()
