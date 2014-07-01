# -*- coding:UTF-8 -*-
# Author:Ju Dalong
# Date:2013/11/29
# This is the UDP client program 
import socket
import traceback
import math
import thread
from websocket import create_connection

class Robot:
    def __init__(self,name,team,number,robot_x,robot_y,direct_x,direct_y,ip,port,state):
        self.name=name
        self.team=team
        self.number=number
        self.ip=ip
        self.port=port
        self.state=state
        self.robot_x=robot_x
        self.robot_y=robot_y
        self.direct_x=direct_x
        self.direct_y=direct_y
    def address(self):
        return (self.ip,self.port)
    def setteam(self,value):
        self.team=value
    def setnumber(self,value):
        self.number=value
    def setstate(self,value):
        self.state=value
    def setip(self,value):
        self.ip=value
    def setport(self,value):
        self.port=value
    def setlocation(self,value_x,value_y,value1_x,value1_y):
        self.robot_x=value_x
        self.robot_y=value_y
        self.direct_x=value1_x
        self.direct_y=value1_y
        
class Ball:
    def __init__(self,owner,ball_x,ball_y):
        self.owner=owner
        self.ball_x=ball_x
        self.ball_y=ball_y
    def setowner(self,value):
        self.owner=value
    def setlocation(self,value_x,value_y):
        self.ball_x=value_x
        self.ball_y=value_y

def Distance(ball,robot):
    distance = int(math.sqrt(pow(ball.ball_x-robot.robot_x,2)+pow(ball.ball_y-robot.robot_y,2)))
    return distance

def Distance2(direction,robot):
    if (direction == 'Left'):
        distance = int(math.sqrt(pow(Left_goal_x-robot.robot_x,2)+pow(Left_goal_y-robot.robot_y,2)))
    else:
        distance = int(math.sqrt(pow(Right_goal_x-robot.robot_x,2)+pow(Right_goal_y-robot.robot_y,2)))
    return distance

def Angle(ball,robot):
    k_robot = math.atan2(robot.direct_y-robot.robot_y,robot.direct_x-robot.robot_x)
    k_ball = math.atan2(ball.ball_y-robot.robot_y,ball.ball_x-robot.robot_x)
    k = k_robot-k_ball
    angle = int((k/(2*math.pi)*360)*100)
    if angle<0:
        angle=angle+36000
    return angle

def Angle2(direction,robot):
    if (direction == 'Left'):        
        k_goal = math.atan2(Left_goal_y-robot.robot_y,Left_goal_x-robot.robot_x)
    else:
        k_goal = math.atan2(Right_goal_y-robot.robot_y,Right_goal_x-robot.robot_x)
    k_robot = math.atan2(robot.direct_y-robot.robot_y,robot.direct_x-robot.robot_x)
    k = k_robot-k_goal
    angle = int((k/(2*math.pi)*360)*100)
    if angle<0:
        angle=angle+36000
    return angle

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

	
# Initialize 
Left_goal_x = 1024
Left_goal_y = 350
Right_goal_x = 0
Right_goal_y = 350
# Initialize  Robot
robot=[0]*4
robot[0]=Robot(0,'B','W',0,0,0,0,'192.168.165.162',8081,0)
robot[1]=Robot(1,'B','G',0,0,0,0,'192.168.165.161',8081,0)
robot[2]=Robot(2,'Y','G',0,0,0,0,'192.168.165.163',8081,0)
robot[3]=Robot(3,'Y','W',0,0,0,0,'192.168.165.164',8081,0)
# Initialize  Robot
ball=Ball(9,0,0)


#host1 = "192.168.165.8"   # server1(raspberry pi) ip
#host2 = "192.168.165.163" # server2(raspberry pi) ip
#host3 = "192.168.165.164" # server3(raspberry pi) ip
#host4 = "192.168.165.165" # server4(raspberry pi) ip   
#port_ras = 8081      
#addr1 = (host1,port_ras)     
#addr2 = (host2,port_ras)
#addr3 = (host3,port_ras)    
#addr4 = (host4,port_ras)

# UDP server ip and port
host = '192.168.165.152'
port = 6000
UDPSERVER_address = (host,port)

#UDP setting
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
s.bind(UDPSERVER_address)
s.settimeout(100)




BUFSIZE = 1024 
MSGSIZE = 18   #The length of sending message
message_last='0'*62
print """SWJTUIC Robot wireless communication client test system
                                                               V1.2
-------------------------------------------------------------------
Mode setting : 1 test mode,message is input by user
               0 UDP  mode,message get by CV 

Message protocol V01:
The length of message is 18
Which means:
        Message[0:3]:  ball_x
        Message[3:6]:  ball_y
        Message[6:9]:  robot_x
        Message[9:12]: robot_y
        Message[12:15]:direct_x
        Message[15:18]:direct_y
-------------------------------------------------------------------"""
print '初始化设置'

