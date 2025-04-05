import pandas as pd
import os

# Папки
input_folder = "data/tsv"
output_folder = "data/clean_csv"
os.makedirs(output_folder, exist_ok=True)

# Загрузка
file_name = "title.basics.tsv"
file_path = os.path.join(input_folder, file_name)
df = pd.read_csv(file_path, sep="\t", dtype=str, na_values=["\\N"], low_memory=False)

# Числовые колонки
numeric_columns = ["isAdult", "startYear", "endYear", "runtimeMinutes"]
for col in numeric_columns:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(int)

# Строковые колонки
string_columns = ["tconst", "titleType", "primaryTitle", "originalTitle", "genres"]
for col in string_columns:
    if col in df.columns:
        df[col] = df[col].fillna("Unknown")

# Сохранение
output_file = os.path.join(output_folder, "title.basics_clean.csv")
df.to_csv(output_file, index=False)
