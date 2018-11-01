#FIXES content_management IMPORT ERROR
import sys
sys.path.append("/var/www/FlaskApp/FlaskApp")

import subprocess
import json
import random
from pprint import pprint
from content_management import problems
from dbconnect import connection
import gc

#USED LATER TO CLEAN JSONFILES
index = 0

#ALPHABET AND NUMBERS FOR HASH GENERATION
alphabet = list("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789")

#GET ALL PROBLEM NAMES THAT ARE ALREADY IN DB
Problems = problems()

#GETS NAMES OF ALL JSON FILES IN CURRENT WORKING DIRECTORY
jsonFiles = subprocess.check_output("ls *.json", stderr=subprocess.STDOUT, shell=True).split("\n")[:-1]

#REMOVE ANY INCOMPLETE JSON FILES
while index < len(jsonFiles):
	try:
		with open(jsonFiles[index]) as currentFile:
			fileData = json.load(currentFile)
			if fileData["name"] == "":
				del jsonFiles[index]
			else:
				index += 1
	except:
		del jsonFiles[index]

#REMOVES ANY ALREADY ADDED PROBLEMS
jsonFiles = [File for File in jsonFiles if File.strip(".json") not in Problems and json.load(open(File))["name"] not in Problems]

#IF NO FILES AVAILABLE TO ADD EXIT
if len(jsonFiles) == 0:
	print("There are no suitable files to be added at this time.")
	sys.exit()

#GET HIGHEST UNLOCK ORDER CURRENTLY ACTIVE
c, conn = connection()
c.execute("SELECT problem_order FROM problems WHERE status = 1")
try:
	highestUnlockActive = sorted(c.fetchall())[-1][0]
except:
	highestUnlockActive = 0

#IF NONE LEFT TO UNLOCK AUTOMATICALLY UNLOCK NEXT LOWEST
if int(c.execute("SELECT name FROM problems_status WHERE completion_status = 0")) == 0:
	lowestUnlock = sorted([json.load(open(File))["problem_order"] for File in jsonFiles])[0]
else:
	lowestUnlock = -1
conn.close()
c.close()
gc.collect()

#HASH GENERATION FOR PROBLEM
def generateHash():
	hash = ""
	for x in range(20):
		hash += alphabet[random.randint(0,61)]
	return hash
	
#GET TYPE OF PROBLEM ADDITION
def getAdditionType():
	while(1):
		try:
			addType = ["Single","Total"][int(raw_input("Would you like to enter one new problem(0) or every problem in the current working directory(1)?\n"))]
			break
		except:
			print ("Please enter either (0) for a single addition or (1) for a sweeping addition.")
	return addType


#GET NAME OF PROBLEM TO ADD IF SINGLE
def getProblemName():
	while(1):
		print ("Files currently suitable to be added to the database:")
		for filename in jsonFiles:
			print (filename.replace(".json",""))
		problemChoice = str(raw_input("Which file is to be added to the database?\n")) + ".json"
		if problemChoice not in jsonFiles:
			print ("Please enter one of the files listed above.")
		else:
			break
	return problemChoice

#VERIFY IF SWEEPING ADDITION
def verifySweeping():
	try:
		if (int(raw_input("You have chosen to add all available problems to the database. Are you sure you want to continue? Enter (1) to confirm or (0) to deny.\n"))):
			fileChoice = jsonFiles
		else:
			sys.exit()
	except Exception:
		if Exception == "SystemExit":
			sys.exit()
		else:
			print ("Please enter either (1) to confirm or (0) to deny.")
	return None

#ADD A SINGLE CHOSEN PROBLEM
def addSingle(fileToAdd):
	with open(fileToAdd) as File:
		Data = json.load(File)
	name = Data["name"]
	text = Data["text"]
	answer = Data["answer"]
	value = Data["value"]
	category = Data["category"]
	problem_order = Data["problem_order"]
	hint_status = Data["hint_status"]
	hint = Data["hint"]
	file_status = Data["file_status"]
	file_display = Data["file_display"]
	file_name = Data["file_name"]
	if problem_order <= highestUnlockActive:
		status = 1
	else:
		status = 0
	c, conn = connection()
	c.execute("""INSERT INTO problems (name,text,answer,value,category,problem_order,problem_hash,hint_status,hint,file_status,file_display,file_name, status) VALUES ("%s","%s","%s",%s,"%s",%s,"%s",%s,"%s",%s,"%s","%s",%s)""" % (name,text,answer,value,category,problem_order,generateHash(),hint_status,hint,file_status,file_display,file_name,status))
	conn.commit()
	conn.close()
	c.close()
	gc.collect()
	print ("Problem successfully linked with database.")
	return None
	
#ADD ALL AVAILABLE PROBLEMS
def addAll():
	c, conn = connection()
	for currentFile in jsonFiles:
		with open(currentFile) as File:
			Data = json.load(File)
		name = Data["name"]
		text = Data["text"]
		answer = Data["answer"]
		value = Data["value"]
		category = Data["category"]
		problem_order = Data["problem_order"]
		hint_status = Data["hint_status"]
		hint = Data["hint"]
		file_status = Data["file_status"]
		file_display = Data["file_display"]
		file_name = Data["file_name"]
		if (problem_order <= highestUnlockActive) or (problem_order == lowestUnlock):
			status = 1
		else:
			status = 0
		c.execute("""INSERT INTO problems (name,text,answer,value,category,problem_order,problem_hash,hint_status,hint,file_status,file_display,file_name, status) VALUES ("%s","%s","%s",%s,"%s",%s,"%s",%s,"%s",%s,"%s","%s",%s)""" % (name,text,answer,value,category,problem_order,generateHash(),hint_status,hint,file_status,file_display,file_name,status))
		conn.commit()
	conn.close()
	c.close()
	gc.collect()
	print ("Problems successfully linked with database.")
	return None
	
#EXECUTE
def main():
	addType = getAdditionType()
	if addType == "Single":
		toAdd = getProblemName()
		addSingle(toAdd)
	else:
		verifySweeping()
		addAll()

main()
