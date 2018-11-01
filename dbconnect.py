import MySQLdb

def connection():
	conn = MySQLdb.connect(host="localhost", user="root", passwd="GuE55/thLs/1492", db="AstralCTF")
	c = conn.cursor()
	return c,conn