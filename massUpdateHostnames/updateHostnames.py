#!/usr/bin/env python
#updateHostnames.py
#2016 - Dan Clegg
import sys
import csv
from datetime import datetime
from elasticsearch import Elasticsearch,RequestsHttpConnection
import ftplib
import os
from parse import *
import socket
import subprocess
import telnetlib


host = 'avreports.byu.edu'
port = 41795
size = 1024

output = ""
hostname = ""
halt = 0
haltReason = ""
true = "true"
false = "false"
parserResult = ""
devType = ""
itemList = ""
projectDir = os.path.abspath(os.getcwd())
telnetClient = telnetlib.Telnet()

### Halt Function ###

def halt(reason):
	print reason
	sys.exit()

### HANDLE ARGUMENTS ###
if len(sys.argv) <> 2:
	print ("Usage: python updateHostnames.py fileName \r")
	print ("Example: python updateHostnames test.csv \r")
	sys.exit()
else:
	devType = sys.argv[1]

### END HANDLE ARGUMENTS ###

### FUNCTIONS ###

def importList(fileName):
	iL = ""
	with open(fileName, 'rb') as f:
		reader = csv.reader(f)
		iL = list(reader)
	return iL

def openTelnet(telnetHost):
	global telnetClient
	telnetClient=telnetlib.Telnet(telnetHost,port)
	#TODO: HAndle more than DMPS
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

def free():
	global telnetClient
	telnetClient.write(b'free \r')
	free = (telnetClient.read_some())
	#TODO: HAndle more than DMPS
	telnetClient.read_until(b"DMPS-300-C>")
	return free

def ramfree():
	global telnetClient
	telnetClient.write(b'ramfree \r')
	ramfree = (telnetClient.read_some())
	#TODO: HAndle more than DMPS
	telnetClient.read_until(b"DMPS-300-C>")
	return ramfree

def fn(func):
	global telnetClient
	telnetClient.write(b''+ func + ' \r')
	#TODO: HAndle more than DMPS
	output = telnetClient.read_until(b"DMPS-300-C>")
	return output

### END FUNCTIONS ###

#Change Directory to build dir
projectDir=os.path.abspath(os.getcwd())

#Import data from list
itemList = importList(devType)
print itemList

print "Opening remote session \r"
for i in itemList:
	telnetClient = openTelnet(i[1])
	output = 

#telnetClient=openTelnet()
#assert isTelnetLive() == true

## freespace gate logic
free1=free()
free2=free()
assert free1 == free2 ## Memory is stable, no active operations

## Close active session
telnetClient=closeTelnet()
assert isTelnetLive() == false
print "Remote session closed"