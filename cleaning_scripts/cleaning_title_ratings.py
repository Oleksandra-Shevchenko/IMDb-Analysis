import pandas as pd

# 📂 Пути к файлам
input_file = "../data/tsv/title.ratings.tsv"
output_file = "../data/clean_csv/title.ratings_clean.csv"

# Загружаем TSV
df = pd.read_csv(input_file, sep="\t", dtype=str, na_values=["\\N"], low_memory=False)

# 🔹 1. Заполняем отсутствующие значения
df.fillna("", inplace=True)

# 🔹 2. Проверяем, что `tconst` заполнен
df = df[df["tconst"] != ""]

# 🔹 3. Преобразуем `averageRating` в `float`, если есть ошибки → 0.0
df["averageRating"] = pd.to_numeric(df["averageRating"], errors="coerce").fillna(0.0)

# 🔹 4. Преобразуем `numVotes` в `int`, если есть ошибки → 0
df["numVotes"] = pd.to_numeric(df["numVotes"], errors="coerce").fillna(0).astype(int)

# 🔹 5. Сохраняем очищенный файл
df.to_csv(output_file, index=False)

print(f"✅ Файл очищен и сохранён в {output_file}!")
