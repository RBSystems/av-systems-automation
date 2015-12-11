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
reqVer = "4.3"
upgradeVer = "4.3"

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
crestronExec = "C:\Program Files (x86)\Crestron\Toolbox\Toolbox.exe"
workspace = "C:\automationWorkspace\uploadNewProgram.ctw"
projectDir = os.path.abspath(os.getcwd())
newProjectPath = projectDir + "\\TEC HD v" + upgradeVer + ".spz"
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
	global telnetClient,ver,newProjectPath,projectDir,upgradeVer
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
	newProjectPath = projectDir + "\\TEC HD v" + upgradeVer + ".spz"
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
	print "Copying Manifest \r"
	telnetClient.write(b'copyfile "\SIMPL\~.Manifest" "\USER\~.Manifest" \r')
	output = (telnetClient.read_until(b"DMPS-300-C>"))
	print "Copying TEC HD v4.3.bin \r"
	telnetClient.write(b'copyfile "\SIMPL\TEC HD v4.3.bin" "\USER\TEC HD v4.3.bin" \r')
	output = (telnetClient.read_until(b"DMPS-300-C>"))
	print "Copying TEC HD v4.3.dip \r"
	telnetClient.write(b'copyfile "\SIMPL\TEC HD v4.3.dip" "\USER\TEC HD v4.3.dip" \r')
	output = (telnetClient.read_until(b"DMPS-300-C>"))
	print "Copying TEC HD v4.3.dsc \r"
	telnetClient.write(b'copyfile "\SIMPL\TEC HD v4.3.dsc" "\USER\TEC HD v4.3.dsc" \r')
	output = (telnetClient.read_until(b"DMPS-300-C>"))
	print "Copying TEC HD v4.3.fp2 \r"
	telnetClient.write(b'copyfile "\SIMPL\TEC HD v4.3.fp2" "\USER\TEC HD v4.3.fp2" \r')
	output = (telnetClient.read_until(b"DMPS-300-C>"))
	print "Copying TEC HD v4.3.ird \r"
	telnetClient.write(b'copyfile "\SIMPL\TEC HD v4.3.ird" "\USER\TEC HD v4.3.ird" \r')
	output = (telnetClient.read_until(b"DMPS-300-C>"))
	print "Copying TEC HD v4.3.rte \r"
	telnetClient.write(b'copyfile "\SIMPL\TEC HD v4.3.rte" "\USER\TEC HD v4.3.rte" \r')
	output = (telnetClient.read_until(b"DMPS-300-C>"))
	print "Copying TEC HD v4.3.rvi \r"
	telnetClient.write(b'copyfile "\SIMPL\TEC HD v4.3.rvi" "\USER\TEC HD v4.3.rvi" \r')
	output = (telnetClient.read_until(b"DMPS-300-C>"))
	print "Copying Program_Boot_Data \r"
	telnetClient.write(b'copyfile "\SIMPL\.~Program_Boot_Data" "\USER\.~Program_Boot_Data" \r')
	output = (telnetClient.read_until(b"DMPS-300-C>"))
	output = "Backed up"
	print "Backup complete \r"
	return output

def fn(func):
	global telnetClient
	telnetClient.write(b''+ func + ' \r')
	output = telnetClient.read_until(b"DMPS-300-C>")
	return output

def push(file):
	global telnetClient

def rollUpdate(ip,path):
	global workspace,crestronExec
	import subprocess
	print "Changing to automationWorkspace folder"
	os.chdir("c:\automationWorkspace")
	orig = "uploadNewProgram.txt"
	tmp = ip + "_tmp.txt"
	origIp = "10.6.36.51"
	origPath = "C:\Users\dgclegg\Documents\repos\My TEC HD\TEC HD v4.3.spz"
	print "Updating script file with new IP"
	input = open(orig)
	output = open(tmp, 'w')
	for s in input.xreadlines(  ):
		s = s.replace(origIp,ip)
		s = s.replace(origPath,path)
		output.write(s)
	output.close(  )
	input.close(  )
	subprocess.call(['cp',orig,'orig_bak'])
	print "Overwriting original script with new script file"
	subprocess.call(['mv',tmp,orig])
	subprocess.call([crestronExec,workspace])
	return "Update complete"

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
print "Changing to " + projectDir + "/build \r"
os.chdir(projectDir + "/build")

print "Opening remote session \r"
telnetClient=openTelnet()
assert isTelnetLive() == true

## iptable gate logic
#iptable()

## system info gate logic
#info()

## Version gate logic
version()
print "Running version " + ver
assert ver == reqVer   ## Prerequisite version number met

## freespace gate logic
free1=free()
free2=free()
assert free1 == free2 ## Memory is stable, no active operations

## Move ahead
#print 'moving ahead \r'
#	
##BACKUP STEPS
print "Running backup \r"
bak=backup()
print bak

rollUpdate(host,newProjectPath)

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
print "Remote session closed"