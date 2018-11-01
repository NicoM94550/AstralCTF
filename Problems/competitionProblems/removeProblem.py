#FIXES content_management IMPORT ERROR
import sys
sys.path.append("/var/www/FlaskApp/FlaskApp")

#IMPORTING DEPENDENTS
import gc
import random
import MySQLdb
from dbconnect import connection
import gc

#GETS LIST OF PROBLEMS
def getProblems():
	c, conn = connection()
	c.execute("SELECT name FROM problems")
	conn.commit()
	PROBLEMS = [x[0] for x in c.fetchall()]
	c.close()
	conn.close()
	gc.collect()
	return PROBLEMS

PROBLEMS = getProblems()

#USER CHOICE OF PROBLEM TO REMOVE
print ("AstralCTF currently shows the following problems as active:")
for x in PROBLEMS:
	print x
toRemove = True
while toRemove == True:
	try:
		toRemove = str(raw_input("Which problem would you like to remove: "))
		if toRemove not in PROBLEMS:
			print ("Please enter an active problem.")
			toRemove = True
		else:
			pass
	except:
		print ("Please enter a string.")

#REMOVING FROM DATABASE
def removeProblem(PROBLEM):
	print("Removing from database...")
	c, conn = connection()
	c.execute("DELETE FROM problems WHERE name = '%s'" % PROBLEM)
	c.execute("DELETE FROM problems_status WHERE name = '%s'" % PROBLEM)
	conn.commit()
	print("Cleaning up...")
	c.close()
	conn.close()
	gc.collect()
removeProblem(toRemove)