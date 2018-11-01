from flask import Flask, render_template, request, url_for, redirect, flash, request
from content_management import Header
from content_management import activeProblems
from content_management import Error
from content_management import problems as Problems
from dbconnect import connection
from sqlInjections import sqlInjectionConnection
from MySQLdb import escape_string as thwart
from wtforms import Form, TextField, IntegerField, PasswordField, BooleanField, validators
from passlib.hash import sha256_crypt
from datetime import datetime
from send_sms import sendMessage
from Scoreboard import scoreboardMake
from getHTML import getHeadline
import gc
import os

Page_List = Header()
Error_Page = Error()

app = Flask(__name__)

@app.route('/index')	#PREVENTS INDEXING
def indexPage():
	return render_template(Error_Page, Page_List = Page_List)

#DO NOT TURN ON
"""
@app.route('/sql-injection', methods = ['POST', 'GET'])
def sqlInjection():
	#try:
	injectResults = None
	form = sqlInjectionForm(request.form)
	if ((request.method == 'POST') and (form.validate())):
		userSearch = str(form.search.data)
		c, conn = sqlInjectionConnection()
		sqlSearch = c.execute(("SELECT name, price FROM products WHERE name LIKE '{}%'").format(userSearch))
		if (int(sqlSearch) >= 1):
			conn.commit()
			injectResults = c.fetchall()
			injectResults = [[result[0], str(result[1])] for result in injectResults]
			return render_template("sqlInjection.html", form = form, title = "SQL Injection Testing", header = "SQL Injection Testing", pageList = Page_List, injectResults = injectResults, )
		else:
			return render_template("sqlInjection.html", form = form, title = "SQL Injection Testing", header = "SQL Injection Testing", pageList = Page_List, injectResults = injectResults, )
	else:
		return render_template("sqlInjection.html", form = form, title = "SQL Injection Testing", header = "SQL Injection Testing", pageList = Page_List, injectResults = injectResults, )
	#except Exception as exception:
	#	return render_template(Error_Page, Error_Type = exception, Page_List = Page_List)
"""

@app.route('/chat', methods = ['GET', 'POST'])
def chatPage():
	try:
		error = None
		Content = None
		Form = chatPage(request.form)
		if request.method == "POST" and Form.validate():
			Message = str(Form.Message.data)
			Team_Hash = Form.Team_Hash.data
			c, conn = connection()
			x = c.execute("SELECT * FROM teams WHERE hash = '%s' AND hash_status = '0'" % thwart(Team_Hash))
			if int(x) == 1:
				conn.commit()
				Team_Data = c.fetchall()
				Team_Name = Team_Data[0][0]
				Time = str(datetime.now())
				c.execute("INSERT INTO messages (team,message,time) VALUES ('%s','%s','%s')" % (Team_Name, thwart(Message), Time))
				conn.commit()
				c.close()
				conn.close()
				gc.collect()
				if len(Message.split("@admin")) > 1:
					sendMessage(Message)
			else:
				error = ("That team does not exist!")
		c, conn = connection()
		c.execute("SELECT * FROM messages")
		conn.commit()
		Content = c.fetchall()
		c.close()
		conn.close()
		gc.collect()
		return render_template(Page_List[4][2], Page_List = Page_List, CONTENT = Content, Title = Page_List[4][3], Header = Page_List[4][4], Form = Form, error = error)
	except Exception as e:
		return render_template(Error_Page, Page_List = Page_List)

class sqlInjectionForm(Form):
		search = TextField("", [validators.Length(min=0, max=1000)])

class chatPage(Form):
		Message = TextField("Message", [validators.Length(min=0, max=200)])
		Team_Hash = PasswordField("Hash", [validators.Length(min=10, max=10)])

