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

### Halt Function ###

def halt(reason):
	print reason
	sys.exit()

### HANDLE ARGUMENTS ###
if len(sys.argv) <> 3:
	print ("Usage: python updateDmpsProgram.py updateFrom updateTo \r")
	print ("Example: python updateDmpsProgram 4.3 4.4 \r")
	sys.exit()
else:
	reqVer = sys.argv[1]
	upgradeVer = sys.argv[2]

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
	ver = retVal
	return retVal

def cd(dir):
	global telnetClient
	telnetClient.write(b'cd '+ dir +' \r')
	output = (telnetClient.read_some())
	output=telnetClient.read_until(b"DMPS-300-C>")
	return output

def copy(srcDir,dstDir,file):
	global telnetClient
	telnetClient.write(b'copyfile '+ srcDir +'\\'+ file +' '+ dstDir +'\\'+ file +' \r')
	output = (telnetClient.read_some())
	telnetClient.read_until(b"DMPS-300-C>")
	return output

def fn(func):
	global telnetClient
	telnetClient.write(b''+ func + ' \r')
	output = telnetClient.read_until(b"DMPS-300-C>")
	return output

def push(file):
	global telnetClient


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

## system info gate logic
#info()

## Version gate logic
version()
ver = ver.replace("v","")
assert ver == reqVer   ## Prerequisite version number met

## freespace gate logic
free1=free()
free2=free()
assert free1 == free2 ## Memory is stable, no active operations

## Move ahead
#print 'moving ahead \r'
#	
##BACKUP STEPS
#if testDir(BAK) == true:
#	print 'cd to BAK \r'
#	cd(BAK)
#	print 'copying ~.Manifest \r'
#	copy(SIMPL,BAK,"~.Manifest")
#	print 'copy done \r'
#else:
#	print "\r"
#
#if testDir(SIMPL) == true:
#
#	## Move new program
#	#fn("stopprog")  # Stop the current DMPS program
#	#print output
#	#fn("progreset")
#	#print output
#	#fn("progcom")
#	#print output
#	print free()


## Close active session
telnetClient=closeTelnet()
assert isTelnetLive() == false
