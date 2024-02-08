import cherrypy
import mongoDB_library as mDB
import json as js
from .config import *


class adaptor_mongo_interface(object):
    exposed = True

    def __init__(self):
        self.ip = IP_REST_ADAPTOR_DB
        self.port = PORT_REST_ADAPTOR_DB
        self.db = mDB(IP_MONGODB, PORT_MONGODB)
        

    def getPort(self):
        return self.port()
    
    def getIP(self):
        return self.ip()
    
    def GET(self, *uri):
        pass

    def POST(self, *uri):
        body_string = cherrypy.request.body.read()
        new_data_dict = js.loads(body_string)
        if uri[0] == "":
            self.db.insert_one_dict(new_data_dict)