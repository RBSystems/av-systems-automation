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

res = es.search(index="events_v3", doc_type='user',size=1)
tot=res['hits']['total']
res = es.search(index="events_v3", doc_type='user',size=tot)

#get data from all results
hits=res['hits']['hits']

for hit in hits:
	#print(hit)
	docId = hit['_id']
	innerRes = es.delete(index="events_v3",doc_type="user",id=docId)
	print(innerRes)
