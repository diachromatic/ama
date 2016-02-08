#!/usr/bin/python

import os
import sys
import pdb
from Tkinter import *
import tkMessageBox

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
        errorbox("Cannot find file: " + filepath)
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
        errorbox("Can't find file: " + game_exe)
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

class GUI:
    def __init__(self,parent):
        self.textvar = StringVar()
        if exists("settings.dat"):
            self.game_exe = file_to_str("settings.dat")
        else:
            str_to_file("settings.dat","Doukutsu.exe")
            self.game_exe = "Doukutsu.exe"
        self.parent = parent
        self.parent.title("Doukutsu Hack Installer - by Carrotlord")
        self.Container1 = LabelFrame(parent)
        self.Container1["text"]="Options"
        self.Container1.pack(padx="10",pady="10")

        self.label1 = Label(self.Container1)
        filenum = findhexfiles()
        if filenum == 1:
            self.label1["text"] = "1 hex file has been found.\nAre you ready to begin installing the hack?\n"
        else:
            self.label1["text"] = str(filenum)+" hex files have been found.\nAre you ready to begin installing the hack?\n"
        self.label1.pack(side="top")

        self.label2 = Label(self.Container1)
        self.label2["text"] = "Game executable name:"
        self.label2.pack(side="top")

        self.entry1 = Entry(self.Container1)
        self.entry1["width"] = "20"
        self.entry1["exportselection"] = 0
        self.entry1["textvariable"] = self.textvar
        self.entry1.insert(0,self.game_exe)
        self.entry1.pack(side="top")

        self.label3 = Label(self.Container1)
        self.label3["text"] = ""
        self.label3.pack(side="top")

        self.button1 = Button(self.Container1)
        self.button1["text"] = "Install Hack"
        self.button1["width"] = 12
        self.button1["command"] = self.installer
        self.button1.pack(side="top",padx="100",pady="10")

        self.button2 = Button(self.Container1)
        self.button2["text"] = "Exit Program"
        self.button2["width"] = 12
        self.button2["command"] = self.exitprogram
        self.button2.pack(side="top",padx="100",pady="5")

    def installer(self):
        str_to_file("settings.dat",self.entry1.get())
        self.game_exe = self.entry1.get()
        autohack(findhexfiles(),self.game_exe)
        msgbox("Auto-hacking finished!\nCopy and paste " + self.game_exe + " back to the game folder.\nThen test it to make sure nothing went wrong.")
        sys.exit()
        
    def exitprogram(self):
        str_to_file("settings.dat",self.entry1.get())
        self.game_exe = self.entry1.get()
        sys.exit()

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

def errorbox(msg):
    tkMessageBox.showerror("Error",msg)
    sys.exit()

def msgbox(msg):
    tkMessageBox.showinfo("Info",msg)

root = Tk()
guiobj = GUI(root)
if findhexfiles() <= 0:
    errorbox("Couldn't find any hex files in the\nhexdata folder.")
root.mainloop()

sys.exit()
