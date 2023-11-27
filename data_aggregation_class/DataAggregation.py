import pandas as pd
from config import *
import re
import parse

def _parse_line(line):
        """
        
        """
        rx_dict = {
            'mac': re.compile(r'iso.3.6.1.4.1.14179.2.1.4.1.3.(?P<mac>.*) ='),
        }
        for key, rx in rx_dict.items():
            match = rx.search(line)
            if match:
                return key, match
        # if there are no matches
        return None, None

class DataAggregation:

    def __init__(self):
        pass

    def fill_dataframe(self):
        df_usernames = pd.read_csv(FILE_USERNAME, header = None, sep = '.')
        print(df_usernames)

    def open_username(self):
        data = []
        with open(FILE_USERNAME, 'r') as file_object:
            for line in file_object:
                mac_res = parse.search('iso.3.6.1.4.1.14179.2.1.4.1.3.{} =', line).fixed
                dom_res = parse.search('@{}"', line).fixed
                row = {
                    'mac': mac_res[0],
                    'domain': dom_res[0]
                }
                data.append(row)
        
        data = pd.DataFrame(data)
        print(data)
                

    
                

elem = DataAggregation()
elem.open_username()