#!/usr/bin/python
# -*- coding: utf-8 -*-

# Marina Martín Hernández
# Ejercicio 9.7

import webapp
import urllib2

class CacheContent_App(webapp.webApp):

	dicc_client = {}
	dicc_server = {}
	cont_client = 0
	cont_server = 0
	url         = ""
################################################################################
	def create_htmlbody (self, contents, original_url):
		first     = contents.find("<body")
		last      = contents.find(">", first)
		url_body  = '<a href=' + original_url + '>' + "Original Webpage" + '</a></br>'
		url_body += '<a href=reload/>' + "Reload" + '</a></br>'
		url_body += '<a href=Server_HTTP_Side>' + "Server-Side HTTP " + '</a>'
		url_body += '<a href=Client_HTTP_Side>' " Client-Side HTTP" + '</a>'
		htmlBody  = contents[:first] + url_body + contents[last+1:]
		return htmlBody
################################################################################
	def parse (self, request):
		self.dicc_client[self.cont_client] = request
		try:
			parsedRequest  = request.split(' ', 2)[1][1:]
		except IndexError:
			parsedRequest  = ''
		return parsedRequest
################################################################################
	def process(self, parsedRequest):
		if parsedRequest == '':
			httpCode = "404 Not Found"
			htmlBody = "ERROR. Try to put a resource."
		elif parsedRequest == "reload/":
			link = urllib2.urlopen(str(self.url))
			httpCode = "302 Found"
			data = link.read()
			htmlBody = "Bien"
		elif parsedRequest == "Server_HTTP_Side":
			httpCode  = "200 OK"
			htmlBody  = '<html><body><h3>' + str(self.dicc_server.items())
			htmlBody += '</h3></br></body></html>'
		elif parsedRequest == "Client_HTTP_Side":
			httpCode  = "200 OK"
			htmlBody  = '<html><body><h3>' + str(self.dicc_client.items())
			htmlBody += '</h3></br></body></html>'
		else:
			try:
				url_available = "http://" + parsedRequest
				link          = urllib2.urlopen(url_available)
				headers       = link.info().headers
				self.dicc_server[self.cont_server] = headers
				htmlBody = link.read()
				htmlBody = self.create_htmlbody(htmlBody, url_available)
				httpCode = "200 OK"
			except IOError:
				httpCode = "404 Not Found"
				htmlBody = "ERROR. Try to put a resource."
		return (httpCode, htmlBody)
################################################################################

if __name__ == "__main__":
	testWebApp = CacheContent_App("localhost", 1234)