import tornado.ioloop
import tornado.web
import tornado.websocket
import os
#import socket
#from multiprocessing import Process,Queue

            
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html',a=1)
        #self.write("Hello, world")

def send_message(message):
    for handler in ChatWebSocket.socket_handlers:
        try:
            handler.write_message(message)
        except:
            logging.error('Error sending message', exc_info=True)
            
class ChatWebSocket(tornado.websocket.WebSocketHandler):
    socket_handlers = set()
    def open(self):
        ChatWebSocket.socket_handlers.add(self)
        #send_message('A new user has entered the chat room.')

    def on_message(self, message):
        #self.write_message(u"You said: " + message+udpmsg)
        send_message(message)
       
    def on_close(self):
        ChatWebSocket.socket_handlers.remove(self)
        #send_message('A user has left the chat room.')
        

"""def socket_p(q):
    HOST = '192.168.165.152'                 # Symbolic name meaning all available interfaces
    PORT = 6000              # Arbitrary non-privileged port
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(10)
    while 1:
        conn, addr = s.accept()
        udppacket = conn.recv(1024)
        q.put(udppacket)
        #print(udppacket)
    conn.close()
"""
settings = {
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
}

application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/websocket", ChatWebSocket),
    (r"/static/(.*)", tornado.web.StaticFileHandler, dict(path=settings['static_path'])),
], **settings)


#udpmsg = ''
if __name__ == "__main__":
    #q = Queue()
    #p = Process(target=socket_p, args=(q,))
    #p.start()
    #udpmsg = q.get()
    
    #p.join()
    
    application.listen(80)
    tornado.ioloop.IOLoop.instance().start()
    
   
