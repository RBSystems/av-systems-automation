#!/usr/bin/env python
#update.py
from datetime import datetime
from elasticsearch import Elasticsearch,RequestsHttpConnection
import sys
import telnetlib
import ftplib
import socket

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
halt = None
haltReason = None
SIMPL = "SIMPL"
SPLUS = "SPLUS"
BAK = "USER"
true = "true"
false = "false"

### FUNCTIONS ###
def openTelnet():
	tn=telnetlib.Telnet(host)
	tn.read_until(b"DMPS-300-C>")  ## IT'S READY TO GO HERE

def testDir(dirToTest):
	tn.write(b'isDir('+dirToTest+') \r')
	output = (tn.read_some())
	tn.read_until(b"DMPS-300-C>")
	return output

def iptable():
	tn.write(b'iptable \r')
	iptable = (tn.read_some())
	tn.read_until(b"DMPS-300-C>")
	return iptable

def info():
	tn.write(b'info \r')
	info = (tn.read_some())
	tn.read_until(b"DMPS-300-C>")
	return info

def free():
	tn.write(b'free \r')
	free = (tn.read_some())
	tn.read_until(b"DMPS-300-C>")
	return free

def ramfree():
	tn.write(b'ramfree \r')
	ramfree = (tn.read_some())
	tn.read_until(b"DMPS-300-C>")
	return ramfree

def version():
	tn.write(b'ver \r')
	ver = (tn.read_some())
	tn.read_until(b"DMPS-300-C>")
	return ver

def cd(dir):
	tn.write(b'cd '+ dir +' \r')
	output = (tn.read_some())
	output=tn.read_until(b"DMPS-300-C>")
	return output

def copy(srcDir,dstDir,file):
	tn.write(b'copyfile '+ srcDir +'\\'+ file +' '+ dstDir +'\\'+ file +' \r')
	output = (tn.read_some())
	tn.read_until(b"DMPS-300-C>")
	return output

def fn(func):
	tn.write(b''+ func + ' \r')
	output = tn.read_until(b"DMPS-300-C>")
	return output

print 'At end of functions declaration \r'
### END FUNCTIONS ###

openTelnet()

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
	fn("stopprog")  # Stop the current DMPS program
	print output
	fn("progreset")
	print output
	fn("progcom")
	print output
	fn("ver")
	print output
else:
	print "Error encountered: %d",haltReason
