from datetime import datetime

class wnparser:
	"""
	Use this to parse the output of a cgi file as the wn server would.  Currently supports:
	wrappers and conditional text.  This is all based on how the wn server runs
	its parsing.  Use wrap() to wrap the text into a wrapper and conditionalText()
	to parse the conditional text.  
	"""
	def __init__(self):
		#maybe I should have some sort of log file to put in here?
		#maybe I should put in the index.wn or index.cache so that fields work
		pass
	def wrap(self, wrapper, text):
		"""
		type(wrapper) = string
		type(text) = string
		wrapper is the location of the file to be used to wrap text.
		text is the text to be wrapped in the file pointed to by wrapper.
		This is currently very inflexible; the include tag better look exactly
		like <!-- #include --> or it won't work.  
		
		Returns a string which has text wrapped in the the wrapper pointed to
		by wrapper.
		"""
		wFile=open(wrapper, 'rU')
		w=wFile.read()
		wFile.close()
		return w.replace("<!-- #include -->", text, 1)
	def whichIndex(self, temp1,temp2):
		"""
		type(temp1) = int
		type(temp2) = int
		A helper function that I don't think I use anymore.  Just supposed to decide
		which of two indexes comes first and take into account that -1 means it does not exist.
		"""
		temp=-1
		if temp1 is not -1:
			temp=temp1
		elif temp2 is not -1:
			temp=temp2
		elif temp1<=temp2:
			temp=temp1
		elif temp1>temp2:
			temp=temp2
		else:
			raise WNParserErrror("Something went nuts in whichIndex: temp1=%s, temp2=%s" % (temp1,temp2))
		return temp
	def oneStep(self, text , start=0):
		"""
		type(text) = string
		type(start) = int
		A helper function.  
		This function is just supposed to feed into oneIfClause().  It seeks out the first
		appearance of some conditional text which appears after start (including start I think).  
		Once found it will return a tripple which returns the begining index of the conditional tag,
		the end of the conditional tag, and what type of tag it is.  For example, for 
		<!-- #if statement -->
		it returns the index of '<' and the index of '>' in the text.  
		If nothing is found it raises a WNParserError.  Also, it will throw a WNParserError 
		if there is a <!-- nested inside a comment tag.  
		Do not call on this function unless you expect to find something.  
		
		return [begin ,end, "#if"] for <!-- #if statement --> -- 1
		return [begin ,end,, "#elif"] for <!-- #elif statement --> -- 0
		return [begin ,end,, "#else"] for <!-- #else statement --> -- 0
		return [begin ,end,,"#endif"] for <!-- #endif statement --> -- -1
		"""
		#count the number of <!-- so that I don't have to enter into an endless loop.  
		c=text.count("<!--")
		if c is 0:
			raise WNParserError("Unable to find '<!--'")
		temp0=start
		# c is really just an upper bound for the number of conditionals
		for i in range(c):
			#try to find a conditional tag and raise errors if any thing goes funny.  
			temp1=text.find("<!--",temp0)
			if temp1 is -1:
				raise WNParserError("Unable to find '<!--'")
			temp2=text.find("-->",temp1+4)
			if temp2 is -1:
				raise WNParserError("Unable to find '-->'")
			temp3=text.find("#",temp1,temp2)
			#did we find a candidate for a conditional tag?
			if temp3 is -1:
				temp0=temp2+3
			elif text.count("<!--",temp1,temp2) > 1:
				raise WNParserError("There is an <!-- nested inside a <!-- --> at %s" % temp1)
			#if so then we restrict our attention to the inside of this tag
			else:
				#checking for bad formatting
				conditionals=["#if","#elif","#else","#endif"]
				c1=0
				for con in conditionals:
					c1+=text.count(con, temp3,temp2)
				if c1>1:
					raise WNParserErorr("Mal-Formatted conditional: more than one condition.")
				#everything looks good so we try to identify and return the tag
				elif c1 is 1:
					if text.count("#if",temp3,temp2) is 1:
						return [temp1,temp2+2,"#if"]
					elif text.count("#elif",temp3,temp2) is 1:
						return [temp1,temp2+2,"#elif"]
					elif text.count("#else",temp3,temp2) is 1:
						return [temp1,temp2+2,"#else"]
					elif text.count("#endif",temp3,temp2) is 1:
						return [temp1,temp2+2,"#endif"]
				else:
					temp0=temp2+3
		#if we made it out of the for loop without finding anything then something went very wrong.
		raise WNParserError("Cannot find any conditionals")
		
	def oneIfClause(self, text, start=0):
		"""
		type(text)= string
		type(start) = int
		This method trys to make a complete description of the location of the outermost conditional clause:
		<!-- #if statement -->
			conditional text
		<!-- #elif statement -->
			conditional text
		<!-- #elif statement -->
		.
		.
		.
		<!-- #elif statement -->
			conditional text
		<!-- #else statement -->
			conditional text
		<!-- #endif statement -->
		Meaning that if there is another conditinal clause nested inside this one, the function will
		disregard it.  It trys to describe the begining and the end of the conditional tags, so
		usually it will return the positions of the symbols '<' and '>' that encapsulate the 
		conditional <!-- #if statement -->, et c..
		returns a list of lists [[beginings], [ends], [type]] where type is the type of 'conditional':
		#if, #elif, #else, #endif and beginings and ends are lists which correspond to the begining 
		and ends of the clauses.  I'm not so sure that a start will ever be needed but I put it in
		just in case.  The function looks for the first conditional after position start (and including start
		I think) in text.  
		Do not use this function unless you expect to find something as it throws WNParserError's if nothing
		or any incomplete clauses are found.  
		"""
		#count the number if conditional tags in the text so that I don't have to run through an endles while loop
		c=text.count("#if", start)
		c+=text.count("#elif", start)
		c+=text.count("#else", start)
		c+=text.count("#endif", start)
		#check for the first clause
		temp=self.oneStep(text,start)
		#check for bad formatting
		if temp[2] != "#if":#be careful with is
			raise WNParserError("Mal-formatted #if clause Did not find an #if first found '%s'" % temp[2])
		#result is what will get returned in the end
		result=[[temp[0]],[temp[1]],[temp[2]]]
		j=1
		index=temp[1]+1 ##Changed but I think it is okay
		#lets look for the rest of the clauses
		#this method uses an index j to keep track of which if clause it is in, setting j+=1 every time it
		#goes into another if clause and setting j+=-1 whenever it goes out of an if clause
		for i in range(c):
			temp=self.oneStep(text,index)
			if temp[2] == "#if":
				j+=1
			elif (temp[2] == "#elif") or (temp[2] == "#else"):
				if j is 1:
					result[0].append(temp[0])
					result[1].append(temp[1])
					result[2].append(temp[2]) 
			elif temp[2] == "#endif":
				j+=-1
				if j is 0:
					result[0].append(temp[0])
					result[1].append(temp[1])
					result[2].append(temp[2])
					return result
			else:
				raise WNParserError("Magic error: temp[2] has some weird value")
			index=temp[1]+1
				
	def conditionalText(self, text):
		"""
		type(text) = string
		This method searches through text and replaces all conditionals with the appropriate text.  
		Supported conditionals are listed in atomicIsTrue(), and conditionals may be nested.  
		The conditionals may be compound and involve parenthesis.  For example,
		
		'these are words before
		<!-- #if True && True || False && False -->
			I am text that should not appear<br />
			<!-- #if True && True || False && False -->
			Html!!!
			<!-- #endif -->
		<!-- #elif (True && True) || (False && False) -->
			I am text that should appear
			<!-- #if True && True || False && False -->
				text 2
			<!-- #elif True && True -->
				more text
			<!--#endif-->
		<!-- #else -->
			ummm
		<!-- #endif -->
		these are words after
		
		before<!-- #if True -->Text1<!-- #elif True-->Text2<!-- #else -->Text3<!-- #endif -->after'
		
		should return
		
		'these are words before

			I am text that should appear
			
				more text
			
		
		these are words after

		beforeText1after'.
		
		The way this method handles errors is that it just returns the text with the error appended as
		an html comment.  As a side note,  the clauses are evaluate from the outside in.  Even though this
		method is much harder to code, it is the way the logic should go.  
		"""
		#count the number of #endif's so that I don't have to enter an endless loop.  
		#c gives an upperbound on the number of times I will need to itterate through the text.
		c=text.count("#endif")
		for i in range(c):
			#if ther aren't any if loops then we can just call it a day.
			if text.count("#endif") is 0:
				return text
			#otherwise we proceed to try to evaluate the if clauses outside in.  
			else:
				try:
					ifBlock=self.oneIfClause(text)
					k=len(ifBlock[0])
					beginBlock=ifBlock[0][0]
					endBlock=ifBlock[1][k-1]
					for j in range(k):
						#if we see the #endif and it is in the right place...
						if (j == (k-1) ) and (ifBlock[2][j] =="#endif"):
							text=text[:beginBlock]+text[(endBlock+1):]
							break
						#some errors that could occur
						elif j == (k-1):
							raise WNParserError("Mal-Formatted #if clause: #endif is not the last clause")
						elif ifBlock[2][j] =="#endif":
							raise WNParserError("Mal-Formatted #if clause: #endif comes before the last clause")
						elif (j < (k-2)) and (ifBlock[2][j] == "#else"):
							raise WNParserError("Mal-Formatted #if clause: #elif is not the second to last clause")
						##else blocks must be evaluated
						elif (ifBlock[2][j] == "#else") and (j == (k-2)):
							insertion=text[(ifBlock[1][j]+1):ifBlock[0][j+1]]
							text=text[:beginBlock]+insertion+text[(endBlock+1):]
							break
						#we are at an #if or #elif clause and we try to evaluate if it is true.  
						elif self.isTrue(text[ifBlock[0][j]:(ifBlock[1][j])+1]):
							insertion=text[(ifBlock[1][j]+1):ifBlock[0][j+1]]
							text=text[:beginBlock]+insertion+text[(endBlock+1):]
							break
				#whatever just print it.or maybe I should have an error log?  No one will see thiserror.  
				#except WNParserError as exception:
				#	message="<!-- "+str(exception)+" -->"
				#	return text+message
				# somehow wn can't handle the line except WNParserError as exception:
				# but it can handle except:
				# so that is what I am going to do
				except:
					return text+"<!-- An error occured -->"
		#this really shouldn't come up, but just in case
		return text
				
	def atomicIsTrue(self, text):
		"""
		type text = string 
		Put in an atomic condtional like True or after "22 Oct 2009 17:41:26" and 
		it will return if it is true or false.  Raises a WNParserError if you put in something which is
		not an atomic conditional.  Must have exactly one statement to evaluate.  
		Can only evaluate the conditions listed in the tuple conditions.  
		True and False must be capitalized!
		"""
		#Check for proper formatting
		conditions=["after","before","True","False"]
		c=0
		for con in conditions:
			if text.count(con) >1:
				raise WNParserError("Not an atomic conditional: more than one of the same condition '%s'" % con)
			elif text.count(con) is 1:
				c+=1
		if c is not 1:
			raise WNParserError("Not an atomic conditional: more that one different condition or no conditions")
		#check the condition
		if text.count("after") is 1:
			indexAfter=text.find("after")
			temp1=text.find("\"", indexAfter+1)
			temp2=text.rfind("\"", temp1+1)	
			if (temp1 == -1) or (temp2==-1) or (temp1==temp2) or ((temp1+1)==temp2): 
				raise WNParserError("Messed up quotes: after")
			else:
				dtStampString=text[temp1+1:temp2]
				dtStampString=dtStampString.strip()
				dtStamp1=datetime.strptime(dtStampString,"%d %b %Y %X")
				return dtStamp1 <= datetime.now()
		elif text.count("before") is 1:
			indexBefore=text.find("before")
			temp1=text.find("\"", indexBefore+1)
			temp2=text.rfind("\"", temp1+1)
			if (temp1 == -1) or (temp2==-1) or (temp1==temp2) or ((temp1+1)==temp2): 
				raise WNParserError("Messed up quotes: before")
			else:
				dtStampString=text[temp1+1:temp2]
				dtStampString=dtStampString.strip()
				dtStamp1=datetime.strptime(dtStampString,"%d %b %Y %X")
				return dtStamp1 >= datetime.now()
		elif text.count("True") is 1:
			return True
		elif text.count("False") is 1:
			return False
		else:
			raise WNParserError("Some condition is not caught by the 'switch'")
	def withoutParenthesisIsTrue(self, text):
		"""
		type text = string
		Evaluates a compound conditional that involves && and || but no parenthesis.   
		Evaluates the the || first and then the &&.  I forget what this is called.  
		Essentially the following statement evaluates to False:
		True && True || False && False
		because it is read in as True && (True || False) && False.
		"""
		#Split it up and evaluate	
		ands=text.split('&&')
		if len(ands) is 0: 
			raise WNParserError("len(ands)==0")
		finalResult=True
		for a in ands:
			ors=a.split('||')
			result=False
			for o in ors:
				#result or self.atomicIsTrue(o) can cause problems.  Won't eval atomic is true
				result = self.atomicIsTrue(o) or result  
			finalResult=finalResult and result
		return finalResult
		
	def withParenthesisIsTrue(self, text):
		"""
		type text= string
		Takes in a compound conditional statement and evaluates it.  You may use parenthesis fianally.
		Will raise a WNParserError if it is not properly formatted.  The idea in this code is to 
		find the fist occorance of ')' and use that to evaluate the innermost, leftmost parenthesis,
		and then iterate.  
		"""
		#count number of parenthesis and format of parentheses
		if text.count("(") is not text.count(")"):
			raise WNParserError("Mal-formatted parenthesis: unequal number of left and right parenthesis")
		c=text.count("(")
		for i in range(0,c+1):
			right=text.find(")")
			if right is -1:
				return self.withoutParenthesisIsTrue(text)
			left=text.rfind("(",0,right)
			if left is -1:
				raise WNParserError("Mal-formatted parentheses: no '(' to the left of ')'")
			temp1=text[left+1:right]
			temp2=self.withoutParenthesisIsTrue(temp1)
			temp=str(temp2)
			text=text[:left]+temp+text[right+1:]
			
	def isTrue(self, text):
		"""
		type text= string
		This is what you want to use to determin if anything such as <!-- #if statement -->
		is true.  Text  must look like:
		<!-- #if statement --> or
		<!-- #elif statement --> or
		<!-- #else statement -->
		and the statement may be a compound
		conditional with parenthesis.  Must be properly formatted or will raise a WNParserError.  
		"""
		#check for formatting and remove extraneous text
		if text.startswith("<!--") and text.endswith("-->"):
			text=text.replace("<!--","")
			text=text.replace("-->","")
			text=text.strip()
		else:
			raise WNParserError("Mal-Formatted conditional clause: does not begin with <!-- or end in -->: %s" % text)
		starts=["#if","#elif"]#elses do not have conditions
		c=0
		for x in starts:
			c+=text.count(x)
			if text.startswith(x):
				text=text.replace(x,"")
		if c is not 1:
			raise WNParserError("Mal-Formatted conditional clause: no if, elif, else statements or too many of them.")
		# do it
		return self.withParenthesisIsTrue(text)


