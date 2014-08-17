# -*- coding:UTF-8 -*-
# Author:Bloomlj
# Date:2014/7/1

import serial
#import math
#import thread
from websocket import create_connection

ser = serial.Serial(7, 9600, timeout=10)

#web socket for reporter

def TalkReporter(msg):
	ws = create_connection("ws://localhost/websocket")
	#print "Sending 'Hello, World'..."
	ws.send(msg)
	#print "Sent"
	#print "Reeiving..."
	result =  ws.recv()
	#print "Received '%s'" % result
	ws.close()

while True:
    #read serial
    #message, address = s.recvfrom(BUFSIZE)
    
    message = ser.readline()
    #send to server
    print(message)
    TalkReporter(message)