class RegistrationForm(Form):
		attempted_hash = PasswordField("Hash", [validators.Length(min=10, max=10)])
		team_name = TextField("Team Name", [validators.Length(min=1, max=20)])
		captain_firstname = TextField("Captain's Firstname", [validators.Length(min=1, max=20)])
		captain_lastname = TextField("Captain's Lastname", [validators.Length(min=1, max=20)])
		accept_tos = BooleanField("I promise that I will not use any knowledge gained from this competition for malicious purposes and that I will play fair without intterupting the experience of others.")

class AddHash(Form):
		hashtoadd = TextField("Hash to Add", [validators.Length(min=10, max=10)])
		admin = PasswordField("Admin Password")

class PrintTables(Form):
		admin = PasswordField("Admin Password")

class AnswerProblem(Form):
		teamHash = PasswordField("Team Hash", [validators.Length(min=10,max=10)])
		answer = PasswordField("Answer")

#HOMEPAGE --- WORKING 10/25/17
@app.route(Page_List[0][1])
def homepage():
	try:
		return render_template(Page_List[0][2],Page_List = Page_List, Title = Page_List[0][3], Header = Page_List[0][4])
	except Exception as e:
		return render_template(Error_Page, Page_List = Page_List)

#REGISTER PAGE --- WORKING 10/25/17
@app.route(Page_List[1][1], methods = ['GET', 'POST'])
def registerteam():
	try:
		form = RegistrationForm(request.form)
		if request.method == "POST" and form.validate():
			attempted_hash =  form.attempted_hash.data
			team_name = form.team_name.data
			captain_firstname = form.captain_firstname.data
			captain_lastname = form.captain_lastname.data
			c, conn = connection()
			x = c.execute("SELECT * FROM teams WHERE hash = '%s' AND hash_status = 1" % thwart(attempted_hash))
			conn.commit()
			c.close()
			conn.close()
			gc.collect()
			if int(x) == 0:
				error = ("That hash is either invalid or has been used. Please try again.")
				return render_template(Page_List[1][2], Page_List = Page_List, Title = Page_List[1][3], Header = Page_List[1][4], form = form, error = error)
			else:
				c, conn = connection()
				x = c.execute("SELECT * FROM teams WHERE teamname = '%s'" % thwart(team_name))
				y = c.execute("SELECT * FROM teams WHERE captain_firstname = '"+thwart(captain_firstname)+"' AND captain_lastname = '"+thwart(captain_lastname)+"'")
				conn.commit()
				c.close()
				conn.close()
				gc.collect()
				if int(x) == 0 and int(y) == 0:
					c, conn = connection()
					c.execute("UPDATE teams SET hash_status = 0 WHERE hash = '%s'" % thwart(attempted_hash))
					conn.commit()
					c.execute("UPDATE teams SET teamname = '%s', captain_firstname = '%s', captain_lastname = '%s' WHERE hash = '%s'" % (thwart(team_name), thwart(captain_firstname), thwart(captain_lastname), thwart(attempted_hash)))
					conn.commit()
					c.close()
					conn.close()
					gc.collect()
					error = ("Thank you for registering your team! Best of luck.")
					scoreboardMake()
				elif int(x) > 0:
					error = ("Team already exists!")
				elif int(y) > 0:
					error = (captain_firstname + " " + captain_lastname + " is already a captain!")
				return render_template(Page_List[1][2], Page_List = Page_List, Title = Page_List[1][3], Header = Page_List[1][4], form = form, error = error)
		return render_template(Page_List[1][2], Page_List = Page_List, Title = Page_List[1][3], Header = Page_List[1][4], form = form)
	except Exception as e:
		return render_template(Error_Page, Page_List = Page_List)
