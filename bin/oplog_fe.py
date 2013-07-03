#!/usr/bin/env python
import sys
import os
import json
from ConfigParser import SafeConfigParser
from pyelasticsearch import ElasticSearch
from datetime import date, timedelta, datetime

d=date.today()

config = "/etc/oplog/oplog.cnf"
if os.path.exists(config):
	parser = SafeConfigParser()
	parser.read(config)
else:
	print "No config file found! Please create: %s" % config
	sys.exit(1)

# this needs to move to /etc/oplog or something
oproot = '/var/www/wsgi/OpLog'
opconfdir = "%s/conf" % (oproot)
sys.path.append(opconfdir)
import oplog

# Change working directory so relative paths (and template lookup) work again
opbindir = "%s/bin" % (oproot)
root = os.path.join(opbindir)
sys.path.insert(0, root)

es = ElasticSearch(oplog.elasticsearch)

from bottle import route, run, get, abort, post, request, template, redirect, default_app, debug, TEMPLATE_PATH

TEMPLATE_PATH.insert(0,opbindir + "/views")

@route('/')
def typelist():
	x = []
	try:
		for i in es.get_mapping(index='oplog')['oplog']:
			x.append(i)
	except:
		return "ERROR: you haven't set up any queues yet!"
		sys.exit()
	# if there's only one queue, skip the queues list for /
	if len(x) == 1:
		qname = "/oplog/%s" % (x[0])
		redirect(qname)
	else:
		return template('typelist', res=x)

@route('/<q>')
@route('/<q>/<sdate>')
@route('/<q>/<sdate>/<fcount>')
def showqueue(q, sdate=d, fcount=0):
	if type(sdate) is str:
		sdate = datetime.strptime(sdate, "%Y-%m-%d")
	qt = []
        for i in es.get_mapping(index='oplog')['oplog']:
                qt.append(i)
	edate = sdate+timedelta(days=1)
	pdate = sdate-timedelta(days=1)
	query = {
   		"query" : {
      			"filtered" : {
        			"query" : {
            				"match_all" : {}
         			},
         		"filter" : {
            			"numeric_range" : {
               				"submitted" : {
                  				"lt" : edate,
                  				"gte" : sdate
               					}
            				}
         			}
      			}
   		},
		"from": int(fcount),
		"size": 50,
		"sort": [
			{ "submitted" : {"order" : "desc"} }
		],
		"facets": {}
	}	
	if sdate == d:
		shownext = 'F'
	else:
		shownext = 'T'
	dates = [ str(pdate).split()[0], str(d), str(edate).split()[0], shownext ]
	w = [ q, len(qt)]
	x = es.search(query, index='oplog', doc_type=q)
	y = [ w, x, dates, fcount ]
        return template('showqueue',  res=y)

#run(host='0.0.0.0', port=8080, debug=True)
debug(True)
application = default_app()