class WNParserError(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)
		

#text center

#x=wnparser()
#text3=\
"""
 
<html> 
 <head> 
  <title>Binghamton University Graduate Conference in Algebra and Topology 2010</title> 
  <link rel="stylesheet" type="text/css" href="../style.css" /> 
  <link rel="shortcut icon" href="../../pics/confIcon2.ico" type="image/x-icon" /> 
 </head> 
 <body> 
  <span class="header"> 
   <h1>Binghamton University<h1> 
   <h2> Graduate Conference in Algebra and Topology</h2> 
   <div style="font-size:150%" align="center">Coming November 2010</div> 
   <div id="mainNavBar"> 
    <a href="../index.html">HOME</a> | 
    <a href="../contact.html">CONTACT</a> | 
    <a href="../archives.html">ARCHIVES</a> |
    <a href="../registration.html">REGISTRATION</a> 
   </div> 
   <hr> 
  </span> 
<!-- #if True --> 
<!-- Hi from true --> 
<!-- #else --> 
<!-- Hi from not true --> 
<!-- #endif --> 
 
  <h2 align="center">Test Registration</h2><hr><form action = "super.cgi" method=POST> 
<span style="color:red;">Required *</span> 
	<p> 
	I can do decoration in html manually.
	</p> 
<strong>First Name:</strong><span style="color:red;">*</span><br /> 
<input name="firstName" value=""><br /> 
<strong>Position:</strong><span style="color:red;">*</span><br /> 
<input type="checkbox" name="position" value="superHero" id="checkBoxID0"  > 
<label for="checkBoxID0">Super Hero</label><br /> 
<input type="checkbox" name="position" value="superVillan" id="checkBoxID1" checked > 
<label for="checkBoxID1">Super Villan</label><br /> 
<strong>Alignment:</strong><br /> 
<input type="radio" name="alighment" value="evil" id="radioButtonID2"  > 
<label for="radioButtonID2">Evil</label><br /> 
<input type="radio" name="alighment" value="netural" id="radioButtonID3" checked > 
<label for="radioButtonID3">Netural</label><br /> 
<input type="hidden" name="speaking" value="no"> 
<strong>What are your super powers:</strong><span style="color:red;">*</span><br /> 
<textarea rows="10" cols="50" wrap="physical" name="powers"></textarea><br /> 
<input type="submit" value="Submit"></form> 
 
  <span class="footer"> 
  <hr> 
  <p> 
   The 2009 conference was supported by National Science Foundation Grant No. 
   DMS0946269 and several Binghamton University departments and organizations including the Mathematics Department, 
   Office of the Vice President for Research, Convocations Committee, Harpur Dean's Office, and the Graduate School. 
   Any opinions, findings and conclusions or recommendations expressed here are those of the author(s) and do not necessarily 
   reflect the views of the National Science Foundation (NSF) or any other sponsor.
  </p> 
   This webpage was last updated on May 23, 2010.
  <hr> 
  </span> 
 </body> 
</html> 

"""
#print x.conditionalText(text3)
"""
print x.wrap("../templates/template1.inc" , "Look at me I am wrapped\n a lot.")
"""
#print x.atomicIsTrue("<!-- #if after \"22 Oct 2011 17:41:26\" -->")
#print x.withoutParenthesisIsTrue("<!-- #if after \"22 Oct 2009 17:41:26\" && before \"22 Oct 2011 17:41:26\"-->")
#print x.withoutParenthesisIsTrue("<!-- #if True && True || False && False-->")
#print x.withoutParenthesisIsTrue("<!-- #if True && True || False && False -->")
#print x.withoutParenthesisIsTrue("<!-- #if True || False -->")
#print x.isTrue("<!-- #else ((True && True) || (False  && False) ) && (after \"22 Oct 2009 17:41:26\" && before \"04 Jun 2010 09:39:26\")-->")
#print x.isTrue("<!-- #if False -->")
#raise WNParserError("Random error")
#text=\
"""
these are words before
<!-- #if True && True || False && False -->
	I am text that should not appear<br />
	<!-- #if True && True || False && False -->
	Html!!!
	<!-- #endif -->
<!-- #elif (True && True) || (False && False) -->
	I am text that should appear
	<!-- #if True && True || False && False -->
		text 2
	<!-- #elif True && True -->
		more text
	<!--#endif-->
<!-- #else -->
	ummm
<!-- #endif -->
<!-- #endif -->
these are words after
"""
"""
t=x.oneStep(text,67)
print t
for i in range(t[0],t[1]+1):
	print i, "  ", text[i]
"""

