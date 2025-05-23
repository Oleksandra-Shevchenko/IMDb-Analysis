import pandas as pd

input_file = "../data/tsv/title.principals.tsv"
output_file = "../data/clean_csv/title.principals_clean.csv"

df = pd.read_csv(input_file, sep="\t", dtype=str, na_values=["\\N"], low_memory=False)

df.fillna("", inplace=True)

df = df[(df["tconst"] != "") & (df["nconst"] != "")]

df["ordering"] = pd.to_numeric(df["ordering"], errors="coerce").fillna(0).astype(int)

df["job"] = df["job"].replace("", "Unknown")
df["characters"] = df["characters"].replace("", "Unknown")

df.to_csv(output_file, index=False)
