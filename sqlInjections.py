import MySQLdb

def sqlInjectionConnection():
	conn = MySQLdb.connect(host="localhost", user="root", passwd="GuE55/thLs/1492", db="sqlInjections")
	c = conn.cursor()
	return c,conn