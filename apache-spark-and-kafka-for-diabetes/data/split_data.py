import pandas as pd
from sklearn.model_selection import train_test_split
import os

def split_data(input_file, offline_file, online_file):
    if not os.path.exists(input_file): return
    df = pd.read_csv(input_file)
    off, on = train_test_split(df, test_size=0.2, stratify=df['Diabetes_binary'], random_state=42)
    off.to_csv(offline_file, index=False)
    on.to_csv(online_file, index=False)

if __name__ == "__main__":
    split_data("data/diabetes_binary_5050split_health_indicators_BRFSS2015.csv", "data/offline.csv", "data/online.csv")
