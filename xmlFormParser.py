import xml.dom.minidom
import MySQLdb
import MySQLdb.cursors

class xmlFormParser:
	"""
	This is supposed to help me make forms, etc..
	has global variable dom which contains the Document Object Model of the form.  
	Here is an example form:

	<form>
	<processingProgram>attendee10.cgi</processingProgram>
	<toDatabase>GradConf</toDatabase>
	<toTable>Participants10</toTable>
	
	<message>
	<p>
	Thank you for your interest in the Binghamton University Graduate Conference in Algebra and Topology 2010.   
	Please fill out the form below to register for the conference as an attendee.  
	</p>
	<span style="color:red;">* Indicates a required field.</span><br /><br />
	</message>
	
	<hiddenField>
		<toVariable>speaking</toVariable>
		<value>no</value>
	</hiddenField>
	
	<textBox>
		<toVariable>firstName</toVariable>
		<required>required</required>
		<title>First Name</title>
		<value></value>
	</textBox>
	
	<textBox>
		<toVariable>lastName</toVariable>
		<required>required</required>
		<title>Last Name</title>
		<value></value>
	</textBox>
	
	<textBox>
		<toVariable>email</toVariable>
		<required>required</required>
		<title>Email</title>
		<value></value>
	</textBox>
	
	<textBox>
		<toVariable>affiliatedInstitution</toVariable>
		<required>required</required>
		<title>Affiliated Institution</title>
		<value></value>
	</textBox>
	
	<radioButtons>
		<title>Position</title>
		<toVariable>position</toVariable>
		<required>required</required>
		<box>
			<checked></checked>
			<label>Undergraduate Student</label>
			<value>undergraduate</value>
		</box>
		<box>
			<checked>checked</checked>
			<label>Graduate Student</label>
			<value>graduate</value>
		</box>
		<box>
			<checked></checked>
			<label>Post-Doc</label>
			<value>postDoc</value>
		</box>
		<box>
			<checked></checked>
			<label>Faculty</label>
			<value>faculty</value>
		</box>
	</radioButtons>
		
	<checkBoxes>
		<title>Meal Preferences</title>
		<toVariable>mealPreferences</toVariable>
		<required>no</required>
		<box>
			<checked></checked>
			<label>No Preference <span style="color: gray">(I'll eat anything.)</span></label>
			<value>noPreference</value>
		</box>
		<box>
			<checked></checked>
			<label>Vegetarian</label>
			<value>vegetarian</value>
		</box>
		<box>
			<checked></checked>
			<label>Vegan</label>
			<value>vegan</value>
		</box>
		<box>
			<checked></checked>
			<label>Gluten Free</label>
			<value>glutenFree</value>
		</box>
		<box>
			<checked></checked>
			<label>Other <span style="color: gray">Please specify in comments</span></label>
			<value>other</value>
		</box>
	</checkBoxes>
	
	<message>
	<p>Unfortunately, we can no longer take reservations for our banquet.  </p>
	</message>
	
	
	<message>
	<p>
	The next few questions deal with our funding services for you. 
	Under these services, it is possible to receive partial to full travel reimbursement
	and a free hotel room. 
	We have limited resources available for travel funding and our hotel service. 
	Thus we cannot guarantee providing these services for everyone who requests it.  
	To read more about our funding services for you, please visit our <a href="../accommodations.html">accommodations page</a>.  
	</p>
	</message>
	
	<radioButtons>
		<title>Travel Funding</title>
		<toVariable>travelFunding</toVariable>
		<required>no</required>
		<box>
			<checked></checked>
			<label>I would like to be considered for travel funding.</label>
			<value>yes</value>
		</box>
		<box>
			<checked>checked</checked>
			<label>I do not want to be considered for travel funding.  </label>
			<value>no</value>
		</box>
	</radioButtons>
	
	<radioButtons>
		<title>Hotel</title>
		<toVariable>hotel</toVariable>
		<required>no</required>
		<box>
			<checked></checked>
			<label>I would like to be considered for the hotel service.</label>
			<value>yes</value>
		</box>
		<box>
			<checked>checked</checked>
			<label>I will find lodging on my own.</label>
			<value>no</value>
		</box>
	</radioButtons>
	
	<message>
	<p>
	For our hotel service, we have to put two people in each room.  
	If you would like to be considered for the hotel service and you have a specific roommate in mind, 
	then please indicate so below, and we will try to pair you two up.  
	Otherwise, leave the pertinent questions blank and we will assign you a roommate of the same gender,
	if you qualify for the hotel service.  
	Your indicated roommate must be a registered participant of the conference.  
	</p>
	</message>
	
	<textBox>
		<toVariable>roommatesFirstName</toVariable>
		<required>no</required>
		<title>Roommate's First Name</title>
		<value></value>
	</textBox>
		
	<textBox>
		<toVariable>roommatesLastName</toVariable>
		<required>no</required>
		<title>Roommate's Last Name</title>
		<value></value>
	</textBox>
	
	<textBox>
		<toVariable>roommatesEmail</toVariable>
		<required>no</required>
		<title>Roommate's Email</title>
		<value></value>
	</textBox>
	
	<message>
	<p>
	We collect the following information to help us determine if we are meeting our goals in encouraging underrepresented minority participation in the conference, 
	to help determine what grants and funding you may be eligible for, and for statistical purposes in applying for future grants.  
	While it is not required that you fill out these areas, it would help us out a lot.
	 
	</p>
	</message>
	
	
	<radioButtons>
		<title>Gender</title>
		<toVariable>gender</toVariable>
		<required>no</required>
		<box>
			<checked></checked>
			<label>Male</label>
			<value>male</value>
		</box>
		<box>
			<checked></checked>
			<label>Female</label>
			<value>female</value>
		</box>
	</radioButtons>
	
	<checkBoxes>
		<title>Ethnicity</title>
		<toVariable>ethnicity</toVariable>
		<required>no</required>
		<box>
			<checked></checked>
			<label>American Indian or Alaska Native</label>
			<value>americanIndianOrAlaskaNative</value>
		</box>
		<box>
			<checked></checked>
			<label>Asian</label>
			<value>asian</value>
		</box>
		<box>
			<checked></checked>
			<label>Black or African American</label>
			<value>blackOrAfricanAmerican</value>
		</box>
		<box>
			<checked></checked>
			<label>Hispanic or Latino</label>
			<value>hispanicOrLatino</value>
		</box>
		<box>
			<checked></checked>
			<label>White</label>
			<value>white</value>
		</box>
		<box>
			<checked></checked>
			<label>Other <span style="color: gray">Please specify in comments</span></label>
			<value>other</value>
		</box>
	</checkBoxes>
	
	<message>
	<p>
	If you have any additional comments, special needs we should know about, or would like to elaborate on any of the above, then please do so here.  
	</p>
	</message>
	
	<textArea>
		<toVariable>comments</toVariable>
		<required>no</required>
		<title>Comments</title>
		<columns>50</columns>
		<rows>10</rows>
		<value></value>
	</textArea>
	
	<exitMessage>
	<p>
	You have successfully registered as an attendee 
	for the 2010 Binghamton University Graduate Conference in Algebra and Topology.
	If you have any additional questions or comments, then please contact us at gradconf@math.binghamton.edu.  
	</p>
	</exitMessage>
	
	</form>

	Supposing that this form is stored as a string in the variable 'form' then we could have the following program:

	cgiData= cgi.FieldStorage()
	formMaker=xmlFormParser(form, cgiData)
	formMaker.generateInsertPage()
	wnParser=wnparser()
	page+=formMaker.getPage()
	page=wnParser.wrap("../templates/template2.inc",page)
	page=wnParser.conditionalText(page)
	print page

	You may want to start the page with some sort of title, since the form only has a form in it.  
	Though, the wnParser will wrap the page to give it a header and a footer.  

	Please note that this program is intended to process itself.  So this program should be called attendee10.cgi 
	since the processingProgram field, way up top, is attendee10.cgi.
	"""
	def __init__(self, form, rawCgiData={}):
		#maybe I should have some sort of log file to put in here?
		self.dom=xml.dom.minidom.parseString(form)
		self.rawCgiData=rawCgiData
		self.idCounter=0
		# note that you will need to change the next three variables if you are running from a different user
		self.host="mysql.math.binghamton.edu" 
		self.user="ntconfweb" 
		# I know laying out the password here looks like a bad security issue, 
		# but this user only works if it is running from one of the department servers,
		# i.e. if someone is registering for the conference from the web.
		# This is why it is not just some variable in the constructor;
		# we need to make sure that the user is setup correctly.
		self.passwd="ImNotGoingToTellYouMyPasswordSoEasily" 

	def loadForm(self, form):
		"""
		type form = string 
		"""
		self.dom=xml.dom.minidom.parseString(form)

	def validateInsertForm(self):
		"""
		Determins if the given form is without errors.  Throws an exception if it has an error.  
		"""
		#first we check to see that there is a properly formatted form tag
		formNodes=self.dom.getElementsByTagName("form")
		if len(formNodes) is not 1:
			raise xmlFormParserException("No form tag found or more than one found.")
		formNode=formNodes[0]
		#make sure that the form tag hass all of its parts.  
		self.validateTagExistsIsUniqueAndHasText(formNode, "processingProgram")
		self.validateTagExistsIsUniqueAndHasText(formNode, "exitMessage")
		self.validateTagExistsIsUniqueAndHasText(formNode, "toDatabase")
		self.validateTagExistsIsUniqueAndHasText(formNode, "toTable")
		#check to see that all of the parts of the form are properly formatted.  
		self.validateParts(formNode)

	def validateParts(self, formNode):
		#check text tags
		textBoxNodes=formNode.getElementsByTagName("textBox")
		for textBoxNode in textBoxNodes:
			self.validateTextBoxNode(textBoxNode)
		#check text Area tags
		textAreaNodes=formNode.getElementsByTagName("textArea")
		for textAreaNode in textAreaNodes:
			self.validateTextAreaNode(textAreaNode)
		#check checkBoxes tags
		checkBoxesNodes=formNode.getElementsByTagName("checkBoxes")
		for checkBoxesNode in checkBoxesNodes:
			self.validateCheckBoxesNode(checkBoxesNode)
		#check radioButtons tags
		radioButtonsNodes=formNode.getElementsByTagName("radioButtons")
		for radioButtonsNode in radioButtonsNodes:
			self.validateRadioButtonsNode(radioButtonsNode)
		#check hidden tags
		hiddenNodes=formNode.getElementsByTagName("hidden")
		for hiddenNode in hiddenNodes:
			self.validateHiddenNode(hiddenNode)
		#check double check text box tags
		doubleCheckTextBoxNodes=formNode.getElementsByTagName("doubleCheckTextBox")
		for doubleCheckTextBoxNode in doubleCheckTextBoxNodes:
			self.validateDoubleCheckTextBoxNode(doubleCheckTextBoxNode)

	def validateTagExistsIsUniqueAndHasText(self, node, tagName):
		"""
		type node = node
		type tagName = string
		The name says it all.  
		"""
		tagNodes=node.getElementsByTagName(tagName)
		if len(tagNodes) is not 1:
			raise xmlFormParserException("No %s tag found or more than one found" % tagName)
		tagNode=tagNodes[0]
		tagText=self.getHtmlText(tagNode.childNodes).strip()
		if len(tagText) is 0:
			raise xmlFormParserException("No text in tag %s" % tagName)
	
	def validateTagExistsAndIsUnique(self, node, tagName):
		"""
		type node = node
		type tagName = string
		The name says it all.  
		"""
		tagNodes=node.getElementsByTagName(tagName)
		if len(tagNodes) is not 1:
			raise xmlFormParserException("No %s tag found or more than one found" % tagName)
	
	def validateTextBoxNode(self, textBoxNode):
		"""
		Each of these validate methods just checks to make sure that the relevant node has all of its important bits.  
		"""
		self.validateTagExistsIsUniqueAndHasText(textBoxNode, "toVariable")
		self.validateTagExistsIsUniqueAndHasText(textBoxNode, "title")
		self.validateTagExistsIsUniqueAndHasText(textBoxNode, "required")
		self.validateTagExistsAndIsUnique(textBoxNode, "value")

	def validateTextAreaNode(self, textAreaNode):
		self.validateTagExistsIsUniqueAndHasText(textAreaNode, "toVariable")
		self.validateTagExistsIsUniqueAndHasText(textAreaNode, "title")
		self.validateTagExistsIsUniqueAndHasText(textAreaNode, "columns")
		self.validateTagExistsIsUniqueAndHasText(textAreaNode, "rows")
		self.validateTagExistsIsUniqueAndHasText(textAreaNode, "required")
		self.validateTagExistsAndIsUnique(textAreaNode, "value")


	def validateCheckBoxesNode(self, checkBoxesNode):
		self.validateTagExistsIsUniqueAndHasText(checkBoxesNode, "toVariable")
		self.validateTagExistsIsUniqueAndHasText(checkBoxesNode, "required")
		boxNodes=checkBoxesNode.getElementsByTagName("box")
		if len(boxNodes) is 0:
			raise xmlFormParserException("No boxes in a checkBoxes tag")
		for boxNode in boxNodes:
			self.validateTagExistsIsUniqueAndHasText(boxNode, "label")
			self.validateTagExistsIsUniqueAndHasText(boxNode, "value")
			self.validateTagExistsAndIsUnique(boxNode, "checked")

	def validateRadioButtonsNode(self, radioButtonsNode):
		self.validateTagExistsIsUniqueAndHasText(radioButtonsNode, "toVariable")
		self.validateTagExistsIsUniqueAndHasText(radioButtonsNode, "required")
		boxNodes=radioButtonsNode.getElementsByTagName("box")
		if len(boxNodes) is 0:
			raise xmlFormParserException("No boxes in a radioButtons tag")
		for boxNode in boxNodes:
			self.validateTagExistsIsUniqueAndHasText(boxNode, "label")
			self.validateTagExistsIsUniqueAndHasText(boxNode, "value")
			self.validateTagExistsAndIsUnique(boxNode, "checked")

	def validateHiddenNode(self, hiddenNode):
		self.validateTagExistsIsUniqueAndHasText(hiddenNode, "toVariable")
		self.validateTagExistsIsUniqueAndHasText(hiddenNode, "value")

	def validateDoubleCheckTextBoxNode(self, doubleCheckTextBoxNode):
		####
		self.validateTagExistsIsUniqueAndHasText(doubleCheckTextBoxNode, "toVariable")
		self.validateTagExistsIsUniqueAndHasText(doubleCheckTextBoxNode, "required")
		boxNodes=doubleCheckTextBoxNode.getElementsByTagName("box")
		if len(boxNodes) is not 2:
			raise xmlFormParserException("There must be exactly 2 boxes in the doubleCheckTextBox tag.")
		for boxNode in boxNodes:
			self.validateTagExistsIsUniqueAndHasText(boxNode, "title")
			self.validateTagExistsAndIsUnique(boxNode, "value")

	def generateInsertPage(self):
		"""
		The main method to be used for forms whose primary function is to insert a new column into the database.
		"""
		result=""
		#first we see if the form has any errors
		self.validateInsertForm()
		if self.isSubmittedPage():
			result=self.generateSubmittedInsertPage()
		elif self.isErrorPage():
			result=self.generateErrorPage()
		elif self.isFirstViewPage():
			result=self.generateFirstViewPage()
		else:
			raise xmlFormParserException("No page type in generatePage()")		
		self.page=result
	
	def getPage(self):
		"""
		Used to retrieve the page once you have executed generateInsertPage() or, if I ever get around to it, generateUpdatePage()
		"""
		return self.page

	def getHtmlText(self, nodelist):
		"""
		type nodelist = list of nodes.  
		gets text from a message or exit message 
		"""	
		rc = []
		for node in nodelist:
			rc.append(node.toxml())	
		return ''.join(rc)

	def isSubmittedPage(self):
		"""
		Has this page been submitted without error?  Usually the forms should be proccessed by themselves.  
		"""
		if self.isFirstViewPage():
			result= False
		elif self.isErrorPage():
			result=False
		else:
			result=True
		return result

	def isErrorPage(self):
		"""
		Has this page been submitted with an error? One error is not filling in a required field.
		"""
		if self.isARequiredFieldMissing():
			result = True
		elif self.isADoubleCheckTextBoxMissmatched():
			result = True
		else:
			result = False
		return result
	
	def isARequiredFieldMissing(self):
		result=False
		#check to see if any fields have not been submitted which are required 
		requiredNodes=self.dom.getElementsByTagName("required")
		for requiredNode in requiredNodes:
			if self.isRequired(requiredNode):
				nameNode=requiredNode.parentNode.getElementsByTagName("toVariable")[0]
				name=self.getHtmlText(nameNode.childNodes).strip()
				if name not in self.rawCgiData:
					result=True
					break
		return result

	
	
	def isADoubleCheckTextBoxMissmatched(self):
		result=False
		#check to see if any doubleCheckTextBoxes have unmatching enteries
		doubleCheckTextBoxNodes=self.dom.getElementsByTagName("doubleCheckTextBox")
		for doubleCheckTextBoxNode in doubleCheckTextBoxNodes:
			if self.isMissmatchedDoubleCheckTextBoxNode(doubleCheckTextBoxNode):
				result=True
				break
		return result

	def isMissmatchedDoubleCheckTextBoxNode(self, node):
		####
		nameNode=node.getElementsByTagName("toVariable")[0]
		name=self.getHtmlText(nameNode.childNodes).strip()
		#I could use getlist(name) instead to clean up the code.
		valueList=self.rawCgiData.getvalue(name) #is this a list or a string?
		if valueList is None:
			#did they put nothing in either field? Thats Okay.
			result=False
		elif type(valueList) is str:
			#did they only put something in one field? Not Okay.
			result = True
		elif (valueList[0] == valueList[1]):
			#Are the fields eqal? okay
			result = False
		else:
			result = True
		return result

	def isFirstViewPage(self):
		"""
		Is this the first time the user has seen the page?  
		"""
		result=(len(self.rawCgiData)==0)
		return result

	def generateFirstViewPage(self):
		"""
		The first time the page is seen the user will not see error messages, etc.  
		"""
		result = ""
		result+=self.handleForm()
		return result

	def handleForm(self):
		#lets create the form.  
		result=""
		processingProgramNode=self.dom.getElementsByTagName("processingProgram")
		processingProgramName=self.getHtmlText(processingProgramNode[0].childNodes)
		result+="<form action = \"%s\" method=POST>\n" % processingProgramName
		#result+="<div style=\"color:red;\">Required *</div>"
		#this is the important bit here
		result+=self.handleParts()
		result+="<input type=\"submit\" value=\"Submit\">"
		result+="</form>"
		return result

	def handleParts(self):
		result=""
		parts=self.dom.childNodes[0].childNodes
		for part in parts:
			#print part.nodeName
			if part.nodeName == "message":
				result+=self.handleMessage(part)
			elif part.nodeName == "textBox":
				result+=self.handleTextBox(part)
			elif part.nodeName == "textArea":
				result+=self.handleTextArea(part)
			elif part.nodeName == "checkBoxes":
				result+=self.handleCheckBoxes(part)
			elif part.nodeName == "radioButtons":
				result+=self.handleRadioButtons(part)
			elif part.nodeName == "hiddenField":
				result+=self.handleHiddenField(part)
			elif part.nodeName == "doubleCheckTextBox":
				result+=self.handleDoubleCheckTextBox(part)
			else:
				pass
				#it is okay to be here
		return result

	def handleMessage(self, node):
		"""
		All of these handle methods are the same.  It just creates a little bit of html as a string and returns it. 
		"""
		result=self.getHtmlText(node.childNodes)
		return result

	def handleTextBox(self, node):
		#make output string
		result=""
		#add on title
		titleNode=node.getElementsByTagName("title")[0]
		result += self.handleTitle(titleNode)
		#add on input
		nameNode=node.getElementsByTagName("toVariable")[0]
		name=self.getHtmlText(nameNode.childNodes)
		valueNode=node.getElementsByTagName("value")[0]
		value=self.getHtmlText(valueNode.childNodes)
		result += "<input name=\"%s\" value=\"%s\"><br /><br />\n\n" % (name, value)		
		return result

	def handleTextArea(self, node):
		#make output string
		result=""
		#add on title
		titleNode=node.getElementsByTagName("title")[0]
		result += self.handleTitle(titleNode)
		#add on input
		tempDict={}
		nameNode=node.getElementsByTagName("toVariable")[0]
		tempDict["name"]=self.getHtmlText(nameNode.childNodes)
		valueNode=node.getElementsByTagName("value")[0]
		tempDict["value"]=self.getHtmlText(valueNode.childNodes)
		columnsNode=node.getElementsByTagName("columns")[0]
		tempDict["columns"]=self.getHtmlText(columnsNode.childNodes)
		rowsNode=node.getElementsByTagName("rows")[0]
		tempDict["rows"]=self.getHtmlText(rowsNode.childNodes)		
		result += "<textarea rows=\"%(rows)s\" cols=\"%(columns)s\" wrap=\"physical\" name=\"%(name)s\">%(value)s</textarea><br /><br />\n\n" % tempDict		
		return result
	
	def handleCheckBoxes(self, node):
		#make output string
		result=""
		#add title
		titleNode=node.getElementsByTagName("title")[0]
		result += self.handleTitle(titleNode)
		#add on check boxes
		boxes=node.getElementsByTagName("box")
		for box in boxes:
			result += self.handleCheckBox(box)
		result+="<br />\n"
		return result

	def handleCheckBox(self, node):
		#make output string
		result=""
		#make dict temp
		temp={'name':'', 'value':'', 'checked':'', 'label':'', 'boxId':''}
		#make box id
		boxId="checkBoxID" + str(self.idCounter)
		self.idCounter+=1
		temp["boxId"]=boxId
		#name
		nameNode=node.parentNode.getElementsByTagName("toVariable")[0]
		temp["name"]=self.getHtmlText(nameNode.childNodes)
		#value
		valueNode=node.getElementsByTagName("value")[0]
		temp["value"]=self.getHtmlText(valueNode.childNodes)
		#label
		labelNode=node.getElementsByTagName("label")[0]
		temp["label"]=self.getHtmlText(labelNode.childNodes)
		#checked
		checkedNode=node.getElementsByTagName("checked")[0]
		temp["checked"]=self.getHtmlText(checkedNode.childNodes)
		result += "<input type=\"checkbox\" name=\"%(name)s\" value=\"%(value)s\" id=\"%(boxId)s\" %(checked)s >\n" %temp
		result += "<label for=\"%(boxId)s\">%(label)s</label><br />\n" % temp
		return result
	
	def handleRadioButtons(self, node):
		#make output string
		result=""
		#add title
		titleNode=node.getElementsByTagName("title")[0]		
		result += self.handleTitle(titleNode)
		#add on check boxes
		boxes=node.getElementsByTagName("box")
		for box in boxes:
			result += self.handleRadioButton(box)
		result+="<br />\n"
		return result

	def handleRadioButton(self, node):
		#make output string
		result=""
		#make dict temp
		temp={'name':'', 'value':'', 'checked':'', 'label':'', 'boxId':''}
		#make box id
		boxId="radioButtonID" + str(self.idCounter)
		self.idCounter+=1
		temp["boxId"]=boxId
		#name
		nameNode=node.parentNode.getElementsByTagName("toVariable")[0]
		temp["name"]=self.getHtmlText(nameNode.childNodes)
		#value
		valueNode=node.getElementsByTagName("value")[0]
		temp["value"]=self.getHtmlText(valueNode.childNodes)
		#label
		labelNode=node.getElementsByTagName("label")[0]
		temp["label"]=self.getHtmlText(labelNode.childNodes)
		#checked
		checkedNode=node.getElementsByTagName("checked")[0]
		temp["checked"]=self.getHtmlText(checkedNode.childNodes)
		result += "<input type=\"radio\" name=\"%(name)s\" value=\"%(value)s\" id=\"%(boxId)s\" %(checked)s >\n" %temp
		result += "<label for=\"%(boxId)s\">%(label)s</label><br />\n" % temp
		return result
	
	def handleHiddenField(self, node):
		result=""
		#name
		nameNode=node.getElementsByTagName("toVariable")[0]
		name=self.getHtmlText(nameNode.childNodes)
		#value
		valueNode=node.getElementsByTagName("value")[0]
		value=self.getHtmlText(valueNode.childNodes)
		result+="<input type=\"hidden\" name=\"%s\" value=\"%s\">\n" % (name, value)
		return result

	def handleDoubleCheckTextBox(self, node):
		####Lets hope this works
		result=""
		boxes=node.getElementsByTagName("box")
		for box in boxes:
			result += self.handleDoubleCheckTextBoxBox(box)
		result+="<br />\n"		
		return result

	def handleDoubleCheckTextBoxBox(self, node):
		####
		result=""
		#add title
		titleNode=node.getElementsByTagName("title")[0]
		title=self.getHtmlText(titleNode.childNodes)
		reqNode=titleNode.parentNode.parentNode.getElementsByTagName("required")[0]
		if self.isRequired(reqNode):
			result+="<strong>%s:</strong><span style=\"color:red;\">*</span><br />\n" % title
		else:
			result+="<strong>%s:</strong><br />\n" % title
		#get all the other stuff
		nameNode=node.parentNode.getElementsByTagName("toVariable")[0]
		name=self.getHtmlText(nameNode.childNodes)
		valueNode=node.getElementsByTagName("value")[0]
		value=self.getHtmlText(valueNode.childNodes)
		#make the tag
		result += "<input name=\"%s\" value=\"%s\"><br /><br />\n\n" % (name, value)
		return result

	def handleTitle(self, titleNode):
		result=""
		title=self.getHtmlText(titleNode.childNodes)
		reqNode=titleNode.parentNode.getElementsByTagName("required")[0]
		if self.isRequired(reqNode):
			result+="<strong>%s:</strong><span style=\"color:red;\">*</span><br />\n" % title
		else:
			result+="<strong>%s:</strong><br />\n" % title
		return result
	
	def isRequired(self, reqNode):
		result=False
		text=self.getHtmlText(reqNode.childNodes)
		text=text.strip()
		text=text.lower()
		if text == "required" or text == "yes":
			result = True
		return result
	def generateErrorPage(self):
		result=""
		self.generateErrorMessage()
		self.prefilForm()
		result+=self.handleForm()
		return result

	def prefilCgiData(self):
		"""
		sets data from form
		"""
		result={}

	def generateErrorMessage(self):
		"""
		Generates the error message that appears when someone messes up filling out the form.  
		"""
		if len(self.rawCgiData) is not 0:
			if self.isErrorPage():
				errorMessage="<div style=\"color: red;\" ><h4>Error Processing</h4>\n"
				if self.isARequiredFieldMissing():
					errorMessage+="Please fill out the required field(s):\n<ul>"
					variableNodes=self.dom.getElementsByTagName("toVariable")
					for v in variableNodes:
						if v.parentNode.nodeName != "hiddenField":
							variable=self.getHtmlText(v.childNodes)
							variable=variable.strip()
							reqNodes=v.parentNode.getElementsByTagName("required")
							#print reqNodes, v.parentNode.nodeName
							#I make sure in validation that every pertinant tag has a required tag.  
							#varReqDict[variable]=self.isRequired(reqNodes[0])
							if (self.isRequired(reqNodes[0]))and(variable not in self.rawCgiData):
								titleNodes=v.parentNode.getElementsByTagName("title")
								title=self.getHtmlText(titleNodes[0].childNodes).strip()
								errorMessage+="<li>%s</li>" % title
					errorMessage+="</ul>"
				if self.isADoubleCheckTextBoxMissmatched():
					errorMessage+="Please make sure both enteries match for the field(s):\n<ul>"
					doubleCheckTextBoxNodes=self.dom.getElementsByTagName("doubleCheckTextBox")
					for doubleCheckTextBoxNode in doubleCheckTextBoxNodes:
						if self.isMissmatchedDoubleCheckTextBoxNode(doubleCheckTextBoxNode):
							firstDoubleCheckTextBoxNode=doubleCheckTextBoxNode.getElementsByTagName("box")[0]
							titleNodes=firstDoubleCheckTextBoxNode.parentNode.getElementsByTagName("title")
							title=self.getHtmlText(titleNodes[0].childNodes).strip()
							errorMessage+="<li>%s</li>" % title
					errorMessage+="</ul>"

				errorMessage+="</div>"
				formNode=self.dom.getElementsByTagName("form")[0]
				errorMessageNode=self.dom.createElement("message")
				errorMessageDom=xml.dom.minidom.parseString(errorMessage)
				errorMessageNode.appendChild(errorMessageDom.childNodes[0])
				formNode.insertBefore(errorMessageNode,formNode.firstChild)
				

	def prefilForm(self):
		"""
		Prefills the form with the informatio the user had already put in.  Essentially if the user doesn't fill in all
		of the required data, we don't want to just erase everything they had previously done and ask them to redo everything.
		The way this method works is that it fills in the information in the dom that will prefill the information.  After that 
		one only needs to call the handleForm method to fill it up. Every tag should have some required field which allows the 
		creator to prefill some of the areas.  We overide those fields.  
		"""
		for key in self.rawCgiData:
			variableNodes=self.dom.getElementsByTagName("toVariable")
			#what if I have two different tags with the same value for toVariable?
			# is should prevent that in varification
			for variableNode in variableNodes:
				if self.textInNodeEquals(variableNode, key):
					if variableNode.parentNode.nodeName == "textBox":
						self.prefilTextBox(variableNode.parentNode,self.rawCgiData.getvalue(key))
					elif variableNode.parentNode.nodeName == "checkBoxes":
						self.prefilCheckBoxes(variableNode.parentNode,self.rawCgiData.getlist(key))
					elif variableNode.parentNode.nodeName == "textArea":
						self.prefilTextArea(variableNode.parentNode,self.rawCgiData.getvalue(key))
					elif variableNode.parentNode.nodeName == "radioButtons":
						self.prefilRadioButtons(variableNode.parentNode,self.rawCgiData.getvalue(key))
					elif variableNode.parentNode.nodeName == "doubleCheckTextBox":
						self.prefilDoubleCheckTextBox(variableNode.parentNode,self.rawCgiData.getlist(key))
					else:
						#it is okay to be here
						pass
			
	def textInNodeEquals(self, node, text):
		result = False
		nodeText=self.getHtmlText(node.childNodes).strip()
		result=(text==nodeText)
		return result 
	
	def prefilTextBox(self, node, value):
		"""
		These prefill methods all work the same.  They just find the right place to fill in the information in the dom.  
		"""
		valueNode=node.getElementsByTagName("value")[0]
		for childNode in valueNode.childNodes:
			valueNode.removeChild(childNode)
		valueNode.appendChild(self.dom.createTextNode(value))
	
	def prefilCheckBoxes(self, node, valueList):
		valueNodes=node.getElementsByTagName("value")
		checkedNodes=node.getElementsByTagName("checked")
		for anyCheckedNode in checkedNodes:
			for childNode in anyCheckedNode.childNodes:
				#if child node is text node
				anyCheckedNode.removeChild(childNode)
			anyCheckedNode.appendChild(self.dom.createTextNode("no"))
		for valueNode in valueNodes:
			for value in valueList:
				if self.textInNodeEquals(valueNode, value.strip()):
					checkedNode=valueNode.parentNode.getElementsByTagName("checked")[0]
					for childNode in checkedNode.childNodes:
						checkedNode.removeChild(childNode)
					checkedNode.appendChild(self.dom.createTextNode("checked"))
					break
	
	def prefilTextArea(self, node, value):
		valueNode=node.getElementsByTagName("value")[0]
		for childNode in valueNode.childNodes:
			valueNode.removeChild(childNode)
		valueNode.appendChild(self.dom.createTextNode(value))
	
	def prefilRadioButtons(self, node, value):
		valueNodes=node.getElementsByTagName("value")
		checkedNodes=node.getElementsByTagName("checked")
		for anyCheckedNode in checkedNodes:
			for childNode in anyCheckedNode.childNodes:
				anyCheckedNode.removeChild(childNode)
			anyCheckedNode.appendChild(self.dom.createTextNode("no"))
		for valueNode in valueNodes:
			if self.textInNodeEquals(valueNode, value.strip()):
				checkedNode=valueNode.parentNode.getElementsByTagName("checked")[0]
				for childNode in checkedNode.childNodes:
					checkedNode.removeChild(childNode)
				checkedNode.appendChild(self.dom.createTextNode("checked"))
			else:
				pass

	def prefilDoubleCheckTextBox(self, node, value):
		####
		boxNodes=node.getElementsByTagName("box")
		if len(value) == 1:
			valueNode=boxNodes[0].getElementsByTagName("value")[0]
			for childNode in valueNode.childNodes:
				valueNode.removeChild(childNode)
			valueNode.appendChild(self.dom.createTextNode(value[0]))
		elif len(value) == 2:
			valueNode=boxNodes[0].getElementsByTagName("value")[0]
			for childNode in valueNode.childNodes:
				valueNode.removeChild(childNode)
			valueNode.appendChild(self.dom.createTextNode(value[0]))
			valueNode=boxNodes[1].getElementsByTagName("value")[0]
			for childNode in valueNode.childNodes:
				valueNode.removeChild(childNode)
			valueNode.appendChild(self.dom.createTextNode(value[1]))

	def generateSubmittedInsertPage(self):
		"""
		If the form has been submitted and there are no errors, then we can process the information,
		shove it in a database, and show the exit message.  In the future we may want to add a blip here
		about emailing a confirmation message.  Or should we do that on the screening page?
		"""
		result=""
		self.processInsertForm()
		exitMessageNode=self.dom.getElementsByTagName("exitMessage")[0]
		exitMessage=self.getHtmlText(exitMessageNode.childNodes)
		result+=exitMessage
		return result

	def processInsertForm(self):
		"""
		I like this method.  We already have the dom at our disposal so it is easier to proccess the
		information they gave.  This is what submits the information to the database.  
		"""
		#first we create a dictionary variabelValueDict which contains pairs key: value
		#the key is the name of the variable in mysql and the value is the value we want the variable to take on.  
		variableValueDict={}
		toVariableNodes=self.dom.getElementsByTagName("toVariable")
		for toVariableNode in toVariableNodes:
			variableName=self.getHtmlText(toVariableNode.childNodes).strip()
			#we have two cases: if the data was submitted and if it wasn't
			if variableName in self.rawCgiData:
				#we have to treat this case differently because the value 
				#is orriginally a pair of identical enteries of which
				#we want only one.  
				if toVariableNode.parentNode.nodeName == "doubleCheckTextBox":
					variableValueDict[variableName]=self.rawCgiData.getlist(variableName)[0]
				else:
					variableValueDict[variableName]=", ".join(self.rawCgiData.getlist(variableName))
			else:
				variableValueDict[variableName]=""
		#now we use the form to find out what the database and table are
		databaseNode=self.dom.getElementsByTagName("toDatabase")[0]
		databaseName=self.getHtmlText(databaseNode.childNodes).strip()
		tableNode=self.dom.getElementsByTagName("toTable")[0]
		tableName=self.getHtmlText(tableNode.childNodes).strip()
		db =	MySQLdb.connect(\
			host=self.host, 
			user=self.user, 
			passwd=self.passwd, 
			db=databaseName, 
			cursorclass = MySQLdb.cursors.DictCursor)
		chand= db.cursor()
		#now we go through the lengthy process of assembling the query.  
		#The issue is that we want injection protection so our query has 
		#to have a bunch of %s in it.
		variableColumns="("
		valueColumns="("
		#we use the keys to make the query
		keys=variableValueDict.keys()
		#and the values to make the tuple that gets inserted into the query via chand.execute.
		values=variableValueDict.values()  
		variableColumns+=(", ".join(keys))
		variableColumns+=")"
		query="INSERT INTO %s %s VALUES (" % (tableName, variableColumns)
		temp=[]
		#this is where we put in the %s for the injection protection.  
		for v in values:
			temp.append("%s")
		temp2=" , ".join(temp)
		query+=temp2
		query+=")"
		#we finally submit the query		 
		chand.execute(query , tuple(values))
		#and close off the connection
		db.commit()
		chand.close()
		db.close()
	
	#########################
	#all of the update stuff is here. 
	###############################
	
	def validateUpdateForm(self):
		"""
		Determins if the given form is without errors.  Throws an exception if it has an error.  
		"""
		#Done
		#first we check to see that there is a properly formatted form tag
		formNodes=self.dom.getElementsByTagName("form")
		if len(formNodes) is not 1:
			raise xmlFormParserException("No form tag found or more than one found.")
		formNode=formNodes[0]
		#make sure that the form tag has all of its parts.  
		self.validateTagExistsIsUniqueAndHasText(formNode, "processingProgram")
		self.validateTagExistsIsUniqueAndHasText(formNode, "exitMessage")
		self.validateTagExistsIsUniqueAndHasText(formNode, "toDatabase")
		self.validateTagExistsIsUniqueAndHasText(formNode, "toTable")
		self.validateTagExistsIsUniqueAndHasText(formNode, "identifyingVariable")
		self.validateTagExistsIsUniqueAndHasText(formNode, "identifyingValue")
		#check to see that all of the parts of the form are properly formatted.  
		self.validateParts(formNode)


	def generateUpdatePage(self):
		"""
		The main method to be used for forms whose primary function is to update a column in the database.  I never 
		actually got around to writing all of the support functions for this, so DON'T USE THIS METHOD.  
		"""
		#Done
		self.validateUpdateForm()
		result=""
		if self.isSubmittedPage():
			result=self.generateSubmittedUpdatePage()
		elif self.isUpdateErrorPage():
			result=self.generateUpdateErrorPage()
		elif self.isFirstViewPage():
			result=self.generateFirstViewPage()
		elif self.isErrorPage():
			result=self.generateErrorPage()
		else:
			raise xmlFormParserException("No page type in generatePage()")		
		self.page=result

	def generateSubmittedUpdatePage(self):
		#Done
		result=""
		self.processUpdateForm()
		exitMessageNode=self.dom.getElementsByTagName("exitMessage")[0]
		exitMessage=self.getHtmlText(exitMessageNode.childNodes)
		result+=exitMessage
		return result

	def isUpdateErrorPage(self):
		#Done
		result=False
		#now we use the form to find out what the database and table are
		databaseNode=self.dom.getElementsByTagName("toDatabase")[0]
		databaseName=self.getHtmlText(databaseNode.childNodes).strip()
		tableNode=self.dom.getElementsByTagName("toTable")[0]
		tableName=self.getHtmlText(tableNode.childNodes).strip()
		db =	MySQLdb.connect(\
			host=self.host, 
			user=self.user, 
			passwd=self.passwd, 
			db=databaseName, 
			cursorclass = MySQLdb.cursors.DictCursor)
		chand= db.cursor()
		#now we need to see that the identifying information exists and is unique
		identifyingVariableNode=self.dom.getElementsByTagName("identifyingVariable")[0]
		identifyingVariableName=self.getHtmlText(identifyingVariableNode.childNodes).strip()
		identifyingValueNode=self.dom.getElementsByTagName("identifyingValue")[0]
		identifyingValueName=self.getHtmlText(identifyingValueNode.childNodes).strip()
		#make the query
		query="SELECT * FROM %s WHERE %s ='%s'" % (tableName, identifyingVariableName, identifyingValueName)
		#Submit the query
		try:		 
			chand.execute(query)
			rows=chand.fetchall()
			if len(rows) != 1:
				result=True
		except:
			result=True
		#and close off the connection
		db.commit()
		chand.close()
		db.close()		
		return result 
	
	def processUpdateForm(self):
		#Done
		"""
		I like this method.  We already have the dom at our disposal so it is easier to proccess the
		information they gave.  This is what submits the information to the database.  
		"""
		#first we create a dictionary variabelValueDict which contains pairs key: value
		#the key is the name of the variable in mysql and the value is the value we want the variable to take on.  
		variableValueDict={}
		toVariableNodes=self.dom.getElementsByTagName("toVariable")
		for toVariableNode in toVariableNodes:
			variableName=self.getHtmlText(toVariableNode.childNodes).strip()
			#we have two cases: if the data was submitted and if it wasn't
			if variableName in self.rawCgiData:
				#we have to treat this case differently because the value 
				#is orriginally a pair of identical enteries of which
				#we want only one.  
				if toVariableNode.parentNode.nodeName == "doubleCheckTextBox":
					variableValueDict[variableName]=self.rawCgiData.getlist(variableName)[0]
				else:
					variableValueDict[variableName]=", ".join(self.rawCgiData.getlist(variableName))
			else:
				variableValueDict[variableName]=""
		#now we use the form to find out what the database and table are
		databaseNode=self.dom.getElementsByTagName("toDatabase")[0]
		databaseName=self.getHtmlText(databaseNode.childNodes).strip()
		tableNode=self.dom.getElementsByTagName("toTable")[0]
		tableName=self.getHtmlText(tableNode.childNodes).strip()
		#the identifying information
		identifyingVariableNode=self.dom.getElementsByTagName("identifyingVariable")[0]
		identifyingVariableName=self.getHtmlText(identifyingVariableNode.childNodes).strip()
		identifyingValueNode=self.dom.getElementsByTagName("identifyingValue")[0]
		identifyingValueName=self.getHtmlText(identifyingValueNode.childNodes).strip()
		#connect to the database
		db =	MySQLdb.connect(\
			host=self.host, 
			user=self.user, 
			passwd=self.passwd, 
			db=databaseName, 
			cursorclass = MySQLdb.cursors.DictCursor)
		chand= db.cursor()
		#now we go through the lengthy process of assembling the query.  
		#The issue is that we want injection protection so our query has 
		#to have a bunch of %s in it.
		settingPairsList=[]
		for key in variableValueDict:
			settingPair=str(key)+"=%s"
			settingPairsList.append(settingPair)
		settingPairsString=" , ".join(settingPairsList)
		query="UPDATE %s SET %s WHERE %s='%s'" % (tableName, settingPairsString, identifyingVariableName, identifyingValueName)
		values=variableValueDict.values()
		#we finally submit the query		 
		chand.execute(query , tuple(values))
		#and close off the connection
		db.commit()
		chand.close()
		db.close()
		
	def generateUpdateErrorPage(self):
		#Done
		result="""\
		<p>
		We Appologize, but your identifying information does not match any that we have on record,
		or your identifying information is duplicated by someone else.  
		Please contact us to proceed with updating your information.
		</p>
		"""
		#not using##self.generateUpdateErrorMessage()
		#self.prefilForm()
		#result+=self.handleForm()
		return result
	
