#!/usr/bin/env python3


import json, os, re, shlex, subprocess, sys, threading, time, xml

from PyQt4.QtWebKit import QWebView
from PyQt4.QtGui import QApplication
from PyQt4.QtCore import QUrl

from db.pg_utils import *
from db.mongo_utils import *
from utils import wikipedia


def dbs_exist():
	"""
		Test to see if app has been run before.
		Basically check if the databases are populated.
	"""
	pass


def setup_app():
	"""
		Configure App
		Basically setup databases.
	"""
	pass


def get_current_version():
	"""
		Check the current version (basically the date) of the XML dumps
	"""
	pass


def get_db_version():
	"""
		Check version (bascially the date) of the host XML dumps
	"""
	pass


def compare_db():
	"""
		Compare the version (basically the date) of the host XML dumps
		to the current version of the wikimedia XML dumps
	"""
	pass


def update_dbs():
	"""
		Check for updates to the XML Dumps and download the updates if they
		have been updated since current version.
	"""
	pass


def start_server():
	"""
		Start the HTML server for the GUI.

		This is ghetto, we'll have to whip up something proper later.
	"""
	webpage_dir = os.path.dirname(os.path.realpath(__file__)) + '/web'
	args = shlex.split('python -m SimpleHTTPServer 9001')
	
	try:
		cwd = os.chdir(webpage_dir)
		server = subprocess.Popen(args)
		print(server.pid)
	except Exception as err:
		print(err)
		return None


def stop_server(server):
	"""
		Stop the HTML server for the GUI.
	"""
	try:
		server.kill()
		while server.returncode is None:
			pass
		return server.returncode
	except NameError:
		print('server object DNE.')
		return False


def main():
	"""
		Run CLIkipedia in GUI mode.
	"""
	app = QApplication(sys.argv)
	browser = QWebView()
	start_server()
	time.sleep(3)
	browser.load(QUrl('http://localhost:9001'))
	browser.show()
	sys.exit(app.exec_())


if __name__ == '__main__':
	main()
