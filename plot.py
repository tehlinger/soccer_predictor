import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from features_calculator import get_team_points,get_team_avg_pts,get_team_matches
from load_data import get_league


def plot_avg_through_time(df):
    sns.lineplot(data=df,x="Date",y="avg",hue="Club")
    plt.show()
