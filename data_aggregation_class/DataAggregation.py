import pandas as pd
from config import *
import re

class DataAggregation:

    def __init__(self):
        pass

    def fill_dataframe(self):
        df_usernames = pd.read_csv(FILE_USERNAME, header = None, sep = '.')
        print(df_usernames)

    def open_username(self):
        data = []
        with open(FILE_USERNAME, 'r') as file_object:
            line = file_object.readline()
            while line:
                key, match = _parse_line(line)
                if key == mac:
                    print("ciao")

    def _parse_line(line):
    """
    ciao
    """
    rx_dict = {
        'mac': re.compile(r'iso.3.6.1.4.1.14179.2.1.4.1.3.(?P<mac>.*) '),
    }
    for key, rx in rx_dict.items():
        match = rx.search(line)
        if match:
            return key, match
    # if there are no matches
    return None, None
                

elem = DataAggregation()
elem.open_username()