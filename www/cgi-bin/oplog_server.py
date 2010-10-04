#!/usr/bin/env python
import SimpleXMLRPCServer, MySQLdb, sys
sys.path.append('/opt/oplog/conf')
import oplog

class StringFunction(object):
  # present the last recordID in the database
  def getanswer(self, resnum):
	curs = conn.cursor()
	sql = "select recordid from maillogs order by recordid desc LIMIT " + resnum
	curs.execute(sql)
	result = curs.fetchall()
	return result
  def getsubject(self, recordid):
	# present the subject for the requested record ID
        curs = conn.cursor()
        sql = "select msgsubject from maillogs  where recordid = '" + recordid + "'"
        curs.execute(sql)
        result = curs.fetchall()
        return result
  def __init__(self):
	import string
	self.python_string = string
if __name__=='__main__':
  server = SimpleXMLRPCServer.CGIXMLRPCRequestHandler()
  if oplog.db_port == "3306":
     conn = MySQLdb.connect(host=oplog.db_host, user=oplog.db_username, passwd=oplog.db_password, db=oplog.db_name)
  else:
     conn = MySQLdb.connect(host=oplog.db_host, port=oplog.db_port, user=oplog.db_username, passwd=oplog.db_password, db=oplog.db_name)
  server.register_instance(StringFunction())
  server.handle_request()
