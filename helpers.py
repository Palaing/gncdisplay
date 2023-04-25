#-----------------------------------------------------------------------------
# Name:			helpers.py
# Purpose:		"gncdisplay" app
#				utility functions
#
# Author:		a.goye
#
# Created:		08/04/2023
# Copyright:	(c) a.goye 2023
# Licence:		GPLv3
#-----------------------------------------------------------------------------

from bottle import template, abort
from config import userfile, tokenfile
import re
import json

def ensureadmin(usr):
	if not usr['isadmin']:
		abort(401)

def log(msg):
	with open('gncdisplay.log', 'a', encoding='utf-8') as logfile:
		logfile.write('\n' + msg)
	return msg

def ftemplate(file,**kwargs):
	with open('vues/' + file, 'r', encoding='utf-8') as template_file:
		tempstring = template_file.read()
	return template(tempstring,kwargs)
	
def validmail(email):
	return bool(re.match(r'[^@]+@[^@]+\.[^@]+', email))
	
def getusers():
	with open(userfile, 'r') as uf: 
		users = json.load(uf)
	return users

def saveusers(users):
	with open(userfile, "w") as uf:
		json.dump(users, uf)
		
def getuser(email):
	users = getusers()
	return users[email]
	
def changepwd(email, password):
	users = getusers()
	user = users[email]
	user[4] = password 
	saveusers(users)

def gettokens():
	with open(tokenfile, 'r') as tf: 
		tokens = json.load(tf)
	return tokens

def savetokens(tokens):
	with open(tokenfile, "w") as tf:
		json.dump(tokens, tf)
