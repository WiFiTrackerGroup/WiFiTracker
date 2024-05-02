import pandas as pd
import sys

if __name__ == "__main__":
    file_user = sys.argv[1]
    file_ap = sys.argv[2]
    
    df_user = pd.read_csv(file_user)
    print("\nNumber of users:", len(df_user))
    df_ap = pd.read_csv(file_ap)
    df_joined = df_user.merge(df_ap, on="name_ap", how="left")
    df_joined.to_csv(file_user)
