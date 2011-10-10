#!/usr/bin/env python
import SimpleXMLRPCServer, MySQLdb, sys
sys.path.append('/opt/oplog/conf')
import oplog
import opdb

class OplogXML(object):
  # present the last recordID in the database
  def __init__(self):
        import string
        self.python_string = string
  def getlastmsg(self, queue):
	self.dbname = opdb.getdbbyid(queue)
	sql = "select id from %s order by id desc LIMIT 1" % (self.dbname)
	result = opdb.select(sql)
	return result
  def getsubject(self, queue, id):
	self.dbname = opdb.getdbbyid(queue)
	# present the subject for the requested record ID
        sql = "select msgsubject from %s where id = '%s'" % (self.dbname, id)
        result = opdb.select(sql)
        return result
if __name__=='__main__':
  opdb = opdb.opdb()
  server = SimpleXMLRPCServer.CGIXMLRPCRequestHandler()
  server.register_instance(OplogXML())
  server.handle_request()
