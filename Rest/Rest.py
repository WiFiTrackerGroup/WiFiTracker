import requests
import cherrypy
import time
import json as js
import DataMasking
import DataAggregation
import DataAcquisition


class RestInterface:
    exposed = True

    def __init__(self):
        self.port = 8080
        self.ip = "0.0.0.0"
        self.dataMasking = DataMasking()
        self.dataAggregation = DataAggregation()
        self.dataAcquisition = DataAcquisition()

    def getIP(self):
        return self.ip

    def getPort(self):
        return self.port

    def GET(self, *uri, **params):
        if uri[0] == 'AP':
            dataAcquisition.acquire_AP()
            df = dataAggregate.aggregate_AP()

        if uri[0] == 'data':
            dataAcquisition.acquire()
            df = dataAggregation.aggregate()
            l1, l2 = dataMasking(list(df["MAC"]), list(df["user"]))
            df.drop(columns=['MAC'])
            df.drop(columns=['user'])
            df.insert(0, "MAC_masked", l1)
            df.insert(1, "user_masked", l2 )


        return js.dumps(df)


if __name__ == "__main__":
    conf = {
        "/": {
            "request.dispatch": cherrypy.dispatch.MethodDispatcher(),
            "tools.session.on": True,
        }
    }

    webService = RestInterface()
    cherrypy.tree.mount(webService, "/", conf)
    cherrypy.config.update({"server.socket_host": webService.getIP()})
    cherrypy.config.update({"server.socket_port": webService.getPort()})

    cherrypy.engine.start()

    try:
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        cherrypy.engine.stop()
