import numpy as np
import pandas as pd


index = pd.Index(data=["Tom", "Bob", "Mary", "James", "Andy", "Alice"], name="name")

data = {
    "age": [18, 30, np.nan, 40, np.nan, 30],
    "city": ["BeiJing", "ShangHai", "GuangZhou", "ShenZhen", np.nan, " "],
    "sex": [None, "male", "female", "male", np.nan, "unknown"],
    "birth": ["2000-02-10", "1988-10-17", None, "1978-08-08", np.nan, "1988-10-17"],
    "is_trade":[None,False,True,False,True,False]
}

user_info = pd.DataFrame(data=data, index=index)
user_info["is_trade"] = user_info["is_trade"].fillna(False)
user_info["age"].fillna(0)
print(user_info)