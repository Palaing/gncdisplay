#-----------------------------------------------------------------------------
# Name:			sendmail.py
# Purpose:		simplify sending email messages
#
# Author:		a.goye
#
# Created:		08/04/2023
# Copyright:	(c) a.goye 2023
# Licence:		GPLv3
#-----------------------------------------------------------------------------

import smtplib
from email import encoders
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from config import mail

tomail = mail['to']
frommail = mail['from']
	
# sends an email (default recipient is tomail); first line ismail subject
# returns 'success' or 'failure'
# +++ note: attachment is given as a string; it must be coded in utf8 +++

def sendmail(mailcontent, sendtomail=tomail, sendfrommail=frommail,
			replytomail='', attachment='', filename=''):
	[subject, nline, text] = mailcontent.partition('\n')
	if attachment:
		msg = MIMEMultipart()	
		msg.attach(MIMEText(text, 'plain'))
		payload = MIMEBase('application', 'octet-stream')
		payload.set_payload(attachment, 'utf8')
		encoders.encode_base64(payload)
		if not filename:
			filename = 'fichier.txt'
		payload.add_header('Content-Disposition', 
							f'attachment; filename= {filename}')
		msg.attach(payload)
	else:
		msg = EmailMessage()	
		msg.set_content(text)
	msg['Subject'] = subject
	msg['From'] = sendfrommail
	msg['To'] = sendtomail
	if replytomail:
		msg.add_header('reply-to', replytomail)
	s = smtplib.SMTP(host=mail['host'], port=mail['port'])
	s.starttls()
	s.login(mail['id'], mail['pwd'])
	res = 'failure'
	try:
		s.send_message(msg)
		res = 'success'
	except SMTPRecipientsRefused as err:
		with open('refusedmails.log', 'a', encoding='utf-8') as logfile:
			logfile.write('\n{0}'.format(err))
	except Exception as err:
		with open('sendmail.log', 'a', encoding='utf-8') as logfile:
			logfile.write('\nUnexpected error: {0}'.format(err))
	finally:
		s.quit()
		return res