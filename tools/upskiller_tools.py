import pandas as pd
from agents import function_tool

UPSKILL_PATH = "data/upskill.csv"

@function_tool
def get_upskill_courses():
    df = pd.read_csv(UPSKILL_PATH)
    return df.to_dict(orient="records")