#print x.oneIfClause(text)
#print x.conditionalText(text)

#text2=\
"""\
before<!-- #if True -->Text1<!-- #elif True-->Text2<!-- #else -->Text3<!-- #endif -->after
"""
"""
print x.conditionalText(text2)
"""
"""
Maybe split with && and || and process each of the insides


if text.find("#if after") is not -1:
				temp1=text.find("\"")
				temp2=text.rfind("\"")	
				if (temp1 == -1) or (temp2==-1) or (temp1==temp2) or ((temp1+1)==temp2): 
					return False
				else:
					dtStampString=text[temp1+1:temp2]
					dtStampString=dtStampString.strip()
					dtStamp1=datetime.strptime(dtStampString,"%d %b %Y %X")
					return dtStamp1 <= datetime.now()
			elif text.find("#if before") is not -1:
				temp1=text.find("\"")
				temp2=text.rfind("\"")
				if (temp1 == -1) or (temp2==-1) or (temp1==temp2) or ((temp1+1)==temp2): 
					return False
				else:
					dtStampString=text[temp1+1:temp2]
					dtStampString=dtStampString.strip()
					dtStamp1=datetime.strptime(dtStampString,"%d %b %Y %X")
					return dtStamp1 >= datetime.now()
					
					
	if 	(text.startswith("<!-- #if") or text.startswith("<!--#if")) and \
		text.endswith("-->") and \
		text.count("#if")==1:
			if text.startswith("<!-- #if"): 
				text=text.replace("<!-- #if","")
			if text.startswith("<!--#if"): 
				text=text.replace("<!--#if","")
			text=text.replace("-->","")
		elif text.startswith("<!-- #elif") or text.startswith("<!--#elif")) and \
		text.endswith("-->") and \
		text.count("#elif")==1:
			if text.startswith("<!-- #elif"): 
				text=text.replace("<!-- #elif","")
			if text.startswith("<!--#elif"): 
				text=text.replace("<!--#elif","")
			text=text.replace("-->","")
		else:
			raise WNParserError("Mal-formatted if or elif clause")
"""
