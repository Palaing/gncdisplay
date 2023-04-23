#-----------------------------------------------------------------------------
# Name:			app.py
# Purpose:		"gncdisplay" app
#				users routes
#
# Author:		a.goye
#
# Created:		08/04/2023
# Copyright:	(c) a.goye 2023
# Licence:		GPLv3
#-----------------------------------------------------------------------------

# TODO: 
# get gnucash file from Dropbox
# review and fix URLs management

from bottle import get, post, request, response, redirect, error, static_file
from datetime import datetime
from helpers import ensureadmin, ftemplate, getuser
from config import dateupfile, firstyear
from datetime import datetime
import messages as msgs
import bcrypt
import re

def check_pwd(email, password):
	user = getuser(email)
	if user and \
		bcrypt.checkpw(password.encode('utf-8'),user[4].encode('utf-8')):
		return (email, user[0])
	return('','')

@get('/img/<filename>')
def server_static(filename):
	return static_file(filename, root='img')

@get('/login')
def login():	
	if request.app.config['authplugin'].sessiondata():
		redirect('show')
	return ftemplate('login.html', redirecturl='show')

@post('/login')
def do_login():
	email = request.forms.getunicode('email')
	password = request.forms.getunicode('password')
	redirecturl = request.forms.getunicode('redirecturl', 'show')
	email, prenom = check_pwd(email, password)
	if email:
		idtoday = ':'.join([str(email), prenom, 
							str(datetime.date(datetime.now()))])
		response.set_cookie('session', idtoday, 
							secret = request.app.config.get('secret'))
		redirect(redirecturl)
	else:
		return ftemplate('login.html', message = msgs.connexion_failed,
						redirecturl = redirecturl)

@get('/logout')
def logout():
	response.delete_cookie('session')
	return ftemplate('login.html', 
		message = msgs.logout_ok, redirecturl='show')

@get('/')
def home():
	redirect('show')

@get('/show')
def show(usr, db, email=''):
	email = email or usr['email']
	account = getuser(email)[3]
	today = datetime.now().strftime('%Y-%m-%d')
	query = """SELECT DISTINCT SUBSTR(t1.post_date, 1, 10) as date, t1.description,
	PRINTF("%.2f", CAST(-s1.value_num AS REAL) /s1.value_denom) AS montant 
	FROM splits s1
	INNER JOIN transactions t1 ON t1.guid=s1.tx_guid
	INNER JOIN accounts a1 ON s1.account_guid=a1.guid
	WHERE a1.code = ?
	AND s1.value_num != '0'
	AND date <= ?
	ORDER BY t1.post_date"""
	cur = db.execute(query, (account,today,))
	transactions = cur.fetchall()
	with open(dateupfile, "r") as df:
		dateup = df.read()[:10]
	cur.execute('SELECT name FROM accounts WHERE code = ?', (account,))
	hoirs = cur.fetchone()[0]
	return ftemplate('transactions.html', 
				user=usr, transactions=transactions, dateup=dateup, hoirs=hoirs)
	
@error(401)
def error401(url):
	return ftemplate('401.html')
	
@error(404)
def error404(error):
	return ftemplate('404.html')

@get('/expenses/<year>')
def expenses(usr, db, year):
	query = """SELECT a1.name,
	SUM(CAST(s1.value_num AS REAL) /s1.value_denom) AS somme
	FROM splits s1
	INNER JOIN transactions t1 ON t1.guid=s1.tx_guid
	INNER JOIN accounts a1 ON s1.account_guid=a1.guid 
	WHERE a1.account_type = 'EXPENSE'
	AND SUBSTR(t1.post_date, 1, 4) = ?
	GROUP BY a1.guid 
	ORDER BY somme DESC"""
	cur = db.execute(query, (str(year),))
	expenses = [item for item in cur.fetchall()]
	names = [exp[0] for exp in expenses]
	sommes = [exp[1] for exp in expenses]
	now = datetime.now()
	years = range(firstyear, now.year + 1)
	return ftemplate('expenses.html', user=usr, expenses=expenses, 
					year=year, years=years, names=names, sommes=sommes)

@post('/expenses')
def yearexpenses(usr, db):
	year = request.forms.getunicode('year')
	return expenses(usr, db, year)

@get('/expenses')
def lastyearexpenses(usr, db):
	now = datetime.now()
	lastyear = now.year - 1
	return expenses(usr, db, lastyear)

# ########### admin routes ###########

@get('/setdateup/<date>')
def setdateup(usr, date):
	ensureadmin(usr)
	with open(dateupfile, "w") as df:
		df.write(date)

@get('/show/<email>')
def showuser(usr, db, email):
	ensureadmin(usr)
	return show(usr, db, email)