#INDIVIDUAL PROBLEM PAGE --- WORKING 10/26/17
@app.route('/problems/<problem>', methods = ['GET', 'POST'])
def problemPage(problem):
	try:
		error = None
		c, conn = connection()
		c.execute("SELECT name, text, answer, value, problem_order, hint_status, file_status, file_display, file_name FROM problems WHERE problem_hash = '%s'" % problem)
		ProblemData = c.fetchall()[0]
		ProblemName = ProblemData[0]
		ProblemText = ProblemData[1]
		ProblemAnswer = ProblemData[2]
		ProblemPoints = ProblemData[3]
		ProblemOrder = ProblemData[4]
		HasHint = ProblemData[5]
		hasFile = ProblemData[6]	#RETURNS 1 IF THE PROBLEM HAS AN ASSOSCIATED FILE OR FILES
		###
		if hasFile == 1:	#IF IT DOES HAVE A FILE OR FILES TO DISPLAY OR LINK
			fileDisplay = ProblemData[7]	#"0/1/0/0/" WHERE EACH VALUE SEPERATED BY A "/" IS FOR A DIFFERENT FILE AND WITH "0" DENOTING A PICTURE TO BE DISPLAYED AND "1" DENOTING A DOWNLOAD LINK
			fileName = ProblemData[8]		#"photoOne.jpg/file.tar/photoTwo.png/photoThree.tif" WHERE EACH VALUE SEPERATED BY A "/" IS FOR A DIFFERENT FILE AND WHICH CORRESPONDS TO A GIVEN fileDisplay VALUE
			fileDisplay = [x for x in fileDisplay.split("/")[:-1]]		#SPLITS fileDisplay BY "/" AND BREAKS INTO ARRAY EXCLUDING LAST VALUE WHICH IS EMPTY SPACE
			fileName = [x for x in fileName.split("/")[:-1]]		#EQUIVALENT TO ABOVE LINE BUT PARSES OUT FILE NAMES
			fileDisplay = fileDisplay[0:len(fileName)]		#ENSURE EQUAL LENGTH
			fileName = fileName[0:len(fileDisplay)]			#ENSURE EQUAL LENGTH
		else:		#IF PROBLEM DOES NOT HAVE ANY FILES
			fileDisplay = []		#EMPTY AS NO FILES NEEDED
			fileName = []			#EMPTY AS NO FILES NEEDED

		numberOfFiles = len(fileDisplay)
		###
		form = AnswerProblem(request.form)
		Hint = ("/problems/%s/hint" % problem)
		if request.method == "POST" and form.validate():
			Team_Hash =  form.teamHash.data
			Team_Answer = form.answer.data
			if Team_Answer != ProblemAnswer:
				error = ("That is not the right answer!")
				return render_template("problemPage.html", Page_List = Page_List, HasHint = HasHint, Title = ProblemName, Link = problem, form = form, ProblemText = ProblemText, error = error, PROBLEMS = Page_List[2], HINT = Hint, hasFile = hasFile, fileDisplay = fileDisplay, fileName = fileName, numberOfFiles = numberOfFiles)
			elif Team_Answer == ProblemAnswer:
				teamExists = int(c.execute("SELECT * FROM teams WHERE hash = '%s' AND hash_status = 0" % thwart(Team_Hash)))
				if teamExists == 0:
					error = "Team does not exist!"
					return render_template("problemPage.html", Page_List = Page_List, HasHint = HasHint, Title = ProblemName, Link = problem, form = form, ProblemText = ProblemText, error = error, PROBLEMS = Page_List[2], HINT = Hint, hasFile = hasFile, fileDisplay = fileDisplay, fileName = fileName, numberOfFiles = numberOfFiles)
				completionStatus = int(c.execute("SELECT * FROM problems_status WHERE name = '%s' AND hash = '%s' AND completion_status = 0" % (ProblemName, thwart(Team_Hash))))
				problemCompletionStatus = int(c.execute("SELECT * FROM problems_status WHERE name = '%s' AND completion_status = 1" % ProblemName))
				c.execute("SELECT name FROM problems WHERE name != '%s' AND problem_order = %s" % (ProblemName, ProblemOrder))
				conn.commit()
				problemsInOrder = c.fetchall()
				orderCompletionStatus = 0
				if len(problemsInOrder) == 0:
					pass
				else:
					for individualProblem in problemsInOrder:
						if int(c.execute("SELECT * FROM problems_status WHERE name = '%s' AND completion_status = 1" % individualProblem)) == 0:
							orderCompletionStatus = 1
							break
				if completionStatus == 1:
					c.execute("UPDATE problems_status SET completion_status = 1 WHERE name = '%s' AND hash = '%s'" % (ProblemName, thwart(Team_Hash)))
					conn.commit()
					if (problemCompletionStatus == 0) and (orderCompletionStatus == 0):
						if int(c.execute("SELECT problem_order, problem_hash FROM problems WHERE problem_order > %s" % ProblemOrder)) != 0:
							conn.commit()
							Make_Order = sorted([x for x in c.fetchall()])[0][0]
							c.execute("UPDATE problems SET status = 1 WHERE problem_order = %s" % Make_Order)
							conn.commit()
					c.execute("UPDATE teams SET points = (points + %s) WHERE hash = '%s'" % (ProblemPoints, thwart(Team_Hash)))
					conn.commit()
					error = ("Points Awarded!")
					scoreboardMake()
				elif completionStatus == 0:
					error = ("Points have already been awarded to this team.")
				c.close()
				conn.close()
				gc.collect()
				return render_template("problemPage.html", Page_List = Page_List, HasHint = HasHint, Title = ProblemName, Link = problem, form = form, ProblemText = ProblemText, error = error, PROBLEMS = Page_List[2], HINT = Hint, hasFile = hasFile, fileDisplay = fileDisplay, fileName = fileName, numberOfFiles = numberOfFiles)
		c.close()
		conn.close()
		gc.collect()
		return render_template("problemPage.html", Page_List = Page_List, HasHint = HasHint, Title = ProblemName, Link = problem, form = form, ProblemText = ProblemText, error = error, PROBLEMS = Page_List[2], HINT = Hint, hasFile = hasFile, fileDisplay = fileDisplay, fileName = fileName, numberOfFiles = numberOfFiles)
	except Exception as e:
		return render_template(Error_Page, Error_Type = e, Page_List = Page_List)
