#!/usr/bin/env python
#updateHostnames.py
#2016 - Dan Clegg
import sys
from elasticsearch import Elasticsearch,RequestsHttpConnection,helpers
import os
from parse import *
import socket
import subprocess
import time

es = Elasticsearch(host='avreports.byu.edu',port='9200')

res = es.search(index="events_v2", doc_type='user',size=1)
tot=res['hits']['total']
res = es.search(index="events_v2", doc_type='user',size=tot)

#result = helpers.reindex(es,'events','events_v2')

#print result

#get data from all results
hits=res['hits']['hits']

for hit in hits:
	#print(hit)
	macAddress = hit['_source']['device']['macAddress']
	hostname = hit['_source']['device']['hostname']
	hostname = hostname.strip()
	building = ""
	roomNumber = ""
	floor = ""
	if (hostname.find("-") > 0):
		arrHostname = hostname.split('-')
		building = arrHostname[0].strip()
		roomNumber = arrHostname[1].strip()
		floor = roomNumber[0]
	ipAddress = hit['_source']['device']['ipAddress']
	description = hit['_source']['device']['description']
	timestamp = hit['_source']['timestamp']
	eventType = "user"
	actionDescription = hit['_source']['actions'][0]['description']
	actionActor = hit['_source']['actions'][0]['actor']

	coordinates = hit['_source']['room']['coordinates']

	room = building + " " + roomNumber
	doc = {
		'device' : {
			'macAddress' : macAddress,
			'hostname': hostname,
			'ipAddress': ipAddress,
			'description': description
		},
		'timestamp': timestamp,
		'eventType': 'user',
		'action': {
			'description': actionDescription,
			'actor': actionActor
		},
		'room' : {
			'building': building,
			'roomNumber': roomNumber,
			'coordinates': coordinates,
			'room': room,
			'floor': floor
		}
	}
	innerRes = es.index(index="events_v3",doc_type="user",body=doc)
	print(innerRes)
