#LOADS DEPENDENCIES
from dbconnect import connection
from content_management import problems
from warnings import filterwarnings
import MySQLdb
import random
import gc
import os

#SUPPRESS WARNINGS
filterwarnings('ignore', category = MySQLdb.Warning)

#LOADING REQUIRED VARIABLES
Alphabet = list("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789")


#INITIAL-SETUP/RESET COMPETITION
def resetCompetition():
	c, conn = connection()
	c.execute("CREATE TABLE IF NOT EXISTS teams (teamname VARCHAR(50) DEFAULT '', captain_firstname VARCHAR(50) DEFAULT '', captain_lastname VARCHAR(50) DEFAULT '', hash VARCHAR(10), hash_status INT(1) DEFAULT 1, points INT(10) DEFAULT 0)")
	conn.commit()
	c.execute("CREATE TABLE IF NOT EXISTS problems (name VARCHAR(100), text VARCHAR(50000), answer VARCHAR(100), value INT(10), category VARCHAR(100), problem_order  INT(10), hint_status INT(1) DEFAULT 0, hint VARCHAR(500) DEFAULT '', file_status INT(1) DEFAULT 0, file_display VARCHAR(100) DEFAULT 0, file_name VARCHAR(1000) DEFAULT '', problem_hash VARCHAR(100), status INT(1) DEFAULT 0)")
	conn.commit()
	c.execute("CREATE TABLE IF NOT EXISTS problems_status (name VARCHAR(100) , hash VARCHAR(10000), completion_status INT(1) DEFAULT 0)")
	conn.commit()
	c.execute("CREATE TABLE IF NOT EXISTS messages (team VARCHAR(50), message VARCHAR(5000), time VARCHAR(100))")
	conn.commit()
	c.execute("DELETE FROM teams")
	conn.commit()
	c.execute("DELETE FROM problems_status")
	conn.commit()

	#MORE REQUIRED VARIABLES
	Problems = problems()

	ifDelete = True
	while ifDelete is True:
		try:
			ifDelete = int(raw_input("Should the messages be deleted(0) or saved(1)?\n..."))
			if ifDelete not in (0,1):
				ifDelete = True
				print("Please enter either (0) or (1).")
			if ifDelete == 0:
				c.execute("DELETE FROM messages")
				conn.commit()
			elif ifDelete ==1:
				c.execute("SELECT * FROM messages")
				conn.commit()
				toSave = c.fetchall()
				toSave = '\n'.join([':'.join(x) for x in toSave])
				File = open('MessageHistory.txt','a+')
				File.write(toSave)
				File.close()
				print("All messages saved to 'MessageHistory.txt'")
				c.execute("DELETE FROM messages")
				conn.commit()
		except Exception:
			print("Please enter an integer.")
	c.execute("UPDATE problems SET status = DEFAULT")
	conn.commit()
	c.execute("UPDATE problems SET status = (1) WHERE problem_order = (0)")
	conn.commit()
	Competitors = True
	while Competitors is True:
		try:
			Competitors = int(raw_input("How many new teams(hashes)?\n..."))
		except Exception:
			print("Please enter an integer.")
	Hashes = []
	for x in range(Competitors):
		toAdd = ""
		for i in range(10):
			toAdd += Alphabet[random.randint(0,61)]
		Hashes.append(toAdd)
	for x in Hashes:
		c.execute("INSERT INTO teams(hash) VALUES ('%s')" % x)
		conn.commit()
	for x in Problems:
		for y in Hashes:
			c.execute("INSERT INTO problems_status(name, hash) VALUES('%s', '%s')" % (x, y))
			conn.commit()
	return Hashes
	c.close()
	conn.close()
	gc.collect()

#INITIATES RESET
Hashes = resetCompetition()

#DEEP FRIED
os.system("cp /var/www/FlaskApp/FlaskApp/static/images/deepFried.png /var/www/FlaskApp/FlaskApp/static/images/currentScoreboard.png")

#RESET SERVER
os.system("service apache2 restart")

#PRINTS USER HASHES
print("Your team hashes are(also stored in HASHES.txt):")
File = open("HASHES.txt","w+")
for x in Hashes:
	print x
	File.write(x + "\n")
File.close()
