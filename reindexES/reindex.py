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

result = helpers.reindex(es,'events','events_v2')

print result