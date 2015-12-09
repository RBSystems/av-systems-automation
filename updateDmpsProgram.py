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
output = ""
splusExists = ""
simplExists = ""
iptable = ""
info = ""
free = ""
ramfree = ""
#ver = ""
halt = 0
haltReason = ""
SIMPL = "SIMPL"
SPLUS = "SPLUS"
BAK = "USER"
true = "true"
false = "false"
parserResult = ""
telnetClient = telnetlib.Telnet()

### FUNCTIONS ###
def openTelnet():
	global telnetClient
	telnetClient=telnetlib.Telnet(host)
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
	global telnetClient
	telnetClient.write(b'iptable \r')
	iptable = (telnetClient.read_some())
	telnetClient.read_until(b"DMPS-300-C>")
	return iptable

def info():
	global telnetClient
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

### END FUNCTIONS ###

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
#version()

## freespace gate logic
#free()

## Move ahead
if (halt <= 0):
	print 'moving ahead \r'
	
	##BACKUP STEPS
	#if testDir(BAK) == true:
	#	print 'cd to BAK \r'
	#	cd(BAK)
	#	print 'copying ~.Manifest \r'
	#	copy(SIMPL,BAK,"~.Manifest")
	#	print 'copy done \r'
	#else:
	#	print "\r"

	#if testDir(SIMPL) == true:

	## Move new program
	#fn("stopprog")  # Stop the current DMPS program
	#print output
	#fn("progreset")
	#print output
	#fn("progcom")
	#print output
	print free()

else:
	print "Error encountered: %d",haltReason


telnetClient=closeTelnet()
assert isTelnetLive() == false
