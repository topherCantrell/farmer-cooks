import tornado.ioloop
import tornado.web
import os

import sys

if sys.platform == 'win32':
    import asyncio
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

class TestHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('You got me')

def main():     
    root = os.path.dirname(__file__)
    
    cont = os.path.join(root,'webroot')
    
    handlers = [
        (r"/test",TestHandler),
        (r"/(.*)", tornado.web.StaticFileHandler, {"path": cont, 'default_filename': 'index.html'})
    ]
            
    app = tornado.web.Application(handlers)
    app.listen(8080)
    tornado.ioloop.IOLoop.current().start()
    
if __name__ == '__main__':
    main()