#!/usr/bin/env python
import sys

input = len(sys.argv)
if input < 2:
	usage()
	sys.exit(1)
else:
	qname = sys.argv[1]

from pyelasticsearch import ElasticSearch
sys.path.append('../conf')
import oplog
es = ElasticSearch(oplog.elasticsearch)

try:
	s = es.status('oplog')
except:
	s = es.create_index('oplog')

es.put_mapping('oplog',qname,{"properties" : { "from" : {"type" : "string", "null_value" : "na"}, "sent" : {"type" : "string", "null_value" : "na"}, "submitted" : {"type" : "date"}, "subject" : {"type" : "string", "null_value" : "na"}, "message" : {"type" : "string", "null_value" : "na"} }})

