import cherrypy
import schedule
import os
import time
import json as js
from sub.config import N_BYTES, T_UPD_SALT, IP, PORT, HOUR
from sub.data_acquisition import DataAcquisition
from sub.data_masking import DataMasking
from sub.data_aggregation import DataAggregation


# TODO: controllo: quando get/data devo avere AP più recenti (e controllare che get/AP sia già stata fatta)
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
            # self.data_acq.acquire_AP()
            df_ap = self.data_aggr.aggregate_AP()

            return js.dumps(df_ap.to_dict())

        elif uri[0] == "data":
            # self.data_acq.acquire()
            df_data = self.data_aggr.aggregate()
            l1, l2 = self.data_mask.hashing_SHA256(
                list(df_data["mac_user"]), list(df_data["username"]), self._salt
            )
            df_data = df_data.drop(columns=["mac_user", "username"])
            df_data.insert(0, "MAC_masked", l1)
            df_data.insert(1, "user_masked", l2)

            return js.dumps(df_data.to_dict())


if __name__ == "__main__":
    conf = {
        "/": {
            "request.dispatch": cherrypy.dispatch.MethodDispatcher(),
            "tools.sessions.on": True,
        }
    }

    web_service = SnmpRest()
    cherrypy.tree.mount(web_service, "/", conf)
    cherrypy.config.update({"server.socket_host": IP})
    cherrypy.config.update({"server.socket_port": PORT})

    cherrypy.engine.start()
    schedule.every().day.at(HOUR).do(web_service.set_salt, os.urandom(N_BYTES))
    try:
        while True:
            schedule.run_pending()
            time.sleep(5)
    except KeyboardInterrupt:
        cherrypy.engine.stop()
