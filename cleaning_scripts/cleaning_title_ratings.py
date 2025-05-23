import pandas as pd

input_file = "../data/tsv/title.ratings.tsv"
output_file = "../data/clean_csv/title.ratings_clean.csv"

df = pd.read_csv(input_file, sep="\t", dtype=str, na_values=["\\N"], low_memory=False)

df.fillna("", inplace=True)

df = df[df["tconst"] != ""]

df["averageRating"] = pd.to_numeric(df["averageRating"], errors="coerce").fillna(0.0)

df["numVotes"] = pd.to_numeric(df["numVotes"], errors="coerce").fillna(0).astype(int)

df.to_csv(output_file, index=False)
