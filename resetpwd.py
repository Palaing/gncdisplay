#-----------------------------------------------------------------------------
# Name:			resetpwd.py
# Purpose:		"gncdisplay" app
#				password reset routes
#
# Author:		a.goye
#
# Created:		08/04/2023
# Copyright:	(c) a.goye 2023
# Licence:		GPLv3
#-----------------------------------------------------------------------------

# TODO: move tokens to different csv file for users file security

from bottle import request, response, get, post
from helpers import log, ftemplate, getuser, changepwd, gettokens, savetokens
import re
import hashlib
import bcrypt
from datetime import datetime, timedelta
import messages as msgs
from sendmail import sendmail
import json
	
# validate a password with min length 6 and max length 20,
# at least 1 digit, 1 upcase and 1 lowcase letter, 1 special character
def validpwd(password):
	pattern = re.compile(
		'^(?=\S{6,20}$)(?=.*?\d)(?=.*?[a-z])(?=.*?[A-Z])(?=.*?[^A-Za-z\s0-9])'
	)
	return re.search(pattern, password)

@get('/forgotpwd')
def forgotpwd():
	return ftemplate('forgotpwd.html')

@post('/forgotpwd')
def do_forgotpwd():
	# exit if user does not exist
	email = request.forms.getunicode('email')
	user = getuser(email)
	if not user:
		return ftemplate('login.html', message = msgs.reset_mail_sent)

	# save a token and date for this user
	tokens = gettokens()
	exp = (datetime.now() + timedelta(minutes=30)).strftime('%Y-%m-%d %H:%M:%S')
	token = hashlib.md5(str(exp).encode()).hexdigest()
	tokens[email] = (exp, token)
	savetokens(tokens)
	
	# send link by mail to user
	link = (request.app.config['base_url'] 
			+ '/resetpwd/' + email + '/' + token)
	# res = sendmail(msgs.reset_password.format(user[1],link), email)
	res = sendmail(msgs.reset_password.format(user[0], link))
	if res == "success":
		log(str(datetime.now()) + ': sent password-reset link to ' + email)
	else: 
		log(str(datetime.now()) + ': password-reset link NOT sent to ' + email)
	return ftemplate('login.html', message=msgs.reset_mail_sent)
	
@get('/resetpwd/<email>/<token>')
def resetpwd(email, token):
	# check token and its expiry date
	tokens = gettokens()
	exp, token1 = tokens.get(email,('',''))
	if not (getuser(email) and token == token1):
		return ftemplate('login.html', message=msgs.invalid_link)
	if datetime.now() > datetime.strptime(exp, '%Y-%m-%d %H:%M:%S'):
		return ftemplate('login.html', message=msgs.reset_lnk_timeout)

	# send email in tmp cookie
	content = str(email) + ':' + str(datetime.date(datetime.now()))
	response.set_cookie('tmpsession', content, path='/',
						secret = request.app.config.get('secret'),
						max_age = request.app.config.get('tmpsession_life'))

	# send choose-password page
	return ftemplate('resetpwd.html')
	
@post('/resetpwd')
def do_resetpwd():
	# check tmp cookie
	content = request.get_cookie('tmpsession',
								secret = request.app.config.get('secret'))
	if not content:
		return ftemplate('login.html', message=msgs.pwd_not_recorded)
	email, sessiondate = content.split(':')
	if sessiondate != str(datetime.date(datetime.now())):
		return ftemplate('login.html', message=msgs.pwd_reset_timeout)
			
	# encode and store new password
	password = request.forms.getunicode('password')
	if not validpwd(password):
		return ftemplate('forgotpwd.html', message=msgs.invalid_pwd)
	pwd = password.encode('utf-8')
	hashedpwd = bcrypt.hashpw(pwd, bcrypt.gensalt()).decode('utf-8')	
	changepwd(email, hashedpwd)
	
	# clean and send login page
	tokens = gettokens()
	del tokens[email]
	savetokens(tokens)
	response.delete_cookie('tmpsession')
	return ftemplate('login.html', message=msgs.pwd_recorded)
