import os
import sys
import pyzmail
import imapclient
import pprint
from credentials import originEmail, password, destinationEmail
import smtplib
import datetime
import html2text

#Setting up dynamic variables for search criteria
numericalMonthStringDict = {1:'Jan'}

#Get current date
now = datetime.datetime.now()

for key, value in numericalMonthStringDict.items():
	if now.month == key:
		month = value

dynamicDate = '%d-%s-%d' %(now.day, month, now.year)

#searchParameter = "(ON \"%d-%s-%d\")" %(now.day, month, now.year)

#print ('searchParameter is ' + searchParameter)


#Trying out IMAP to retrieve emails
imapObj = imapclient.IMAPClient('imap-mail.outlook.com', ssl=True)

#Selecting UIDs of emails - setting criteria
#UIDs = imapObj.search('(ON "15-Jan-2019")')

#logging in imap object
imapObj.login(originEmail, password)

### ACDB1 SET
##Selecting folder to read files from
#imapObj.select_folder('INBOX/Pusher.py/ACDB1', readonly=True)
###Selecting UIDs of emails - setting criteria
#UIDs = imapObj.search('(FROM dwopr@AUSVACDODB02.activant.com)') 

### DEV SET
##Selecting folder to read files from
imapObj.select_folder('INBOX/Pusher.py/DEV', readonly=True)
###Selecting UIDs of emails - setting criteria
UIDs = imapObj.search('(FROM dwopr@ausxeptdmo02.activant.com)') 



##Printing UIDs of emails
print (UIDs)
##Fetching emails
fetched = imapObj.fetch(UIDs,  ['BODY[]'])
i = 0
for element in UIDs:
	message = pyzmail.PyzMessage.factory(fetched[element][b'BODY[]'])
	bodyText = ''
	bodyOfPusherEmails = (message.text_part.get_payload().decode(message.text_part.charset))
	for word in bodyOfPusherEmails.split():
		#print ('word is: ' + word)
		if 'RTN:0' in word:
			#Nothing went wrong here
			bodyText +=str(word)
			break
		elif 'RTN:1' in word:
			#Send an email saying that it broke	
			bodyText +=str(word)
			i += 1
			print ("Error number %d  "%i)
			print ('Subject: %r' % (message.get_subject(), ))
			print ('From: %r' % (message.get_address('from'), ))
			print ('To: %r' % (message.get_addresses('to'), ))
			print ('Cc: %r' % (message.get_addresses('cc'), ))
			print('\n')
			print('LOG MESSAGE')
			print (bodyText)
			print('\n')
		else:
			bodyText +=str(word)

#
###UIDs to use [5350, 5354, 5360, 5367, 5371, 5378]
##[538, 540, 542, 544, 546, 548, 550, 552, 554, 556, 558]
#message = pyzmail.PyzMessage.factory(fetched[556][b'BODY[]'])
##
#print (message.get_subject())
#
#print (message.get_addresses('from'))
#
#print (message.get_addresses('to'))



##THIS PART READS AN INDIVIDUAL EMAIL BODY AND DETECTS WHEN RTN IS BESIDES 0
#bodyOfPusherEmails = (message.text_part.get_payload().decode(message.text_part.charset))
#
#for word in bodyOfPusherEmails.split():
	#print ('word is: ' + word)
	#if 'RTN:0' in word:
	#	print ('It went fine')
	#else:
	#	#Send an email saying that it broke
	#	print ('It broke')

imapObj.logout()



##Sending email part
#Outlook port
#port = 587
##SMTP server domain name - TLS
#smtpObj = smtplib.SMTP('smtp-mail.outlook.com', 587)
#
##Check for errors in object
##print (smtpObj.ehlo())
#
##Set up encrypted SMTP connection
#smtpObj.starttls()
#
##Logging in
##print (smtpObj.login(originEmail, password))
#smtpObj.login(originEmail, password)
#
##Test of sending an originEmail
##smtpObj.sendmail(originEmail, destinationEmail,
##'Subject: So long.\nDear Alice, so long and thanks for all the fish. Sincerely, Bob')
#
##Logging off
#smtpObj.quit()