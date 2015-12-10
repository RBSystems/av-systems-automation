#!/usr/bin/env python
#update.py
import sys
from datetime import datetime
from elasticsearch import Elasticsearch,RequestsHttpConnection
import ftplib
import os
from parse import *
import socket
import telnetlib
import time

host = '10.6.36.51'
port = 41795
size = 1024
reqVer = ""
upgradeVer = ""

output = ""
splusExists = ""
simplExists = ""
iptable = ""
info = ""
ver = ""
halt = 0
haltReason = ""
SIMPL = "SIMPL"
SPLUS = "SPLUS"
BAK = "USER"
true = "true"
false = "false"
parserResult = ""
telnetClient = telnetlib.Telnet()
simplfiles = ["~.Manifest","TEC HD v4.3.bin","TEC HD v4.3.dip","TEC HD v4.3.dsc","TEC HD v4.3.fp2","TEC HD v4.3.ird","TEC HD v4.3.rte","TEC HD v4.3.rvi",".~Program_Boot_Data"]
splusfiles = ["_S2_TEC_HD_v4_3.spl"]

### System Functions ###

def halt(reason):
	print reason
	sys.exit()

def is_number(s):
	try:
		float(s)
		return true
	except ValueError:
		pass

	try:
		import unicodedata
		unicodedata.numeric(s)
		return true
	except (TypeError, ValueError):
		pass
	return false


### HANDLE ARGUMENTS ###
if len(sys.argv) <> 3:
	print ("Usage: python updateDmpsProgram.py updateFrom updateTo \r")
	print ("Example: python updateDmpsProgram 4.3 4.4 \r")
	sys.exit()
else:
	reqVer = sys.argv[1]
	upgradeVer = sys.argv[2]
	assert is_number(reqVer) == true
	assert is_number(upgradeVer) == true
	## !! TEST TO SEE IF VERSIONS REQUESTED EXIST

### END HANDLE ARGUMENTS ###


### FUNCTIONS ###
def openTelnet():
	global telnetClient
	telnetClient=telnetlib.Telnet(host,port)
	telnetClient.read_until(b"DMPS-300-C>")  ## IT'S READY TO GO HERE
	return telnetClient

def closeTelnet():
	global telnetClient
	telnetClient.close()
	return telnetClient

def isTelnetLive():
	global telnetClient
	s=telnetClient.get_socket()
	if s == 0:
		return false
	else:
		return true

def testDir(dirToTest):
	global telnetClient
	telnetClient.write(b'isDir('+dirToTest+') \r')
	output = (telnetClient.read_some())
	telnetClient.read_until(b"DMPS-300-C>")
	return output

def iptable():
	global telnetClient,iptable
	telnetClient.write(b'iptable \r')
	iptable = (telnetClient.read_some())
	telnetClient.read_until(b"DMPS-300-C>")
	return iptable

def info():
	global telnetClient,info
	telnetClient.write(b'info \r')
	info = (telnetClient.read_some())
	telnetClient.read_until(b"DMPS-300-C>")
	return info

def free():
	global telnetClient
	telnetClient.write(b'free \r')
	free = (telnetClient.read_some())
	telnetClient.read_until(b"DMPS-300-C>")
	return free

def ramfree():
	global telnetClient
	telnetClient.write(b'ramfree \r')
	ramfree = (telnetClient.read_some())
	telnetClient.read_until(b"DMPS-300-C>")
	return ramfree

def version():
	global telnetClient,ver
	telnetClient.write(b'\r\rprogcomments \r')
	localVer = (telnetClient.read_until("Program File"))
	split = localVer.split("TEC")
	retVal = ""
	for line in split:
		if line.find("v") <> -1:
			retVal = line

	splitLine = retVal.split(" ")
	for word in splitLine:
		if word.find(".") <> -1:
			word = word.strip()
			word = word.replace("Program","")
			word = word.replace("\r","")
			word = word.replace("\n","")
			retVal = word

	telnetClient.read_until(b"DMPS-300-C>")
	ver = retVal.replace("v","")
	return retVal

def cd(dir):
	global telnetClient
	telnetClient.write(b'cd '+ dir +' \r')
	output = (telnetClient.read_some())
	output=telnetClient.read_until(b"DMPS-300-C>")
	return output

def copy(file):
	global telnetClient
	telnetClient.write(b'copyfile \"' + file +'\" \"\\USER\\' + file + '\" \r')
	output = (telnetClient.read_until(b"DMPS-300-C>"))
	return output

