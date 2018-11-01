import MySQLdb

def sqlInjectionConnection():
	conn = MySQLdb.connect(host="REDACTED", user="REDACTED", passwd="REDACTED", db="REDACTED")
	c = conn.cursor()
	return c,conn
