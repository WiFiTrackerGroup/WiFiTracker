import os
import pandas as pd

path = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(path,"then.csv")
df = pd.read_csv(path)
print(df["From"])