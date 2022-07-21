import pandas as pd

happy_df = pd.read_csv("data/happy.csv")


def get_df(value):
    df = happy_df[["Total happiness", value]].dropna().reset_index(drop=True)
    categories = df[value].unique()
    df1 = df["Total happiness"][(df[value] == categories[0])]
    df2 = df["Total happiness"][(df[value] == categories[1])]
    return categories, df1, df2


def get_stats(df):
    n = df.size
    mean = round(df.mean(), 3)
    std = round(df.std(), 3)
    q1 = df.quantile(0.25)
    median = df.median()
    q3 = df.quantile(0.75)
    iqr = q3 - q1
    return n, mean, std, q1, median, q3, iqr
