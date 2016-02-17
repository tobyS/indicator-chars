#!/bin/bash

edit_menu()
{
FILE=/home/$USER/.indicator-chars
TMP=$(mktemp)
zenity --text-info --editable --title="Edit menu" --filename=$FILE --width 550 --height 550 > $TMP
if [ "$?" = 0 ]
then
DIFF=$(diff -q --from-file "$FILE" "$TMP"; echo $?)
	if [ "$DIFF" != 0 ]
	then
		mv $FILE "$FILE"~
		mv $TMP "$FILE"
		notify-send "Updated menu" -i gtk-dialog-info -t 3000 -u normal
	fi
fi
exit 0
}

change_icon()
{
menu_icon()
{
im="zenity --list --radiolist --title=\"Change Icon\" --text=\"<b>Select icon to use:</b>\" --width 270 --height 170"
im=$im" --column=\"☑\" --column \"Options\" --column \"Description\" "
im=$im"FALSE \"Light\" \"Icon for dark panels\" "
im=$im"FALSE \"Dark\" \"Icon for light panels\" "
im=$im"FALSE \"Color\" \"Icon for all panels\" "
}
option_icon()
{
choice=`echo $im | sh -`
if echo $choice | grep "Light" > /dev/null
then
	cp -f "/usr/local/indicator-chars/dark-theme-icon.png" "/usr/local/indicator-chars/indicator-chars-icon.png"
fi
if echo $choice | grep "Dark" > /dev/null
then
	cp -f "/usr/local/indicator-chars/light-theme-icon.png" "/usr/local/indicator-chars/indicator-chars-icon.png"
fi
if echo $choice | grep "Color" > /dev/null
then
	cp -f "/usr/local/indicator-chars/color-theme-icon.png" "/usr/local/indicator-chars/indicator-chars-icon.png"
fi
}
menu_icon
option_icon
}

restart()
{
killall indicator-chars.py
indicator-chars.py
}

########################################################################

if [ $# -eq 0 ]
then
	echo "You should specify a function as parameter; e.g. change_icon"
	exit 1
else
	for func do
		[ "$(type -t -- "$func")" = function ] && "$func"
	done
fi

exit 0
