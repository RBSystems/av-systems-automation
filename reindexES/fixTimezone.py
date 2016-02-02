#!/usr/bin/env python
#fixTimezone.py
#2016 - Dan Clegg
import sys
import argparse
from elasticsearch import Elasticsearch,RequestsHttpConnection,helpers
import os
from parse import *
import socket
import subprocess
from datetime import datetime,timedelta
from pytz import timezone,utc,zoneinfo

# METHOD 1: Hardcode zones:
#"2016-2-2T15:02:34Z" 
es = Elasticsearch(host='avreports.byu.edu',port='9200')

res = es.get(index="events",doc_type="user",id="AVKkIc8NTOnrL3UbVDlA")
print res
#res = es.search(index="events", doc_type='user',size=1)
#tot=res['hits']['total']
#res = es.search(index="events", doc_type='user',size=tot)

#result = helpers.reindex(es,'events','events_v2')
mtn = timezone('US/Mountain')
utcZone = timezone('UTC')

#get data from all results
hits=res['hits']['hits']

for hit in hits:
	#utc = datetime.strptime('2016-02-02 02:37:21', '%Y-%m-%d %H:%M:%S')
	# Tell the datetime object that it's in UTC time zone since 
	# datetime objects are 'naive' by default

	# Convert time zone
	#timestamp = hit['_source']['timestamp']

#	macAddress = hit['_source']['device']['macAddress']
#	hostname = hit['_source']['device']['hostname']
#	hostname = hostname.strip()
#	building = ""
#	roomNumber = ""
#	floor = ""
#	if (hostname.find("-") > 0):
#		arrHostname = hostname.split('-')
#		building = arrHostname[0].strip()
#		roomNumber = arrHostname[1].strip()
#		floor = roomNumber[0]
#	ipAddress = hit['_source']['device']['ipAddress']
#	description = hit['_source']['device']['description']
	timestamp = hit['_source']['timestamp']
	datetimeparts = timestamp.split('T')
	dt = datetimeparts[0]
	dateparts = datetimeparts.split('-')
	y = dateparts[0]
	mth = dateparts[1]
	d = dateparts[2]

	t = datetimeparts[1]
	t.replace("Z","")
	timeparts = t.split(':')
	h = timeparts[0]
	m = timeparts[1]
	s = timeparts[2]
	
	localdt = datetime(y,mth,d,h,m,s,tzinfo=Mountain)
	print (localdt)
	#(dt.astimezone(UTC))
	#utcTime = timestamp.astimezone(, "%Y-%m-%dT%H:%M:%SZ"))
	#local_tz = utctime.astimezone(mtn)
	#print mytime.strftime("%Y.%m.%d %H:%M:%S")
#	eventType = "user"
#	actionDescription = hit['_source']['actions'][0]['description']
#	actionActor = hit['_source']['actions'][0]['actor']
#
#	coordinates = hit['_source']['room']['coordinates']
#
#	room = building + " " + roomNumber
#	doc = {
#		'device' : {
#			'macAddress' : macAddress,
#			'hostname': hostname,
#			'ipAddress': ipAddress,
#			'description': description
#		},
#		'timestamp': timestamp,
#		'eventType': 'user',
#		'action': {
#			'description': actionDescription,
#			'actor': actionActor
#		},
#		'room' : {
#			'building': building,
#			'roomNumber': roomNumber,
#			'coordinates': coordinates,
#			'room': room,
#			'floor': floor
#		}
#	}
#	innerRes = es.index(index="events",doc_type="user",body=doc)
#	print(innerRes)