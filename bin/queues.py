#!/usr/bin/env python
import os
import sys
import time
from ConfigParser import SafeConfigParser

config = "/etc/oplog/oplog.cnf"
if os.path.exists(config):
        parser = SafeConfigParser()
        parser.read(config)
else:
        print "No config file found! Please create: %s" % config
        sys.exit(1)

elasticsearch = parser.get('default', 'elasticsearch').strip('"').strip("'")

input = len(sys.argv)
if input < 2:
	usage()
	sys.exit(1)
else:
	qname = sys.argv[1]

from pyelasticsearch import ElasticSearch
es = ElasticSearch(elasticsearch)

try:
	s = es.status('oplog')
except:
	print "Creating index: oplog"
	try:
		s = es.create_index('oplog')
		print "sleeping for 5 to ensure index exists"
		time.sleep(5)
	except:
		print "ERROR: index creation failed!"
		sys.exit()

print "Creating queue: %s" % qname
try:
	es.put_mapping('oplog',qname,{"properties" : { "from" : {"type" : "string", "null_value" : "na"}, "sent" : {"type" : "string", "null_value" : "na"}, "submitted" : {"type" : "date"}, "subject" : {"type" : "string", "null_value" : "na"}, "message" : {"type" : "string", "null_value" : "na"} }})
	print "Created queue with mapping:"
	print es.get_mapping('oplog',qname)
except:
	print "ERROR: queue creation failed!"
