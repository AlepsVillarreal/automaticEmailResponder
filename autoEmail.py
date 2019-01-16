import os
import sys
import pyzmail
import imapclient
import pprint
from credentials import originEmail, password, destinationEmail
import smtplib
import html2text

#Outlook port
port = 587

#Depending in encryption, choose what kind of object to create

#SSL standard
#smtpObj = smtplib.SMTP_SSL('smtp-mail.outlook.com', 465)

#SMTP server domain name - TLS
smtpObj = smtplib.SMTP('smtp-mail.outlook.com', 587)
#print (type(smtpObj))

#Check for errors in object
#print (smtpObj.ehlo())

#Set up encrypted SMTP connection
smtpObj.starttls()

#Logging in
#print (smtpObj.login(originEmail, password))
smtpObj.login(originEmail, password)

#Test of sending an originEmail
#smtpObj.sendmail(originEmail, destinationEmail,
#'Subject: So long.\nDear Alice, so long and thanks for all the fish. Sincerely, Bob')

#Logging off
smtpObj.quit()

#Trying out IMAP to retrieve emails
imapObj = imapclient.IMAPClient('imap-mail.outlook.com', ssl=True)

#logging in imap object
imapObj.login(originEmail, password)

#Selecting folder to read files from
imapObj.select_folder('INBOX', readonly=True)

#pprint.pprint(imapObj.list_folders())

#Selecting UIDs of emails - setting criteria
UIDs = imapObj.search('(ON "15-Jan-2019")')

#Printing UIDs of emails
print (UIDs)

#Fetching emails
fetched = imapObj.fetch(UIDs,  ['BODY[]'])


#UIDs to use [5350, 5354, 5360, 5367, 5371, 5378]
message = pyzmail.PyzMessage.factory(fetched[5367][b'BODY[]'])

print (message.get_subject())

print (message.get_addresses('from'))

print (message.get_addresses('to'))

#print (message.text_part.get_payload().decode(message.text_part.charset))

#print (message.html_part.get_payload().decode(message.text_part.charset))
#print (message.html_part.get_payload().decode(message.html_part.charset))

body = html2text.html2text(message.html_part.get_payload().decode(message.html_part.charset))

print (body)

imapObj.logout()


