import sys

sys.path.append("data_anonimization")
import cherrypy
import schedule
import os
import time
import json as js
from config import N_BYTES, T_UPD_SALT, IP, PORT
from data_masking import DataMasking
import DataAggregation
import DataAcquisition


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
    try:
        while True:
            if (time.time() - t_start) > T_UPD_SALT:
                web_service.set_salt(os.urandom(N_BYTES))
            time.sleep(5)
    except KeyboardInterrupt:
        cherrypy.engine.stop()