class xmlFormParserException(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)

# test area

"""
form=\"\"\"\
<form>
<processingProgram>test.cgi</processingProgram>
<toDatabase>GradConf</toDatabase>
<toTable>FakeTable10</toTable>

<message>
	<p>
	I can do decoration in html manually. hi
	</p>
</message>

<textBox>
	<toVariable>firstName</toVariable>
	<title>First Name</title>
	<required>required</required>
	<value></value>
</textBox>

<checkBoxes>
	<title>Position</title>
	<toVariable>position</toVariable>
	<required>required</required>
	<box>
		<checked></checked>
		<label>Super Hero</label>
		<value>superHero</value>
	</box>
	<box>
		<checked>checked</checked>
		<label>Super Villan</label>
		<value>superVillan</value>
	</box>
</checkBoxes>

<radioButtons>
	<title>Alignment</title>
	<toVariable>alighment</toVariable>
	<required>no</required>
	<box>
		<checked></checked>
		<label>Evil</label>
		<value>evil</value>
	</box>
	<box>
		<checked>checked</checked>
		<label>Netural</label>
		<value>netural</value>
	</box>
</radioButtons>

<hiddenField>
	<toVariable>speaking</toVariable>
	<value>no</value>
</hiddenField>

<exitMessage>
	<p>
	You have successfully registered as an attendee 
	for the 2010 Binghamton University Graduate Conference in Algebra and Topology.
	If you have any additional questions or comments, then please contact us at gradconf@math.binghamton.edu.  
	</p>
</exitMessage>

</form>
\"\"\"
cgiInputs={}

pageMaker= xmlFormParser(form, cgiInputs)
pageMaker.generateInsertPage()

print pageMaker.getPage()
"""
