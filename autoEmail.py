import os
import sys
import pyzmail
import imapclient
import pprint
from credentials import originEmail, password, destinationEmail
import smtplib

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

imapObj.select(mailbox='INBOX', readonly=True)

pprint.pprint(imapObj.list_folders())

#logging in imap object
imapObj.login(originEmail, password)

