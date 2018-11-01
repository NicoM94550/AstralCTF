#IMPORT DEPENDENCIES --- WORKING 10/25/17
import gc
from dbconnect import connection

#Header INFORMATION FOR ALL PAGES --- WORKING 10/25/17
def Header():
	Page_List = [["Homepage","/","main.html","AstralCTF","AstralCTF"],["Register Team","/register","register-team.html","Team Registration","Register a Team"],["Problems","/problems","problems.html","Problems","Problems"],["Scoreboard","/scoreboard","scoreboard.html","Scoreboard","Scoreboard"],["Chat","/chat","chat.html","AstralCTF Chat","Chat"],["Reference Guide","/references","references.html","Reference Guide","Reference Guide"],["About","/about","about.html","About","About AstralCTF"], ["Solved Problems", "solved-problems", "solvedProblems.html", "Solved Problems", "Solved Problems"]]	
	#["Button Name","Link","html filename","Title","Header"]
	return(Page_List) #RETURN LIST OF ALL PAGES TO BE SEEN IN DROPDOWN

#EXTRACT ACTIVE PROBLEMS WORKING --- WORKING 10/25/17
def activeProblems(): #DEPENDS UPON: (getCategories(), MySQL(problems))
	c, conn = connection()
	Categories = getCategories() #GET CATEGORIES
	Active_Problems = {} #CREATE EMPTY DICTIONARY
	for x in Categories: #LOOP THROUGH LIST OF CATEGORIES
		c.execute("SELECT value, problem_hash FROM problems WHERE category = '%s' AND status = 1" % x) #SELECTS ALL ACTIVE PROBLEMS
		Activated_Problems = c.fetchall() #GRAB ACTIVE PROBLEMS STORE IN VARIABLE To_Parse
		Category_Specific_Problems = [] #MAKES EMPTY LIST FOR CATEGORY x
		for i,y in enumerate(Activated_Problems):	#LOOPS THROUGH AND ADDS ACTIVE PROBLEMS TO Category_Specific_Problems IF THE PROBLEM'S CATEGORY IS EQUAL TO x
			if len(y) == 0: #IF EMPTY OBJECT IN LIST THEN SKIP
				pass
			else: #IF NOT EMPTY ADD TO ARRAY
				Category_Specific_Problems.append([z for z in y])
		if len(Category_Specific_Problems) == 0: #IF ARRAY IS EMPTY PASS
			pass
		else: #IF ARRAY NOT EMPTY ADD TO DICTIONARY WITH KEY AS CATEGORY
			Active_Problems[x] = Category_Specific_Problems
	c.close()
	conn.close()
	gc.collect()
	return(Active_Problems) #RETURN DICTIONARY WITH KEYS AS CATEGORY NAMES AND EACH KEY BEING EQUAL TO SAID CATEGORIES' ACTIVE PROBLEMS

def problems(): #DEPEND UPON: (MySQL(problems))
	c, conn = connection()
	c.execute("SELECT name FROM problems") #TO MySQL
	Problems = [x[0] for x in c.fetchall()] #SELECTS ALL PROBLEM name FROM problems AND STORES IN VAR
	c.close()
	conn.close()
	gc.collect()
	return(Problems) #RETURNS ALL PROBLEM name IN LIST

def Error(): #DEPENDS UPON: (NONE)
	Error_Page = "Error_Handler.html" #SETS DEFAULT Error_Page AS "errorHandler.html"
	return(Error_Page) #RETURNS Error_Page

def getCategories(): #DEPENDS UPON : (MySQL(problems))
	c, conn = connection()
	c.execute("SELECT category FROM problems") #TO MySQL
	Categories = [x[0] for x in c.fetchall()] #GRABS ALL category IN problems AND STORES IN VAR 
	c.close()
	conn.close()
	gc.collect()
	Categories = list(set(Categories)) #REMOVES DUPLICATES
	return(Categories) #RETURNS ALL Categories AS A LIST
