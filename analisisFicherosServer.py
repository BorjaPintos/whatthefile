# -*- coding: utf-8 -*-
import sys
import random
import subprocess
import cgi
import uuid
import core
import re
import json
from urllib.parse import urlparse
from urllib.parse import parse_qs
from http.server import BaseHTTPRequestHandler, HTTPServer

md5RegularExpresions = re.compile('/^[a-f0-9]{32}$/i')


class handler(BaseHTTPRequestHandler):
	def do_POST(self):
		self.server_version = ""
		self.sys_version = ""
		ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
		modulesToUse = parseValues(self.path)
		if ctype == 'multipart/form-data':
			pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
			content_len = int(self.headers.get('Content-length'))
			pdict['CONTENT-LENGTH'] = content_len
			postvars = cgi.parse_multipart(self.rfile, pdict)
			ident = core.run(postvars['fileToUpload'][0], modulesToUse);
			self.send_response(302)
			self.send_header('Location', "/"+ident)
			self.end_headers()
		else:
			self.send_response(400)
			self.end_headers()
			self.wfile.write("Se debe subir un fichero")

	def do_GET(self):
		self.server_version = ""
		self.sys_version = ""
		if self.path == '/favicon.ico':
			do_sendFavicon(self)
		elif self.path == '/listModules':
			do_sendModules(self)
		elif self.path == '/':
			do_sendForm(self)
		elif self.path == '/kill':
			pywebserver.server_close()
		else:
			do_viewReport(self, self.path)


def parseValues(path):
	o = urlparse(path)
	queryparams = parse_qs(o.query)
	modulesToUse = []
	try:
		unparserModulesToUse = queryparams['values'][0].split(",")
		for unparserModule in unparserModulesToUse:
			try:
				moduleStr = unparserModule.split(":")
				module = {}
				module["id"] = int(moduleStr[0])
				module["params"] = []
				args = moduleStr[1].split(" ")
				for arg in args:
					module["params"].append(arg)
				modulesToUse.append(module)
			except:
				print("invalid module:" + unparserModule)
	except:
		print("no modules")
	return modulesToUse
def do_sendFavicon(self):
	self.send_response(200)
	self.send_header("Content-type", "image/png")
	self.end_headers()
	self.wfile.write(open("./images/favicon.png", "rb").read())

def do_sendModules(self):
	self.send_response(200)
	self.send_header("Content-type", "application/json")
	self.end_headers()
	self.wfile.write(json.dumps(core.getModules(), indent=4).encode())

def do_sendForm(self):
	self.send_response(200)
	self.send_header("Content-type", "text/html")
	self.end_headers()
	self.wfile.write(open("./pages/index.html", "rb").read())

def do_viewReport(self, name):
	report = core.viewReport(name.split('/')[1])
	if report is None:
		do_404(self)
	else:
		self.send_response(200)
		self.send_header("Content-type", "application/json")
		self.end_headers()
		self.wfile.write(json.dumps(report,indent=4).encode())

def do_404(self):
	self.send_response(200)
	self.send_header("Content-type", "text/html")
	self.end_headers()
	self.wfile.write("404 not found".encode())

if __name__ == "__main__":
	PORT = 8080

pywebserver = HTTPServer(("", PORT), handler)

print ("Simulando el servicio en el puerto: " +  str(PORT))
try:
	pywebserver.serve_forever()
except KeyboardInterrupt:
	pass
pywebserver.server_close()
