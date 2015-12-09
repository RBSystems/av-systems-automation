#!/usr/bin/env python
#update.py
from datetime import datetime
from elasticsearch import Elasticsearch,RequestsHttpConnection
import sys
import ftplib
import os
import socket
import telnetlib

host = '10.6.36.51'
port = 41795
size = 1024
output = None
splusExists = None
simplExists = None
iptable = None
info = None
free = None
ramfree = None
ver = None
halt = 0
haltReason = None
SIMPL = "SIMPL"
SPLUS = "SPLUS"
BAK = "USER"
true = "true"
false = "false"
telnetClient = telnetlib.Telnet()

### FUNCTIONS ###
def openTelnet():
	telnetClient=telnetlib.Telnet(host)
	telnetClient.read_until(b"DMPS-300-C>")  ## IT'S READY TO GO HERE

def closeTelnet():
	telnetClient.close()

def isTelnetLive():
	s=telnetClient.get_socket()
	if s == 0:
		return false
	else:
		return true

def testDir(dirToTest):
	telnetClient.write(b'isDir('+dirToTest+') \r')
	output = (telnetClient.read_some())
	telnetClient.read_until(b"DMPS-300-C>")
	return output

def iptable():
	telnetClient.write(b'iptable \r')
	iptable = (telnetClient.read_some())
	telnetClient.read_until(b"DMPS-300-C>")
	return iptable

def info():
	telnetClient.write(b'info \r')
	info = (telnetClient.read_some())
	telnetClient.read_until(b"DMPS-300-C>")
	return info

def free():
	telnetClient.write(b'free \r')
	free = (telnetClient.read_some())
	telnetClient.read_until(b"DMPS-300-C>")
	return free

def ramfree():
	telnetClient.write(b'ramfree \r')
	ramfree = (telnetClient.read_some())
	telnetClient.read_until(b"DMPS-300-C>")
	return ramfree

def version():
	telnetClient.write(b'ver \r')
	ver = (telnetClient.read_some())
	telnetClient.read_until(b"DMPS-300-C>")
	return ver

def cd(dir):
	telnetClient.write(b'cd '+ dir +' \r')
	output = (telnetClient.read_some())
	output=telnetClient.read_until(b"DMPS-300-C>")
	return output

def copy(srcDir,dstDir,file):
	telnetClient.write(b'copyfile '+ srcDir +'\\'+ file +' '+ dstDir +'\\'+ file +' \r')
	output = (telnetClient.read_some())
	telnetClient.read_until(b"DMPS-300-C>")
	return output

def fn(func):
	telnetClient.write(b''+ func + ' \r')
	output = telnetClient.read_until(b"DMPS-300-C>")
	return output

print 'At end of functions declaration \r'
### END FUNCTIONS ###

openTelnet()

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

	#Change Directory to build dir
	projectDir=os.path.abspath(os.getcwd())
	os.chdir(projectDir + "/build")

	cd 

	## Move new program
	#fn("stopprog")  # Stop the current DMPS program
	#print output
	#fn("progreset")
	#print output
	#fn("progcom")
	#print output
	#fn("ver")
	#print output
else:
	print "Error encountered: %d",haltReason


closeTelnet()
assert isTelnetLive() == false
