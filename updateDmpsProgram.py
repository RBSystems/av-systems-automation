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

tn=telnetlib.Telnet(host)
tn.read_until(b"DMPS-300-C>")  ## IT'S READY TO GO HERE

### FUNCTIONS ###

def testDir(dirToTest):
	tn.write(b'tn.isDir('+dirToTest+')')
	output = (tn.read_some())
	tn.read_until(b"TSW-750>")
	return output



### END FUNCTIONS ###

