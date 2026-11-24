import yaml
import pandas as pd
from yaml import safe_load
import os 
from tqdm import tqdm


folder_path = r"E:\T20s international\data.yaml"

filenames = [
    os.path.join(folder_path, file)
    for file in os.listdir(folder_path)
    if file.endswith((".yaml", ".yml"))
]

all_dfs = []

for file_path in tqdm(filenames):
    with open(file_path, "r", encoding="utf-8") as file:
        data = yaml.safe_load(file)

    df = pd.json_normalize(data)
    all_dfs.append(df)

final_df = pd.concat(all_dfs, ignore_index=True)

print(final_df.head())
print("Final shape:", final_df.shape)

final_df.to_csv("t20_matches.csv", index=False)

















































