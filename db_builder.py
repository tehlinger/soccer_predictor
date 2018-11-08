import pandas as pd

import features_calculator as fc
from load_data import get_league

def get_team_data_per_match(year):
    df = get_league(year)[-55:]
    db = format_data_for_team_avg_evolution(year)

def format_data_for_team_avg_evolution(year):
    df = get_league(year)
    result = None
    for team in df.HomeTeam.unique():
        team_df = fc.get_team_matches(df,team)
        avgs = fc.get_team_avg_pts(df,team)
        points = fc.get_team_evolution(df,team)
        res = pd.DataFrame({\
                "Club":[team for i in range(0,team_df.shape[0])],
                "Date":team_df.Date,\
                "avg":avgs.values,\
                "m_avg_5":fc.get_team_mobile_avg_pts(df,team,n=5).values,
                "n":[i for i in range(0,team_df.shape[0])],\
                "pts":points.values})
        if result is None:
            result = res
        else:
            result = result.append(res)
    return result

def build_db(year):
    df = get_league(year)
