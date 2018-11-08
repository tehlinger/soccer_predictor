import pandas as pd

import features_calculator as fc
from load_data import get_league
from db_builder import format_data_for_team_avg_evolution

def get_only_feats_columns_renamed(prefix,matches,feats):
    of_interest = list(set(feats.columns)-set(matches.columns))
    res_df = feats[of_interest]
    res_df.columns = [prefix+i for i in res_df.columns]
    return res_df

def categorize(x):
    if x["FTHG"] > x["FTAG"]:
        return ("home_win")
    else:
        if x["FTHG"] == x["FTAG"]:
            return "draw"
        else:
            return "home_lose"

def get_features_for_all_matches(year):
    db = format_data_for_team_avg_evolution(year)
    matches = get_league(year)\
            [fc.interesting_cols()]
    home_feats = merge_matches("HomeTeam",db,matches)
    home_feats = \
            get_only_feats_columns_renamed(\
            "home_",matches,home_feats)
    away_feats = merge_matches("AwayTeam",db,matches)
    away_feats = \
            get_only_feats_columns_renamed(\
            "away_",matches,away_feats)
    res = pd.concat([matches.reset_index(),\
            home_feats.reset_index(),away_feats.reset_index()]\
            ,axis=1)
    res["day"] = res["home_n"]
    res =  res.drop(columns=["index","Date","HomeTeam","AwayTeam"\
            ,"home_n","away_n"])
    res["target"] = res.apply(lambda x : categorize(x),axis=1)
    return res.loc[res.day > 0]

def merge_matches(column,db,matches):
    modif_df = db.copy()
    modif_df[column] = modif_df["Club"]
    #modif_df = modif_df.drop(columns=["Club"])
    result =\
            matches.merge(modif_df,how="left",on=["Date",column],\
            suffixes=("","_"+column.lower()))
    return result.drop(columns=["Club"])

def test():
    db = format_data_for_team_avg_evolution(2014)
    matches = get_league(2014)
    return merge_matches("HomeTeam",db,matches)

def get_big_df():
    result =None
    for i in range(2008,2019):
        if i == 2016:
            continue
        print(str(i)+"...")
        df = get_features_for_all_matches(i)
        if result is None:
            result = df
        else:
            result = result.append(df)
    return result
