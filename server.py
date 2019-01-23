#!/usr/bin/env python3
#  coding: utf-8 
import socketserver

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        #Get the request token from data
        self.data = self.request.recv(1024).strip()
        recv_data = str(self.data).split()
        get_request = ""
        data = ""
        response_code = ""
        mime_type = ""
        for token_index in range(len(recv_data)):
            if recv_data[token_index][0:5] == "b'GET":
                get_request = recv_data[token_index+1]
                break
        
        #Find the mime-type
        print("GET REQUEST:", get_request)
        print("SPLIT", get_request.split("."))
        if (get_request == "/"):
            response_code = "200 OK"
            #mime_type = "text/html"

        f_type = get_request.split(".")
        if (len(f_type) == 2):
            if (get_request.split(".")[1] == "html"):
                response_code = "200 OK"
                mime_type = "text/html"

            if (get_request.split(".")[1] == "css"):
                response_code = "200 OK"
                mime_type = "text/css"

        else:
            response_code = "404 Not Found"
            mime_type = "text/html"
            data = "\n<!DOCTYPE html><html><body><h1>404 Not Found</h1></body></html>\r\n"

        if ((mime_type == "text/html") and (response_code == "200 OK")):
            try:
                with open("www" + get_request, "r") as serve_file:
                    data = serve_file.read()
            except:
                response_code = "404 Not Found"
                data = "<html><body><h1>404 Not Found</h1></body></html>"
            



        #with open("www" + get_request, "r") as serve_file:
            #data = serve_file.read()
        #print("Got a request of: %s\n" % recv_data)
        #print("GET REQUEST: %s\n" % get_request)
        response = "HTTP/1.1 %s\nContent-Type: %s\r\n%s" % (response_code, mime_type, data)
        print("RESPONSE: %s" %response)
        #self.request.sendall(bytearray("OK",'utf-8'))
        self.request.sendall(bytearray(response,'utf-8'))

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
