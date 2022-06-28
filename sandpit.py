import pandas as pd

happy_df = pd.read_csv("happy.csv")
stats_df = happy_df[["Total happiness", "Sex"]].dropna()
stats_df1 = stats_df["Total happiness"][(stats_df["Sex"] == "M")]
stats_df2 = stats_df["Total happiness"][(stats_df["Sex"] == "F")]
mean1 = stats_df1.mean()
mean2 = stats_df2.mean()
print(round(mean1, 3))
print(round(mean2, 3))