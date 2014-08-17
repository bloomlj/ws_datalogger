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

    print("Server is running on 80 port now.")
    application.listen(80)
    tornado.ioloop.IOLoop.instance().start()
    
    
   
