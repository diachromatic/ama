#!/usr/bin/python

import os
import sys
import pdb

def display2():
    print "------------"
    print ""

def exists(filename):
    try:
        fileobj = open(filename,"r")
    except IOError:
        return 0
    else:
        fileobj.close()
        return 1

def str_to_file(filepath,megastr):
    fileobj = open(filepath,"wb")
    fileobj.write(megastr)
    fileobj.close()

def file_to_str(filepath):
    try:
        fileobj = open(filepath,"rb")
    except:
        error("Cannot find file: " + filepath)
    else:
        megastr = ""
        char = "-"
        while 1:
            char = fileobj.read(1)
            if len(char)!=1:
                break
            megastr = megastr + char
        fileobj.close()
        return megastr

def autohack(totalfiles,game_exe):
    digitstr = "0123456789abcdef"
    offsetstr = "400000"
    dokuoffset = 0
    hexfilepos = 0
    currentchar = "-"
    currentfile = 1
    filelocation = "null"
    if not(exists(game_exe)):
        error("Can't find file: " + game_exe)
    Doku = open(game_exe,"rb+")
    while currentfile <= totalfiles:
        hexfile = open("hexdata/hex"+str(currentfile)+".txt","rb")
        hexfile.seek(0,0)
        offsetstr = hexfile.read(6)
        dokuoffset = int(offsetstr,16)
        if dokuoffset > 0x400000:
            dokuoffset -= 0x400000
        hexfilepos = 6
        while 1:
            hexfile.seek(hexfilepos,0)
            Doku.seek(dokuoffset,0)
            currentchar = hexfile.read(1)
            if len(currentchar) != 1:
                break
            if int(digitstr.count(currentchar.lower())) == 1:
                hexfile.seek(hexfilepos,0)
                tempvar = int(hexfile.read(2),16)
                Doku.write(chr(tempvar));
                dokuoffset += 1
                hexfilepos += 2
            else:
                hexfilepos += 1
        hexfile.close()
        currentfile += 1

def findhexfiles():
    counter = 0
    while 1:
        counter += 1
        try:
            fileobj = open("hexdata/hex"+str(counter)+".txt","r")
        except IOError:
            return counter - 1
        else:
            fileobj.close()

def error(msg):
    print ""
    print "Error."
    print msg
    print "Exiting program..."
    raw_input("")
    sys.exit()

if exists("settings.dat"):
    game_exe = file_to_str("settings.dat")
else:
    str_to_file("settings.dat","Doukutsu.exe")
    game_exe = "Doukutsu.exe"
print "===== Doukutsu Hack Installer ====="
print "--------   By Carrotlord   --------"
print ""
filenum = findhexfiles()
if filenum == 0:
    error("Can't find any hex files in hexdata folder.")
elif filenum == 1:
    print "1 hex file has been found."
else:
    print str(filenum) + " hex files have been found."
print "Are you ready to start installing the hack?"
print ""
while 1:
    print "============ Main Menu ============"
    print "1: Install Hack"
    print "2: Change Game Exe Name [" + game_exe + "]"
    print "3: Exit Program"
    print ""
    choice = raw_input("Enter a number:")
    try:
        choice = int(choice)
    except ValueError:
        error("You did not type in a number.")
    else:
        if choice > 3 or choice < 1:
            error("You didn't type in a number between 1 and 3.")
        if choice == 1:
            display2()
            print "Auto-hacking, please wait..."
            autohack(filenum,game_exe)
            print ""
            print "Auto-hacking finished!\nCopy and paste " + game_exe + " back to the game folder.\nThen test it to make sure nothing went wrong."
            raw_input("")
            sys.exit()
        elif choice == 2:
            display2()
            print "Type in the name of the game executable"
            game_exe = raw_input("you want to hack:")
            str_to_file("settings.dat",game_exe)
            display2()
        else:
            sys.exit()
