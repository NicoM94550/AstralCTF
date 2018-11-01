import MySQLdb

def connection():
	conn = MySQLdb.connect(host="REDACTED", user="REDACTED", passwd="REDACTED", db="REDACTED")
	c = conn.cursor()
	return c,conn
