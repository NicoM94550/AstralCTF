#IMPORTING DEPENDENTS
import gc
import random
import MySQLdb

#FOR DATABASE CONNECTIONS
def connection():
	conn = MySQLdb.connect(host="localhost", user="root", passwd="GuE55/thLs/1492", db="AstralCTF")
	c = conn.cursor()
	return c,conn

#GETS PROBLEM NAME
def getName():
	ProblemName = True
	while ProblemName is True:
		try:
			ProblemName = str(raw_input("What is the problem's name?\n..."))
		except Exception:
			print("Please enter a string.")
	return ProblemName

#GETS PROBLEM TEXT
def getText():
	ProblemText = True
	while ProblemText is True:
		try:
			ProblemText = str(raw_input("What is the problem text?\n..."))
		except Exception:
			print("Please enter a string.")
	return ProblemText
	
#GETS PROBLEM ANSWER
def getAnswer():
	ProblemAnswer = True
	while ProblemAnswer is True:
		try:
			ProblemAnswer = str(raw_input("What is the problem's answer?\n..."))
		except Exception:
			print("Please enter a string.")
	return ProblemAnswer
	
#GETS PROBLEM POINT VALUE	
def getValue():
	ProblemPoints = True
	while ProblemPoints is True:
		try:
			ProblemPoints = int(raw_input("What is the problem's point value?\n..."))
		except Exception:
			print("Please enter an integer.")
	return ProblemPoints
		
#GETS PROBLEM CATEGORY
def getCategory():
	ProblemCategory = True
	while ProblemCategory is True:
		try:
			ProblemCategory = str(raw_input("What is the problem's category?\n..."))
		except Exception:
			print("Please enter a string.")
	return ProblemCategory

#GETS UNLOCKS ORDER
def getOrder():
	ProblemUnlock = True
	while ProblemUnlock is True:
		try:
			ProblemUnlock = int(raw_input("What is the problem's unlock level(Integer, 0 automatically unlocks, then 1 and on)?\n..."))
		except Exception:
			print("Please enter an integer.")
	return ProblemUnlock

#CHECKS IF HAS HINT
def hasHint():
	booleanCheck = True
	while booleanCheck is True:
		try:
			HasHint = int(raw_input("Shall this problem have a hint? Yes(1) or no(0).\n..."))
			if HasHint in (0,1):
				booleanCheck = False
			else:
				print("Please enter either (1) for having a hint or (0) for not having a hint.")
		except Exception as e:
			print("Please enter an integer.")
	return HasHint

#IF HAS HINT GETS HINT	
def getHint():
	ProblemHint = True
	while ProblemHint is True:
		try:
			ProblemHint = str(raw_input("What is the problem's hint?\n..."))
		except Exception:
			print("Please enter a string.")
	return ProblemHint

#CHECKS IF HAS FILE + DISPLAY TYPE
def hasFile():
	hasFile = True
	while hasFile is True:
		try:
			hasFile = int(raw_input("Does this problem have an assosciated file, Yes(1) or no(0)?\n..."))
			if hasFile not in (0,1):
				hasFile = True
				print("Please enter either (0) or (1).")
		except Exception:
			print("Please enter an integer.")
	return hasFile

#GETS DISPLAY TYPE
def getDisplay():
	FileDisplay = True
	while FileDisplay is True:
		try:
			FileDisplay = int(raw_input("Should the file be displayed on problem page(0) or be a download link(1)?\n..."))
			if FileDisplay not in (0,1):
				FileDisplay = True
				print("Please enter either (0) or (1).")
		except Exception:
			print("Please enter an integer.")
	return FileDisplay

#GETS FILE NAME
def getFilename():
	FileName = True
	while FileName is True:
		try:
			FileName = str(raw_input("What is the name of the file?\n..."))
			print("Please place %s in THISISWHEREFOLDERWILLBE." % FileName)
		except Exception:
			print("Please enter a string.")
	return FileName

#GET VARIABLES
NAME = getName()
TEXT = getText()
ANSWER = getAnswer()
VALUE = getValue()
CATEGORY = getCategory()
ORDER = getOrder()
HASHINT = hasHint()
if HASHINT == 1:
	HINT = getHint()
else:
	HINT = None
HASFILE = hasFile()
if HASFILE == 1:
	DISPLAY, FILE = getDisplay(), getFilename()