def backup():
	global telnetClient
	fn("del \USER\*.*")
	telnetClient.write(b'copyfile "\SIMPL\~.Manifest" "\USER\~.Manifest" \r')
	output = (telnetClient.read_until(b"DMPS-300-C>"))
	telnetClient.write(b'copyfile "\SIMPL\TEC HD v4.3.bin" "\USER\TEC HD v4.3.bin" \r')
	output = (telnetClient.read_until(b"DMPS-300-C>"))
	telnetClient.write(b'copyfile "\SIMPL\TEC HD v4.3.dip" "\USER\TEC HD v4.3.dip" \r')
	output = (telnetClient.read_until(b"DMPS-300-C>"))
	telnetClient.write(b'copyfile "\SIMPL\TEC HD v4.3.dsc" "\USER\TEC HD v4.3.dsc" \r')
	output = (telnetClient.read_until(b"DMPS-300-C>"))
	telnetClient.write(b'copyfile "\SIMPL\TEC HD v4.3.fp2" "\USER\TEC HD v4.3.fp2" \r')
	output = (telnetClient.read_until(b"DMPS-300-C>"))
	telnetClient.write(b'copyfile "\SIMPL\TEC HD v4.3.ird" "\USER\TEC HD v4.3.ird" \r')
	output = (telnetClient.read_until(b"DMPS-300-C>"))
	telnetClient.write(b'copyfile "\SIMPL\TEC HD v4.3.rte" "\USER\TEC HD v4.3.rte" \r')
	output = (telnetClient.read_until(b"DMPS-300-C>"))
	telnetClient.write(b'copyfile "\SIMPL\TEC HD v4.3.rvi" "\USER\TEC HD v4.3.rvi" \r')
	output = (telnetClient.read_until(b"DMPS-300-C>"))
	telnetClient.write(b'copyfile "\SIMPL\.~Program_Boot_Data" "\USER\.~Program_Boot_Data" \r')
	output = (telnetClient.read_until(b"DMPS-300-C>"))
	telnetClient.write(b'copyfile "\SPLUS\_S2_TEC_HD_v4_3.spl" "\USER\_S2_TEC_HD_v4_3.spl" \r')
	output = (telnetClient.read_until(b"DMPS-300-C>"))
	output = "Backed up"
	return output

def fn(func):
	global telnetClient
	telnetClient.write(b''+ func + ' \r')
	output = telnetClient.read_until(b"DMPS-300-C>")
	print output
	return output

def push(file):
	global telnetClient

def cleanTime(t):
	tmp = t[4:] # Remove first four charachters, i.e. "Mon "
	tmp = t[:-8] # Remove last 5 characters, i.e. " 2015"
	return tmp


### END FUNCTIONS ###

### BACKUP ###

#projectDir=os.path.abspath(os.getcwd())
#os.chdir(projectDir + "/bak")
#
#
#telnetClient=openTelnet()
#assert isTelnetLive() == true
#
#
#
#telnetClient=closeTelnet()
#assert isTelnetLive() == false

### END BAK ###

#Change Directory to build dir
projectDir=os.path.abspath(os.getcwd())
os.chdir(projectDir + "/build")

telnetClient=openTelnet()
assert isTelnetLive() == true

## iptable gate logic
#iptable()
#assert iptable == something

## system info gate logic
#info()
#assert info == something

## Version gate logic
version()
assert ver == reqVer   ## Prerequisite version number met

## freespace gate logic
free1=free()
free2=free()
assert free1 == free2 ## Memory is stable, no active operations

##BACKUP STEPS
#bak=backup()
#print bak

if testDir(SIMPL) == true:
	# Move new program
	fn("stopprog")  # Stop the current DMPS program
	print output
	fn("del \SIMPL\*.*")
	fn("del \SPLUS\*.*")
	cd("\SIMPL")

	for f in simplfiles:
		(mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat(f)
		cDate = time.ctime(mtime)
		parsed = cDate.replace("Mon ","")

	print fn("xput" + fileSize + " " + fileDate + " " + fileName)
	#xput .~Program_Boot_Data
	#xput TEC HD v4.3.bin
	#xput TEC HD v4.3.rte
	#xput TEC HD v4.3.fp2
	#xput TEC HD v4.3.ird
	#isdir \SPLUS
	#// TEST TRUE
	#cd \SPLUS\
	#xput _S2_TEC_HD_v4_3.spl
	#isdir \SIMPL
	#// TEST TRUE
	#cd \SIMPL\
	#xput 87255 12-07-15 15:19:28 TEC HD v4.3.rvi
	#xput 883 12-07-15 15:19:28 TEC HD v4.3.dsc
	#xput 173 12-07-15 15:19:28 ~.Manifest
	#xput 165497 12-07-15 23:13:38 TEC HD v4.3.zig
	#\r\n x 4
	#progreset
	#progcom
	
#version()
#assert ver == upgradeVer   ## Prerequisite version number met

## Close active session
telnetClient = closeTelnet()
assert isTelnetLive() == false
