import pandas as pd
from load_data import get_league
from math import ceil
import itertools
import numpy as np

def get_team_mobile_avg_pts(df,team,n=5):
    team_points = get_team_evolution(df,team)
    return team_points.rolling(n,min_periods=1).mean()

def get_team_avg_pts(df,team):
    team_points = get_team_evolution(df,team)
    result = (np.cumsum(team_points))/team_points.index
    result[0] = 0
    return result

def get_team_matches(df,team):
    return df.loc[(df.HomeTeam.str.match(team))|\
                (df.AwayTeam.str.match(team))]

def calc_points(entry):
    if entry["FTHG"] > entry["FTAG"]:
        return {"HomeTeamPoints":3,"AwayTeamPoints":0}
    else:
        if entry["FTHG"] == entry["FTAG"]:
            return {"HomeTeamPoints":1,"AwayTeamPoints":1}
        else:
            return {"HomeTeamPoints":0,"AwayTeamPoints":3}

def get_matches_points(df):
    result = []
    for i in range(0,df.shape[0]):
        entry = df.iloc[i]
        result.append(calc_points(df.iloc[i]))
    return pd.DataFrame(result)

def get_matching_points_in_entry(entry,team):
    if entry["HomeTeam"] == team:
        return entry.HomeTeamPoints
    else:
        return entry.AwayTeamPoints

def get_team_points(df,team):
    if ("HomeTeamPoints" not in df.columns) or\
            ("AwayTeamPoints" not in df.columns):
                raise ValueError("Points columns not in df. Maybe you"+\
                        " forgot to use get_team_matches?")
    return df.apply(lambda x : get_matching_points_in_entry(x,team),axis=1)

def interesting_cols():
    return ["Date","HomeTeam","AwayTeam","FTHG","FTAG"]

def get_team_evolution(df,team):
    games_df = get_team_matches(df,team)[interesting_cols()]
    points = get_matches_points(games_df)
    whole_df = pd.concat([games_df.reset_index(),points.reset_index()],axis=1)
    whole_df = whole_df[interesting_cols()+["HomeTeamPoints","AwayTeamPoints"]]
    points = get_team_points(whole_df,team)
    return points
