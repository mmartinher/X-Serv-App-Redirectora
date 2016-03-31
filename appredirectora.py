#!/usr/bin/python
# -*- coding: utf-8 -*-

# Marina Martín Hernández
# Ejercicio App Redirectora

import socket
import random

class webApp:

    def parse (self, request):
        return None

    def process (self, parseRequest):
        url = 'http://localhost:1234/' + str(random.randint(0,999999))
        htmlAnswer  = "<html><body><p><h1><center>"
        htmlAnswer += "<body style='background:#8A2BE2'>"
        htmlAnswer += "<span style='color:#FFFACD'>"
        htmlAnswer += 'New redirection: '+ str(url)+ "</center></h1></p>"
        htmlAnswer += "<meta http-equiv='refresh' content='3;"
        htmlAnswer += "URL=" + str(random.randint(0,999999))
        htmlAnswer += "'></p></body></html>"
        return ("302 Found", htmlAnswer)

    def __init__(self, hostname, port):

        mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        mySocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        mySocket.bind((hostname, port))
        mySocket.listen(5)

        try:
            while True:
                print 'Waiting for connections'
                (recvSocket, address) = mySocket.accept()
                print 'HTTP request received (going to parse and process):'
                request = recvSocket.recv(2048)
                print request
                parsedRequest = self.parse(request)
                (returnCode, htmlAnswer) = self.process(parsedRequest)
                print 'Answering back...'
                recvSocket.send("HTTP/1.1 " + returnCode + " \r\n\r\n"
                                + htmlAnswer + "\r\n")
                recvSocket.close()
        except KeyboardInterrupt:
                print "Closing binded socket"
                mySocket.close()

if __name__ == "__main__":
    testWebApp = webApp("localhost", 1234)