else:
	DISPLAY, FILE = None, None

#USER CHECK
NotChecked = True
while NotChecked:
	print("NAME(1): %s" % NAME)
	print("TEXT(2): %s" % TEXT)
	print("ANSWER(3): %s" % ANSWER)
	print("VALUE(4): %s" % VALUE)
	print("CATEGORY(5): %s" % CATEGORY)
	print("ORDER(6): %s" % ORDER)
	if HINT == None:
		print("HINT(7): NONE")
	else:
		print("HINT(7): %s" % HINT)
	if HASFILE == 0:
		print("HAS-FILE(8): NO FILE")
	else:
		print("HAS-FILE(8): HAS FILE")
	if DISPLAY == 0:
		print("DISPLAY(9): DISPLAYED ON PAGE")
	else:
		print("DISPLAY(9): DOWNLOAD")
	print("FILE(10): %s" % FILE)
	isInt = True
	while isInt:
		try:
			CheckStatus = int(raw_input("If this information seems correct enter (0), otherwise enter the number assosciated with the wrong value(one at a time).\n..."))
			if CheckStatus in (0,1,2,3,4,5,6,7,8,9):
				isInt = False
		except Exception:
			print("Please enter an integer.")
	if CheckStatus == 0:
		NotChecked = False
	elif CheckStatus == 1:
		NAME = getName()
	elif CheckStatus == 2:
		TEXT = getText()
	elif CheckStatus == 3:
		ANSWER = getAnswer()
	elif CheckStatus == 4:
		VALUE = getValue()
	elif CheckStatus == 5:
		CATEGORY = getCategory()
	elif CheckStatus == 6:
		ORDER = getOrder()
	elif CheckStatus == 7:
		HASHINT = hasHint()
		if HASHINT == 1:
			HINT = getHint()
		else:
			HINT = None
	elif CheckStatus == 8:
		HASFILE = hasFile()
		if HASFILE == 1:
			DISPLAY, FILE = getDisplay(), getFilename()
		else:
			DISPLAY, FILE = None, None
	elif CheckStatus == 9:
		DISPLAY = getDisplay()
	elif CheckStatus == 10:
		FILE = getFilename()

#GETS INFORMATION READY FOR DATABASE INJECTION
print("Preparing information...")
DATABASE_NAME = NAME
DATABASE_TEXT = TEXT
DATABASE_ANSWER = ANSWER
DATABASE_VALUE = str(VALUE)
DATABASE_CATEGORY = CATEGORY
DATABASE_ORDER = str(ORDER)
if HINT == None:
	DATABASE_HASHINT = '0'
	DATABASE_HINT = "0"
else:
	DATABASE_HASHINT = '1'
	DATABASE_HINT = HINT
if DISPLAY == None:
	DATABASE_HASFILE = '0'
	DATABASE_DISPLAY = '0'
	DATABASE_FILENAME = "0"
else:
	DATABASE_HASFILE = '1'
	DATABASE_DISPLAY = str(DISPLAY + 1)
	DATABASE_FILENAME = FILE
if DATABASE_ORDER == '0':
	DATABASE_STATUS = '1'
else:
	DATABASE_STATUS = '0'

#MAKES UNIQUE PROBLEM HASH
Alphabet = list("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789")
DATABASE_HASH = ""
for x in range(20):
	DATABASE_HASH += Alphabet[random.randint(0,61)]

#CONNECT TO DATABASE AND INJECT
def INJECT():
	c, conn = connection()
	toExecute = ("INSERT INTO problems (name, text, answer, value, category, problem_order, hint_status, hint, file_status, file_display, file_name, problem_hash, status) VALUES ('" + DATABASE_NAME + "', '" + DATABASE_TEXT + "', '" + DATABASE_ANSWER + "', '" + DATABASE_VALUE + "', '" + DATABASE_CATEGORY + "', '" + DATABASE_ORDER + "', '" + DATABASE_HASHINT + "', '" + DATABASE_HINT + "', '" + DATABASE_HASFILE + "', '" + DATABASE_DISPLAY + "', '" + DATABASE_FILENAME + "', '" + DATABASE_HASH + "', '" + DATABASE_STATUS + "')")
	c.execute(toExecute)
	conn.commit()
	print("Cleaning up...")
	c.close()
	conn.close()
	gc.collect()
	print("Done...")
	return None

INJECT()