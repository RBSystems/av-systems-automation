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
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host,port))
s.send('iptable')
data = s.recv(size)
print 'Received: %d',data
s.close()

#dmpsFile = "dmpsAddresses.txt"
#fileToTrans = "dan.txt"

#with open(fname) as f:
#    address = f.readline()
    
