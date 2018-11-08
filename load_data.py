import pandas as pd
import datetime

def get_league(year):
    try:
        f = "data/"+str(year)+".csv"
        result =  pd.read_csv(f)
        result["Date"] = result.Date.apply(lambda x :\
                datetime.datetime.strptime(x,"%d/%m/%y"))
        return result
    except FileNotFoundError as e:
        raise ValueError("Year "+str(year)+" : no datafile match.")
