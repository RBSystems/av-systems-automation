#!/usr/bin/env python
#updateHostnames.py
#2016 - Dan Clegg
import sys
import argparse
from elasticsearch import Elasticsearch,RequestsHttpConnection,helpers
import os
from parse import *
import socket
import subprocess
import time

rNum = ''
newCoords = ''

parser = argparse.ArgumentParser()
parser.add_argument('--coordinates', help='Specify new lon,lat for the room')
parser.add_argument('--room', help='i.e.\'ITB 1010\'')
args = parser.parse_args()

if args.room:
	rNum = args.room
else:
	print('You must specify a room\r')
	exit(1)

roomSplit = rNum.split(" ")
assert(len(roomSplit) == 2)
bldg = roomSplit[0]
rm = roomSplit[1]

if args.coordinates:
	newCoords = args.coordinates
else:
	print('You must specify coordinates\r')
	exit(1)

coordsArr = newCoords.split(',')
assert (len(coordsArr) == 2)

#coord1 = int(coordsArr[0])
#coord2 = int(coordsArr[1])

#qry = 'room.building: \"' + bldg + '\" room.roomNumber: \"' + rm + '\"'
qry = 'ITB'
es = Elasticsearch(host='avreports.byu.edu',port='9200')
res = es.search(index='configuration', q=qry)
#print (res)
#get data from all results
hits=res['hits']['hits']
for hit in hits:
	configId = hit['_id']
	print(configId)
#	hostname = hit['_source']['hostname']
#	hostname = hostname.strip()
#	building = hit['_source']['room']['building']
#	roomNumber = hit['_source']['room']['roomNumber']
#	floor = hit['_source']['room']['floor']
#	ipAddress = hit['_source']['ipconfig']['ip']
#	mask = hit['_source']['ipconfig']['mask']
#	gateway = hit['_source']['ipconfig']['gateway']
#	macaddress = hit['_source']['ipconfig']['macaddress']
#	dns = hit['_source']['ipconfig']['dns']
#	
#	doc = {
#		'deviceType': 'CP',
#		'hostname': hostname,
#		'description': '',
#		'ipconfig': {
#			'ip': ipAddress,
#			'mask': mask,
#			'gateway': gateway,
#			'macaddress': macaddress,
#			'dns': ['10.8.0.26', '10.8.0.19']
#		},
#		'room': {
#			'building': building,
#			'roomNumber': roomNumber,
#			'coordinates': [coord1, coord2],
#			'floor': floor
#		},
#		'serial': '',
#		'ICN': ''
#	}
#	innerRes = es.index(index='configuration',doc_type='cp',id=body=doc)
###	print(innerRes)
###