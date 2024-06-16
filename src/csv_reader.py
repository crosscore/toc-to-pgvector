import pandas as pd
import glob
file_path = glob.glob("../data/csv/original/*.csv")
df = pd.read_csv(file_path[0], encoding="utf-8")
print(df)
