import cherrypy
import mongoDB_library as mDB
import json as js
from .config import *


class adaptor_mongo_interface(object):
    exposed = True

    def __init__(self):
        self.ip = IP_REST_ADAPTOR_DB
        self.port = PORT_REST_ADAPTOR_DB

        
        self.db_counting = mDB(IP_MONGODB, PORT_MONGODB)
        self.coll_name = NAME_MONGODB
        

    def getPort(self):
        return self.port()
    
    def getIP(self):
        return self.ip()
    
    def GET(self, *uri, **params):
        list_parameters = params.keys()
        if uri[0] == self.coll_name:
            if all(par in ["class", "init_date", "final_date"] for par in list_parameters):
                return self.db_counting.findBy_class_period(
                                                        int(params['class']),
                                                        int(params['init_date']),
                                                        int(params['final_date']))
            if all(par in ["init_date", "final_date"] for par in list_parameters):
                return self.db_counting.findBy_period(
                                                    int(params['init_date']),
                                                    int(params['final_date']))

    def POST(self, *uri):
        body_string = cherrypy.request.body.read()
        new_data_dict = js.loads(body_string)
        if uri[0] == self.coll_name:
            self.db_counting.insert_records(new_data_dict)