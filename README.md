python-proxyserver forking async
==================

Simple tcp proxy server for forwarding tcp connections in python.

This software functions as a proxy server between a client and another server.

this variant is forking (allows multiple client connections at once) and
asynchronous (it does not block on waiting for data) and allows any tcp data stream to pass.

i have tested by tunneling vnc connections.

Please configure the appropriate host/port information at the top of proxyserver.py

Enjoy!
