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
        self.data = self.request.recv(1024).strip()
        tokens = self.data.decode().split()
        mime_type = ""
        response_code = ""
        try:
            r_index = tokens.index("GET")
            r_data = tokens[r_index+1]
        except:
            response_code = "405 Method Not Allowed"
            mime_type = "text/html"
            data = "<html><body><h1>405 Not Found</h1></body></html>"

        try:
            if (r_data[-1] == "/"):
                r_data += "index.html"

            if (len(r_data.split(".")) == 2):
                if (r_data.split(".")[1] == "html"):
                    mime_type = "text/html"
                if (r_data.split(".")[1] == "css"):
                    mime_type = "text/css"
            
            with open("www" + r_data, "r") as serve_file:
                data = serve_file.read()

        except:
            response_code = "404 Not Found"
            mime_type = "text/html"
            data = "<html><body><h1>404 Not Found</h1></body></html>"

        response = "HTTP/1.1 %s\nContent-Type: %s\r\n\r\n%s" % (response_code, mime_type, data)
        print ("RESPONSE: %s\n" % response)

        self.request.sendall(bytearray(response,'utf-8'))

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()