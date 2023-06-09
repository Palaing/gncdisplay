#-----------------------------------------------------------------------------
# Name:			authplugin.py
# Purpose:		"gncdisplay" app
#				authentication plugin
#
# Author:		a.goye
#
# Created:		08/04/2023
# Copyright:	(c) a.goye 2023
# Licence:		GPLv3
#-----------------------------------------------------------------------------

from bottle import request, redirect, makelist
from datetime import datetime
import inspect

class AuthPlugin(object):

	name = 'authplugin'

	def __init__(self, keyword='usr', secret='', adminemails=['']):
		self.keyword = keyword
		self.secret = secret
		self.adminemails = adminemails

	def sessiondata(self):
		idtoday = request.get_cookie('session', secret=self.secret)
		if idtoday:
			email, prenom, sessiondate = idtoday.split(':')
			if sessiondate == str(datetime.date(datetime.now())):
				return {
					'email': email, 
					'prenom': prenom, 
					'isadmin': email in self.adminemails
				}
		return dict()
		
	def apply(self, callback, context):
		keyword = self.keyword
		
		spec = inspect.getfullargspec(callback)
		args = makelist(spec[0]) + makelist(spec.kwonlyargs)
		if keyword not in args:
			return callback		
			
		def wrapper(*args, **kwargs):
			usr = self.sessiondata()
			if usr:
				kwargs[keyword] = usr
				return callback(*args, **kwargs)
			else:
				redirect("login")
				
		return wrapper
