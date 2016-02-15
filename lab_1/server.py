#!/usr/bin/env python2.7
from RPCServerHandler import RPCServerHandler
import SocketServer, os, atexit, json
import wrapper

# Initialize all the things
PORT = 8000
handler = RPCServerHandler
httpd = SocketServer.ThreadingTCPServer(("localhost", PORT), handler, False)
httpd.allow_reuse_address = True
httpd.server_bind()
httpd.server_activate()

# Register files in "static" recursively
for root, dirnames, filenames in os.walk('static'):
  for f in filenames:
    f = root + '/' + f
    print("ADDING : ", f, " : ", os.path.relpath(f, 'static'))
    RPCServerHandler.register_file(f, os.path.relpath(f, 'static'))
# Point '' to index.html

### ----------------------------------
### STATIC FILES: GET any path relative to PWD
### ----------------------------------
# redirrect "/" to "static/index.html"
RPCServerHandler.register_redirect("", "/ui/index.html")

### ----------------------------------
### RPC API (POST)
### ----------------------------------
# restart: reload student code
# returns None
RPCServerHandler.register_function(lambda d : RPCServerHandler.reload_modules(), 'restart')

# ls: list directory contents
# returns a dictionary { directories: ["abc",...], files: ["abc",..] }
RPCServerHandler.register_function(lambda d : ls_path( d['path']) , 'ls')

# cat: read contents of a file
# returns string contents of file
RPCServerHandler.register_function(lambda d : cat_file( d['path'] ), 'cat')

# call: call student code
# returns return value
RPCServerHandler.register_module("wrapper")
### ----------------------------------

def cleanup():
  # free the socket
  print("CLEANING UP!")
  httpd.shutdown()
  print("CLEANED UP")

atexit.register(cleanup)

# Start the server
print("serving files and RPCs at port", PORT)
httpd.serve_forever()
