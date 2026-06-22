import pandas as pd


def load_csv(filepath):
    df = pd.read_csv(filepath)
    df = df.dropna(how="all")
    return df.to_dict(orient="records")


def load_excel(filepath, sheet_name=0):
    df = pd.read_excel(filepath, sheet_name=sheet_name)
    df = df.dropna(how="all")
    return df.to_dict(orient="records")