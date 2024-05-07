import sys
import os
import pandas as pd
import json

if __name__ == "__main__":
    '''
    Simple JSON to csv converter.
    Note: make sure to change the input file!
    '''
    inp_file = sys.argv[1]  
    out_file = os.path.splitext(inp_file)[0] + ".csv"
    try:
        with open(inp_file) as f:
            json_log = json.load(f)
        df_log = pd.DataFrame.from_dict(json_log) 
        df_log.to_csv(out_file, index= False)
    except:
        sys.exit(1)
    
    sys.exit(0)
