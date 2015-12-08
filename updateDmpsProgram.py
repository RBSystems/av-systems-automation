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
def output=""
def splusExists=""
def simplExists=""
def iptable = ""
def info = ""
def free = ""
def ramfree = ""
def ver = ""
def halt = 0
def haltReason = ""

tn=telnetlib.Telnet(host)
tn.read_until(b"DMPS-300-C>")  ## IT'S READY TO GO HERE

### FUNCTIONS ###

def testDir(dirToTest):
	tn.write(b'isDir('+dirToTest+') \r')
	output = (tn.read_some())
	tn.read_until(b"TSW-750>")
	return output

def iptable():
	tn.write(b'iptable \r')
	iptable = (tn.read_some())
	tn.read_until(b"TSW-750>")
	return iptable

def info():
	tn.write(b'info \r')
	info = (tn.read_some())
	tn.read_until(b"TSW-750>")
	return info

def free():
	tn.write(b'free \r')
	free = (tn.read_some())
	tn.read_until(b"TSW-750>")
	return free

def ramfree():
	tn.write(b'ramfree \r')
	ramfree = (tn.read_some())
	tn.read_until(b"TSW-750>")
	return ramfree

def version():
	tn.write(b'ver \r')
	ver = (tn.read_some())
	tn.read_until(b"TSW-750>")
	return ver

### END FUNCTIONS ###

## iptable gate logic
iptable()

## system info gate logic
info()

## Version gate logic
version()

## freespace gate logic
free()

## Move ahead
if (halt <= 0):

	##BACKUP STEPS


	## Move new program
	#stopprog()  # Stop the current DMPS program
else:
	print "Error encountered: %d",haltReason