INPUTMODE = int(raw_input("模式选择:1 测试模式        0 UDP模式")) # Mode setting : 1 test mode,message is input by user
                                                   #                0 UDP  mode,message get by CV
                                
if (INPUTMODE==1):
    print ("Mode 1")
else:
    print ("Mode 0")

DIRECTION= int(raw_input('进攻方向设置：1 向左 0向右'))
if (DIRECTION==1):
    direction='Left'
else:
    direction='Right'

print ("************************Test begin************************")



def dataprocess(message,address):
    if(address == addr1):
        print "Robot1 recevied message:",message,"from DSP"
        
    elif (address == addr2):
        print "Robot2 has recevied message:",message
    elif (address == addr3):
        print "Robot3 has recevied message:",message
    elif (address == addr4):
        print "Robot4 has recevied message:",message
    else:
        print "Receive data:%s from cv"%message
        # date process
        ball.setlocation(int(message[0:3],16),int(message[3:6],16))
        #robot1.setlocation=
        ball_x = int(message[0:3],16)
        ball_y = int(message[3:6],16)
        robot1_x = int(message[6:9],16)
        robot1_y = int(message[9:12],16)
        direct_x = int(message[12:15],16)
        direct_y = int(message[15:18],16)
        if ((ball_x== 0 and ball_y==0)or(robot_x==0 and robot_y==0)or(direct_x==0 and direct_y==0)):
            print "Location message is not full,discard."
        else:
            distance = int(math.sqrt(pow(ball_x-robot_x,2)+pow(ball_y-robot_y,2)))
            k_robot = math.atan2(direct_y-robot_y,direct_x-robot_x)
            k_ball = math.atan2(ball_y-robot_y,ball_x-robot_x)
            k = k_robot-k_ball
            angle = int((k/(2*math.pi)*360)*100)
            if angle<0:
                angle=angle+36000

            print "ball(",ball_x,",",ball_y,") robot(",robot_x,",",robot_y,") direct(",direct_x,",",direct_y,")"
            print 'Distance:%08d  \nAngele:%08d'%(distance,angle)
            #print "Protocol version V%s"%msg[1:3]
        
            #if msg.startswith("1"):
            msg_tran='%04x%04x00000000'%(distance,angle)
            #msg='0010%04x00000000'%(angle)
            #msg=msg[3:]
            s.sendto(msg_tran,addr4)
            print "Message %s has been sent to Robot1(IP:%s)"%(msg_tran,host4)
        
            #elif msg.startswith("2"):
            #    s.sendto(msg,addr2)
            #    print "Message %s send to Robot2(IP:%s)"%(msg,host2)
            #elif msg.startswith("3"):
            #    s.sendto(msg,addr3)
            #    print "Message %s send to Robot1(IP:%s)"%(msg,host3)
            #elif msg.startswith("4"):
            #    s.sendto(msg,addr4)
            #    print "Message %s send to Robot1(IP:%s)"%(msg,host4)
            #else:
            #    print ("Wrong message!")
            #    continue
            #data, addrr = s.recvfrom(BUFSIZE)
            #if not data:
            #    print "server has exist"
            #    break
            #print "Robot has recevied message:",data
    thread.exit()
        
