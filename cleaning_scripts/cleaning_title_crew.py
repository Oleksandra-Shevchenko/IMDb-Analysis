import pandas as pd

input_file = "../data/tsv/title.crew.tsv"
output_file = "../data/clean_csv/title.crew_clean.csv"

df = pd.read_csv(input_file, sep="\t", dtype=str, na_values=["\\N"], low_memory=False)

df.fillna("", inplace=True)

df = df[df["tconst"] != ""]

df["directors"] = df["directors"].replace("", "Unknown")
df["writers"] = df["writers"].replace("", "Unknown")

df.to_csv(output_file, index=False)