#HINT PAGE FOR INDIVIDUAL PROBLEMS --- WORKING 10/26/17
@app.route('/problems/<Problem_Given>/hint', methods = ['POST', 'GET'])
def Hint(Problem_Given):
	try:
		error = None
		c, conn = connection()
		Problem = "/problems/%s" % Problem_Given
		c.execute("SELECT name,hint FROM problems WHERE problem_hash = '%s'" % Problem_Given)
		conn.commit()
		Problem, Problem_Hint = c.fetchall()[0][0:2]
		if Problem_Hint == '0':
			Problem_Hint = ("This problem has no hint!")
		Problem_Link = ("http://162.243.159.89/problems/%s" % (Problem_Given))
		c.close()
		conn.close()
		gc.collect()
		return render_template('Hint.html', Problem = Problem, Hint = Problem_Hint, Page_List = Page_List, Problem_Link = Problem_Link)
	except Exception as e:
		return render_template(Error_Page, Page_List = Page_List)

#ALL PROBLEMS PAGE --- WORKING 10/25/17
@app.route(Page_List[2][1])
def problems():
	try:
		Active_Problems = activeProblems()
		return render_template(Page_List[2][2], Page_List = Page_List, Active_Problems = Active_Problems, Title = Page_List[2][3], Header = Page_List[2][4])
	except Exception as e:
		return render_template(Error_Page, Error_Type = e, Page_List = Page_List)

@app.route(Page_List[3][1])
def scoreboard():
	try:
		return render_template(Page_List[3][2], Page_List = Page_List, Title = Page_List[3][3], Header = Page_List[3][4])
	except Exception as e:
		return render_template(Error_Page, Page_List = Page_List)

