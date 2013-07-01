#!/usr/bin/env python
import sys
import json
from bottle import route, run, get, abort, post, request, template
from pyelasticsearch import ElasticSearch
from datetime import date, timedelta

# Leaving these for examples for now
# listdate = strftime("%Y-%m-%d", localtime())
# sentdate = strftime("%a, %d %b %Y", localtime())

d=date.today()

sys.path.append('../conf')
import oplog

es = ElasticSearch(oplog.elasticsearch)

@route('/')
def typelist():
	res = []
	for i in es.get_mapping(index='oplog')['oplog']:
		res.append(i)
	return template('typelist', res=res)

@route('/queue/:q')
def showqueue(q, showdate=d):
	n = showdate+timedelta(days=1)
	query = {
   		"query" : {
      			"filtered" : {
        			"query" : {
            				"match_all" : {}
         			},
         		"filter" : {
            			"numeric_range" : {
               				"submitted" : {
                  				"lt" : n,
                  				"gte" : showdate
               					}
            				}
         			}
      			}
   		},
		"from": 0,
		"size": 50,
		"sort": [
			{ "submitted" : {"order" : "desc"} }
		],
		"facets": {}
	}	
	x = es.search(query, index='oplog', doc_type=q)
        return template('showqueue',  res=x)

run(host='0.0.0.0', port=8080, debug=True)
