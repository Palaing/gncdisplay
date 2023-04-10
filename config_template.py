#-------------------------------------------------------------------------------
# Name:			config_template.py
# Purpose:		"gncdisplay" app
#				show structure of config.py file: confidential configuration data
#
# Author:		a.goye
#
# Created:		08/04/2023
# Copyright:	(c) a.goye 2023
# Licence:		GPLv3
#-------------------------------------------------------------------------------

# secret key for cookies signature
secret = "a_very_secret_phrase_to_encode_cookies"

# key for form hidden parameters encryption
key = b'a_very_random_key'

# smtp data for sending emails,
# plus default 'to' and 'from' mail addresses
mail = {
	'host':	'ssl.mysmtpserver.com',
	'port':	587,
	'id':	'my_id_on_ssl.mysmtpserver.com',
	'pwd': 	'my_password_on_ssl.mysmtpserver.com',
	'to': 	'defaultreccipient@someserver.com',
	'from':	'defaultsender@someserver.com',
}

# data files
# db file is a gnucash data file under sqlite3 format
dbfile = 'path/to/gnucash/sqlite3/file'
# userfile is a json-dumped file with following format:
# {email: [firstname, lastname, email, account, password]}
userfile = 'path/to/user/json/file'
# tokenfile is a json-dumped file with following format:
# {email: [expirydate, token]}
tokenfile = 'path/to/tokens/json/file'