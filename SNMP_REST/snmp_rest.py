import cherrypy
from cherrypy.lib import auth_digest
import schedule
import os
import time
import json as js
from sub.config import *
from sub.data_acquisition import DataAcquisition
from sub.data_masking import DataMasking
from sub.data_aggregation import DataAggregation
import pandas as pd


class SnmpRest:
    exposed = True

    def __init__(self):
        self.set_salt(os.urandom(N_BYTES))
        self.data_mask = DataMasking()
        self.data_aggr = DataAggregation()
        self.data_acq = DataAcquisition()
        self.ts = [time.time() - TIME_BUFF]

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
                if self.ts[0] < (time.time() - TIME_BUFF):
                    # self.data_acq.acquier()
                    try:
                        df_data = self.data_aggr.aggregate()
                    except:
                        raise cherrypy.HTTPError(
                            500, f"Error in retrieving connected devices data!"
                        )

                    # Adding the mac masked
                    l1, l2 = self.data_mask.hashing_SHA256(
                        list(df_data["mac_user"]), list(df_data["username"]), self._salt
                    )
                    df_data = df_data.drop(columns=["mac_user", "username"])
                    df_data.insert(0, "MAC_masked", l1)
                    df_data.insert(1, "user_masked", l2)

                    # Adding Timestamp
                    self.ts = [time.time()] * len(df_data)
                    df_data.insert(0, "Timestamp", self.ts)
                    self.df_data = df_data

                return js.dumps(self.df_data.to_dict())

            elif uri[0] == "test":
                self.data_acq.acquier()
                df_ap = self.data_aggr.aggregate_AP()
                user = pd.DataFrame(self.data_aggr.open_username())
                rssi = pd.DataFrame(self.data_aggr.open_rssi())
                snr = pd.DataFrame(self.data_aggr.open_snr())
                byte_rx = pd.DataFrame(self.data_aggr.open_bytes_rx())
                byte_tx = pd.DataFrame(self.data_aggr.open_bytes_tx())
                ap_mac = pd.DataFrame(self.data_aggr.open_ap_mac())

                l1, l2 = self.data_mask.hashing_SHA256(
                    list(user["mac_user"]), list(user["username"]), self._salt
                )

                output = {
                    "MAC_masked": list(l1),
                    "user_masked": list(l2),
                    "rssi": list(rssi.rssi),
                    "snr": list(snr.snr),
                    "byte_rx": list(byte_rx.byte_rx),
                    "byte_tx": list(byte_tx.byte_tx),
                    "ap_name": list(ap_mac.name_ap),
                }

                return js.dumps(output)


# USERS = {"jon": "secret"}

if __name__ == "__main__":
    conf = {
        "/": {
            "request.dispatch": cherrypy.dispatch.MethodDispatcher(),
            "tools.sessions.on": True,
        }
    }

    #   conf = {
    #       "/": {
    #           "request.dispatch": cherrypy.dispatch.MethodDispatcher(),
    #           "tools.auth_digest.on": True,
    #           "tools.auth_digest.realm": "localhost",
    #           "tools.auth_digest.get_ha1": auth_digest.get_ha1_dict_plain(USERS),
    #           "tools.auth_digest.key": "a565c27146791cfb",
    #           "tools.auth_digest.accept_charset": "UTF-8",
    #       },
    #   }

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
