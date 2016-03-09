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

res = es.search(index="events", doc_type='user',size=1)
tot=res['hits']['total']
res = es.search(index="events", doc_type='user',size=tot)

#get data from all results
hits=res['hits']['hits']
print hits

for hit in hits:
	try:
		deviceExists = False
		try:
			actionDescription = hit['_source']['device']
		except:
			deviceExists = False
		else:
			deviceExists = True
		if(deviceExists):
			macAddress = hit['_source']['device']['macAddress']
			hostname = hit['_source']['device']['hostname']
			hostname = hostname.strip()
			ipAddress = hit['_source']['device']['ipAddress']
			description = hit['_source']['device']['description']
		else:
			macAddress = ""
			hostname = ""
			ipAddress = ""
			description = ""
		building = ""
		roomNumber = ""
		floor = ""
		if (hostname.find("-") > 0):
			arrHostname = hostname.split('-')
			building = arrHostname[0].strip()
			roomNumber = arrHostname[1].strip()
			floor = roomNumber[0]
		tsExists = False
		try:
			timestamp = hit['_source']['timestamp']
		except:
			tsExists = False
		else:
			tsExists = True

		if (tsExists):
			timestamp = hit['_source']['timestamp']
		else:
			timestamp = None

		eventType = "user"
		actionsExists = False
		try:
			actionDescription = hit['_source']['actions'][0]['description']
		except:
			actionsExists = False
		else:
			actionsExists = True
		
		if (actionsExists):
			actionDescription = hit['_source']['actions'][0]['description']
			actionActor = hit['_source']['actions'][0]['actor']
		else:
			actionExists = False
			try:
				actionDescription = hit['_source']['action']['description']
			except:
				actionExists = False
			else:
				actionExists = True

			if(actionExists):
				actionDescription = hit['_source']['action']['description']
				actionActor = hit['_source']['action']['actor']
			else:
				actionDescription = None
				actionActor = None
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
		innerRes = es.index(index="events_v7",doc_type="user",body=doc)
		print(innerRes)
	except:
		continue