def data2process(message,address):
    global ball,robot,message_last
    if(address == robot[0].address()):
        print "Robot1 has recevied message:",message
    elif (address == robot[1].address()):
        print "Robot2 has recevied message:",message
    elif (address == robot[2].address()):
        print "Robot3 has recevied message:",message
    elif (address == robot[3].address()):
        print "Robot4 has recevied message:",message
    else:
        print "Receive data:%s from cv"%message
        # date process
        if (ball.owner != 9):
            if (ball.owner == 0):
                distance = Distance2(direction,robot[0])
                angle = Angle2(direction,robot[0])
                if (distance<100 and (angle <85 or (angle<355 and angle>270))):
                    msg_tran='02%04x%04x000000'%(distance,angle)
                else:
                    msg_tran='FF%04x%04x000000'%(distance,angle)
                #print 'Distance:%08d  \nAngele:%08d'%(distance,angle)
                s.sendto(msg_tran,robot[0].address())
                print "Message %s has sent to Robot1(IP:%s)"%(msg_tran,robot[0].ip)
            elif (ball.owner == 1):
                distance = Distance2(direction,robot[1])
                angle = Angle2(direction,robot[1])
                if (distance<100 and (angle <85 or (angle<355 and angle>270))):
                    msg_tran='02%04x%04x000000'%(distance,angle)
                else:
                    msg_tran='FF%04x%04x000000'%(distance,angle)
                #print 'Distance:%08d  \nAngele:%08d'%(distance,angle)
                s.sendto(msg_tran,robot[1].address())
                print "Message %s has sent to Robot2(IP:%s)"%(msg_tran,robot[1].ip)
            else:
                distance_0 = Distance2(direction,robot[0])
                distance_1 = Distance2(direction,robot[1])
                angle_0 = Angle2(direction,robot[0])
                angle_1 = Angle2(direction,robot[1])
                #print 'Robot1 Distance:%08d  \nAngele:%08d'%(distance_0,angle_0)
                #print 'Robot2 Distance:%08d  \nAngele:%08d'%(distance_1,angle_1)
                msg_tran='FF%04x%04x000000'%(distance_0,angle_0)
                s.sendto(msg_tran,robot[0].address())
                print "Message %s has sent to Robot1(IP:%s)"%(msg_tran,robot[0].ip)
                msg_tran='FF%04x%04x000000'%(distance_1,angle_1)
                s.sendto(msg_tran,robot[1].address())
                print "Message %s has sent to Robot2(IP:%s)"%(msg_tran,robot[1].ip)
        elif((int(message[0:3],16) == 0 and int(message[3:6],16) == 0)):
            print "Location message is not full,discard."
        else:
            if (message[6:8] == 'NL'):
                message = message[:6]+message_last[6:20]+message[20:]
            if (message[20:22] == 'NL'):
                message = message[:20]+message_last[20:34]+message[34:]
            if (message[34:36] == 'NL'):
                message = message[:34]+message_last[34:48]+message[48:]
            if (message[48:50] == 'NL'):
                message = message[:48]+message_last[48:62]+message[62:]    
            message_last=message[:]
            ball.setlocation(int(message[0:3],16),int(message[3:6],16))
            a = range(4)
            for i in range(4):
                for j in a:
                    if (message[6+i*14]==robot[j].team and message[7+i*14]==robot[j].number):
                        robot[j].setlocation(int(message[(8+i*14):(11+i*14)],16),int(message[(11+i*14):(14+i*14)],16),
                        int(message[(14+i*14):(17+i*14)],16),int(message[(17+i*14):(20+i*14)],16))
                        b=a.pop(a.index(j))
                        break
            distance_0 = Distance(ball,robot[0])
            distance_1 = Distance(ball,robot[1])
            if (distance_0<distance_1):
                angle=Angle(ball,robot[0])
                print 'Distance:%08d  Angele:%08d'%(distance_0,angle)
                msg_tran='03%04x%04x000000'%(distance_0,angle)
                s.sendto(msg_tran,robot[0].address())
                print "Message %s has sent to Robot1(IP:%s)"%(msg_tran,robot[0].ip)
                # robot1?                
            else:
                angle=Angle(ball,robot[1])
                print 'Distance:%08d\nAngele:%08d'%(distance_1,angle)
                msg_tran='03%04x%04x000000'%(distance_1,angle)
                s.sendto(msg_tran,robot[1].address())
                print "Message %s has sent to Robot2(IP:%s)"%(msg_tran,robot[1].ip)
                # robot0?
                
    thread.exit()

# Sending date
if (INPUTMODE):
    while True:
        try:
            message = raw_input('Please input Message(size of %d):'%MSGSIZE)
            if len(message)!= MSGSIZE:
                print ("Wrong message!")
                continue
            thread.start_new(dataprocess,(message, address))
        except (KeyboardInterrupt, SystemExit,):
            cont = raw_input("contiue?")
            if(cont in 'yes'):
                continue
            else:
                print ("************************Test end************************")
                s.close()
                break            
        except:
            traceback.print_exc()
            cont = raw_input("contiue?")
            if(cont in 'yes'):
                continue
            else:
                print ("************************Test end************************")
                s.close()
                break
else:
    while True:
        try:
            print "Waiting for message....."
            message, address = s.recvfrom(BUFSIZE)
            #thread.start_new(data2process,(message, address))
            thread.start_new(TalkReporter,(message,))                       
        except (KeyboardInterrupt):
            msg_tran='0000000000000000'
            s.sendto(msg_tran,robot[0].address())
            s.sendto(msg_tran,robot[1].address())
            cont = raw_input ("All robot stop,contiue?")
            if(cont in 'yes'):
                continue
            else:
                print ("************************Test end************************")
                s.close()
                
                break            
        except (socket.timeout):
            cont = raw_input ("Timeout for waiting,contiue?")
            if(cont in 'yes'):
                continue
            else:
                print ("************************Test end************************")
                s.close()
                
                break
        except (SystemExit):
            cont = raw_input("contiue?")
            if(cont in 'yes'):
                continue
            else:
                print ("************************Test end************************")
                s.close()
                
                break 
        except:
            traceback.print_exc()
            cont = raw_input("contiue?")
            if(cont in 'yes'):
                continue
            else:
                print ("************************Test end************************")
                s.close()
                
                break