@app.route(Page_List[5][1])
def references():
	try:
		return render_template(Page_List[5][2], Page_List = Page_List, Title = Page_List[5][3], Header = Page_List[5][4])
	except Exception as e:
		return render_template(Error_Page, Page_List = Page_List)

@app.route(Page_List[6][1])
def about():
	try:
		return render_template(Page_List[6][2], Page_List = Page_List, Title = Page_List[6][3], Header = Page_List[6][4])
	except Exception as e:
		return render_template(Error_Page, Page_List = Page_List)

@app.errorhandler(404)
def page_not_found(e):
	try:
		return render_template(Error_Page, Page_List = Page_List)
	except Exception as e:
		return render_template(Error_Page, Page_List = Page_List)

@app.route('/admin')
def adminpanel():
	try:
		return render_template('adminpanel.html', Page_List = Page_List)
	except Exception as e:
		return render_template(Error_Page, Page_List = Page_List)

@app.route('/admin/addhash', methods = ['GET', 'POST'])
def addhash():
	try:
		error = None
		form = AddHash(request.form)
		if request.method == "POST" and form.validate():
			hashtoadd =  form.hashtoadd.data
			enteredpassword = sha256_crypt.encrypt(str(form.admin.data))
			adminPassword = open("/var/www/FlaskApp/FlaskApp/admin.txt",'r').read().replace("\n","")
			if sha256_crypt.verify(adminPassword,enteredpassword):
				c, conn = connection()
				if int(c.execute("SELECT * FROM teams WHERE hash = '%s'" % thwart(hashtoadd))) > 0:
					conn.close()
					gc.collect()
					error = "Hash already in use!"
					return render_template('addhash.html', Page_List = Page_List, form = form, error = error)
				c.execute("INSERT INTO teams (hash) VALUES ('%s')" % thwart(hashtoadd))
				conn.commit()
				for problem in Problems():
					c.execute("INSERT INTO problems_status (name, hash) VALUES ('%s', '%s')" % (problem, thwart(hashtoadd)))
					conn.commit()
				c.close()
				conn.close()
				gc.collect()
				error = ("Hash added.")
				return render_template('addhash.html', Page_List = Page_List, form = form, error = error)
			else:
				error = ("Invalid password.")
				return render_template('addhash.html', Page_List = Page_List, form = form, error = error)
		return render_template('addhash.html', Page_List = Page_List, form = form, error = error)
	except Exception as e:
		return render_template(Error_Page, Error_Type = e, Page_List = Page_List )

@app.route('/admin/printtables', methods = ['GET', 'POST'])
def printtables():
	try:
		error = None
		form = PrintTables(request.form)
		if request.method == "POST" and form.validate():
			enteredpassword = sha256_crypt.encrypt(str(form.admin.data))
			adminPassword = open("/var/www/FlaskApp/FlaskApp/admin.txt",'r').read().replace("\n","")
			if sha256_crypt.verify(adminPassword,enteredpassword):
				c, conn = connection()
				c.execute("SELECT * FROM problems")
				conn.commit()
				problems = c.fetchall()
				c.execute("SELECT * FROM teams")
				conn.commit()
				teams = c.fetchall()
				c.execute("SELECT * FROM problems_status")
				conn.commit()
				problems_status = c.fetchall()
				c.execute("SELECT * FROM messages")
				conn.commit()
				messages = c.fetchall()
				c.close()
				conn.close()
				gc.collect()
				error = [problems, teams, problems_status, messages]
				return render_template('printtables.html', Page_List = Page_List, form = form, error = error)
			else:
				error = ("Invalid password.")
				return render_template('printtables.html', Page_List = Page_List, form = form, error = error)
		return render_template('printtables.html', Page_List = Page_List, form = form, error = error)
	except Exception as e:
		return render_template(Error_Page, Page_List = Page_List)

if __name__ == "__main__":
	app.run()
