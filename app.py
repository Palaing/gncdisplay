#-----------------------------------------------------------------------------
# Name:			app.py
# Purpose:		"gncdisplay" app
#				main app file
#
# Author:		a.goye
#
# Created:		08/04/2023
# Copyright:	(c) a.goye 2023
# Licence:		GPLv3
#-----------------------------------------------------------------------------

from bottle import debug, run, default_app
import bottle.ext.sqlite
import os
from authplugin import AuthPlugin
from config import secret, dbfile

onrender = 'RENDER' in os.environ

app = default_app()
app.config.update({
	'base_url': os.environ.get('RENDER_EXTERNAL_URL', 'http://localhost:8000'),
	'secret': secret,						# cookies encryption key
	'tmpsession_life': 1800,				# lifetime of the pwd reset cookie
	'adminemails': ['alain.goye@free.fr'],	# emails of site admins
	'postmaster': 'postmaster@viensatoi.fr',
})

dbplugin = bottle.ext.sqlite.Plugin(dbfile=dbfile, keyword='db')
app.install(dbplugin)

app_authplugin = AuthPlugin(keyword='euser', secret = app.config.get('secret'), 
							adminemails = app.config.get('adminemails'))
						
app.install(app_authplugin)
app.config['authplugin'] = app_authplugin

import home
# import admin
import resetpwd
# import invite

if __name__ == '__main__':
	if onrender:
		hostname = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
		run(host=hostname, port=80, debug=True)
	else:
		run(host='localhost', port=8000, debug=True, reloader=True)
