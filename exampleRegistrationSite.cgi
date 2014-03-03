#!/usr/bin/python
"""
name: exampleRegistrationSite.cgi
usage: People that are to attend should use this page to register for the conference.   
"""
print "Content-Type: text/html\n\n"
import cgitb
cgitb.enable()
import sys
#sys.path.append("../scripts")
from xmlFormParser import xmlFormParser
from wnparser import wnparser
import cgi


#below is the XML data used to create the webpage and process the submitted data.  
form="""\
<form>
<processingProgram>exampleRegistrationSite.cgi</processingProgram>
<toDatabase>exampleDatabase</toDatabase>
<toTable>exampleTable</toTable>

<message>
	<h2><center>Application for Registration</center></h2>
	<hr />
	<p>
	Thank you for your interest in the Third Annual Upstate New York Number 
	Theory Conference. Applications for contributed talks and for attending
	the conference will be open until April 19th.  
	Please fill out the form below to submit your application.


	</p>
	<span style="color:red;">* Indicates a required field.</span><br /><br />
</message>

<textBox>
	<toVariable>firstName</toVariable>
	<title>First Name</title>
	<required>required</required>
	<value></value>
</textBox>

<textBox>
	<toVariable>lastName</toVariable>
	<title>Last Name</title>
	<required>required</required>
	<value></value>
</textBox>

<doubleCheckTextBox>
	<toVariable>email</toVariable>
	<required>required</required>
	<box>
		<title>Email</title>
		<value></value>
	</box>
	<box>
		<title>Re-Enter Email</title>
		<value></value>
	</box>
</doubleCheckTextBox>

<textBox>
	<toVariable>institution</toVariable>
	<title>Affiliated Institution</title>
	<required>required</required>
	<value></value>
</textBox>

<radioButtons>
	<title>Position</title>
	<toVariable>title</toVariable>
	<required>required</required>
	<box>
		<checked>checked</checked>
		<label>Student</label>
		<value>student</value>
	</box>
	<box>
		<checked></checked>
		<label>Post-Doc</label>
		<value>postDoc</value>
	</box>
	<box>
		<checked></checked>
		<label>Junior Researcher</label>
		<value>juniorResearcher</value>
	</box>
	<box>
		<checked></checked>
		<label>Senior Researcher</label>
		<value>seniorResearcher</value>
	</box>
</radioButtons>

<radioButtons>
	<title>Would you like to give a contributed talk?</title>
	<toVariable>wantsToTalk</toVariable>
	<required>required</required>
	<box>
		<checked></checked>
		<label>Yes</label>
		<value>yes</value>
	</box>
	<box>
		<checked>checked</checked>
		<label>No</label>
		<value>no</value>
	</box>
</radioButtons>

<message>
        <hr />
	<h3>
	 Students, Post-Docs, and Junior Researchers
	</h3>
	<p>
	If you are a student, post-doc or junior researcher, then please fill out the following.  
	If you are a <b>student</b> and you are requesting funding, 
	then please ask your adviser to write a brief (doesn't have to be more than a paragraph) recommendation and send it to us at ntconf@math.binghamton.edu.
	</p>
</message>

<radioButtons>
	<title>Are you requesting funding?</title>
	<toVariable>requestsFunding</toVariable>
	<required>no</required>
	<box>
		<checked></checked>
		<label>Yes</label>
		<value>yes</value>
	</box>
	<box>
		<checked>checked</checked>
		<label>No</label>
		<value>no</value>
	</box>
</radioButtons>

<message>
  <p>
  <b>If you are requesting funding</b>, then please carefully answer the following questions.  We will let you know as soon as possible what portion of your travel costs will be covered.
  </p>
</message>

<textBox>
	<toVariable>travellingFrom</toVariable>
	<title>Where are you travelling from?</title>
	<required>no</required>
	<value></value>
</textBox>

<textBox>
	<toVariable>carTravelDistance</toVariable>
	<title>If you are travelling by a non-rental car then how many miles will you be travelling?  <span style="color:grey;">(Please be as specific as possible.)</span></title>
	<required>no</required>
	<value></value>
</textBox>

<textBox>
	<toVariable>travellingWith</toVariable>
	<title>If you are travelling by a non-rental car then who will you be travelling with?</title>
	<required>no</required>
	<value></value>
</textBox>

<textArea>
	<toVariable>freeFormTravel</toVariable>
	<required>no</required>
	<title>If you are travelling by another method, how will you be getting to the conference?  With whom will you be travelling?  Please estimate the cost per person.</title>
	<columns>50</columns>
	<rows>10</rows>
	<value></value>
</textArea>

<message>
	<hr />
	<h3>
		Students
	</h3>
	<p>
	If you are a student, then please fill out the following.  
	</p>
</message>

<textBox>
	<toVariable>phdYear</toVariable>
	<title>What year do you expect to complete your Ph.D.?</title>
	<required>no</required>
	<value></value>
</textBox>

<textBox>
	<toVariable>adviserFirstName</toVariable>
	<title>Adviser's First Name</title>
	<required>no</required>
	<value></value>
</textBox>

<textBox>
	<toVariable>adviserLastName</toVariable>
	<title>Adviser's Last Name</title>
	<required>no</required>
	<value></value>
</textBox>

<doubleCheckTextBox>
	<toVariable>adviserEmail</toVariable>
	<required>no</required>
	<box>
		<title>Adviser's Email</title>
		<value></value>
	</box>
	<box>
		<title>Re-Enter Adviser's Email</title>
		<value></value>
	</box>
</doubleCheckTextBox>

<message>
	<hr />
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
	Thank you for applying to register for the 
	Third Annual Upstate New York Number Theory Conference.
	If you do not receive email confirming your application for registration within the next few days, 
	or if you have any additional questions or comments, 
	then please contact us at
	ntconf@math.binghamton.edu.  
	</p>
</exitMessage>

<message>
<p>
For questions, please contact ntconf@math.binghamton.edu.
</p>
</message>

</form>
"""

cgiData= cgi.FieldStorage()
formMaker=xmlFormParser(form, cgiData)
formMaker.generateInsertPage()
wnParser=wnparser()
page=""
page+=formMaker.getPage()

page=wnParser.wrap("exampleWrapper.inc", page)
page=wnParser.conditionalText(page)
print page




