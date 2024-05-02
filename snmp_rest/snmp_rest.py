import cherrypy
import requests
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

        self.SNMPaddr = "http://" + IP + ":" + str(PORT)

    def set_salt(self, salt: bytes):
        """Set the random salt needed to the DataMasking module"""
        self._salt = salt

    def GET(self, *uri):
        if len(uri) == 1:
            if uri[0] == "AP":
                self.data_acq.acquier_AP()
                try:
                    df_ap = self.data_aggr.aggregate_AP()
                except:
                    raise cherrypy.HTTPError(500, f"Error in retrieving AP data!")
                return js.dumps(df_ap.to_dict())

            elif uri[0] == "data":
                if self.ts[0] < (time.time() - TIME_BUFF):
                    self.data_acq.acquier()
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

            elif uri[0] == "APChannelInfo":
                self.data_acq.acquier_AP_info()
                try:
                    df_APdata = self.data_aggr.aggregate_channel_info()
                except:
                    raise cherrypy.HTTPError(
                        500, f"Error in retrieving connected devices data!"
                    )

                # Adding Timestamp
                ts = [time.time()] * len(df_APdata)
                df_APdata.insert(0, "Timestamp", ts)
                return js.dumps(df_APdata.to_dict())


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
    schedule.every().day.at(HOUR_SALT).do(web_service.set_salt, os.urandom(N_BYTES))
    schedule.every().day.at(HOUR_AP).do(requests.get, web_service.SNMPaddr + "/AP")

    # First AP name initialization (start run)
    requests.get(web_service.SNMPaddr + "/AP")

    try:
        while True:
            schedule.run_pending()
            time.sleep(5)
    except KeyboardInterrupt:
        cherrypy.engine.stop()
