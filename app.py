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
from config import base_url, secret, adminemails, postmaster, dbfile

onrender = 'RENDER' in os.environ
onlinux = 'SHELL' in os.environ

# TODO : move URL and mail data to config file

app = default_app()
app.config.update({
	'base_url': base_url,
	'postmaster': postmaster,
})

dbplugin = bottle.ext.sqlite.Plugin(dbfile=dbfile, keyword='db')
app.install(dbplugin)

app_authplugin = AuthPlugin(keyword='usr', 
							secret=secret, adminemails=adminemails)
						
app.install(app_authplugin)
app.config['authplugin'] = app_authplugin

import home
import resetpwd

# required for wsgi on apache2
application = app

if __name__ == '__main__':
	if onrender:
		app.config['base_url'] = os.environ.get('RENDER_EXTERNAL_URL')
		hostname = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
		run(host=hostname, port=80, debug=True)
	elif onlinux:
		app.config['base_url'] = base_url + ':8000'
		run(host=base_url[8:], port=8000, debug=True, reloader=True)
	else:
		app.config['base_url'] = 'http://localhost:8000'
		run(host='localhost', port=8000, debug=True, reloader=True)

