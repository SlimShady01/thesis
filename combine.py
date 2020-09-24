import pandas as pd

pd1 = pd.read_csv("fli.csv")
pd2 = pd.read_csv("sep_fli.csv")

pd1["month"] = "april"

bigdata = pd1.append(pd2, ignore_index=True)
bigdata.to_csv("august_7_result.csv", index=False)