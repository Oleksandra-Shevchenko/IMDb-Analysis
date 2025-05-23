import pandas as pd
import os

input_folder = "data/tsv"
output_folder = "data/clean_csv"
os.makedirs(output_folder, exist_ok=True)

file_name = "name.basics.tsv"
file_path = os.path.join(input_folder, file_name)

df = pd.read_csv(file_path, sep="\t", dtype=str, na_values=["\\N"], low_memory=False)

df.fillna("Unknown", inplace=True)

numeric_columns = ["birthYear", "deathYear"]
for col in numeric_columns:
    df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(int)

output_file = os.path.join(output_folder, "name.basics_clean.csv")
df.to_csv(output_file, index=False)

