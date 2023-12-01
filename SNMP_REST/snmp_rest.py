import cherrypy
import schedule
import os
import time
import json as js
from sub.config import N_BYTES, T_UPD_SALT, IP, PORT, HOUR
from sub.data_acquisition import DataAcquisition
from sub.data_masking import DataMasking
from sub.data_aggregation import DataAggregation


class SnmpRest:
    exposed = True

    def __init__(self):
        self.set_salt(os.urandom(N_BYTES))
        self.data_mask = DataMasking()
        self.data_aggr = DataAggregation()
        self.data_acq = DataAcquisition()

    def set_salt(self, salt: bytes):
        self._salt = salt

    def GET(self, *uri):
        if uri[0] == "AP":
            self.data_acq.acquire_AP()
            df = self.data_aggr.aggregate_AP()

        if uri[0] == "data":
            self.data_acq.acquire()
            df = self.data_aggr.aggregate()
            l1, l2 = self.data_mask.hashing_SHA256(
                list(df["MAC"]), list(df["user"]), self._salt
            )
            df.drop(columns=["MAC"])
            df.drop(columns=["user"])
            df.insert(0, "MAC_masked", l1)
            df.insert(1, "user_masked", l2)

        return js.dumps(df)


if __name__ == "__main__":
    conf = {
        "/": {
            "request.dispatch": cherrypy.dispatch.MethodDispatcher(),
            "tools.session.on": True,
        }
    }

    web_service = SnmpRest()
    cherrypy.tree.mount(web_service, "/", conf)
    cherrypy.config.update({"server.socket_host": IP})
    cherrypy.config.update({"server.socket_port": PORT})

    cherrypy.engine.start()
    t_start = time.time()
    schedule.every().day.at(HOUR).do(web_service.set_salt, os.urandom(N_BYTES))
    try:
        while True:
            schedule.run_pending()
            time.sleep(5)
    except KeyboardInterrupt:
        cherrypy.engine.stop()
