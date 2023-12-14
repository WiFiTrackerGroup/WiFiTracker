import cherrypy
from cherrypy.lib import auth_digest
import schedule
import os
import time
import json as js
from sub.config import N_BYTES, T_UPD_SALT, IP, PORT, HOUR
from sub.data_acquisition import DataAcquisition
from sub.data_masking import DataMasking
from sub.data_aggregation import DataAggregation


# TODO: schedule the AP retieval
class SnmpRest:
    exposed = True

    def __init__(self):
        self.set_salt(os.urandom(N_BYTES))
        self.data_mask = DataMasking()
        self.data_aggr = DataAggregation()
        self.data_acq = DataAcquisition()

    def set_salt(self, salt: bytes):
        """Set the random salt needed to the DataMasking module"""
        self._salt = salt

    def GET(self, *uri):
        if len(uri) > 0:
            if uri[0] == "AP":
                # self.data_acq.acquier_AP()
                try:
                    df_ap = self.data_aggr.aggregate_AP()
                except:
                    raise cherrypy.HTTPError(500, f"Error in retrieving AP data!")
                return js.dumps(df_ap.to_dict())

            elif uri[0] == "data":
                # self.data_acq.acquier()
                try:
                    df_data = self.data_aggr.aggregate()
                except:
                    raise cherrypy.HTTPError(
                        500, f"Error in retrieving connected devices data!"
                    )

                l1, l2 = self.data_mask.hashing_SHA256(
                    list(df_data["mac_user"]), list(df_data["username"]), self._salt
                )
                df_data = df_data.drop(columns=["mac_user", "username"])
                df_data.insert(0, "MAC_masked", l1)
                df_data.insert(1, "user_masked", l2)
                return js.dumps(df_data.to_dict())


USERS = {"jon": "secret"}

if __name__ == "__main__":
    # conf = {
    #     "/": {
    #         "request.dispatch": cherrypy.dispatch.MethodDispatcher(),
    #         "tools.sessions.on": True,
    #     }
    # }

    conf = {
        "/": {
            "request.dispatch": cherrypy.dispatch.MethodDispatcher(),
            "tools.auth_digest.on": True,
            "tools.auth_digest.realm": "localhost",
            "tools.auth_digest.get_ha1": auth_digest.get_ha1_dict_plain(USERS),
            "tools.auth_digest.key": "a565c27146791cfb",
            "tools.auth_digest.accept_charset": "UTF-8",
        },
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
