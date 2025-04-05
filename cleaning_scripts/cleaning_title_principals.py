import pandas as pd

# 📂 Пути к файлам
input_file = "../data/tsv/title.principals.tsv"
output_file = "../data/clean_csv/title.principals_clean.csv"

# Загружаем TSV
df = pd.read_csv(input_file, sep="\t", dtype=str, na_values=["\\N"], low_memory=False)

# 🔹 1. Заполняем отсутствующие значения
df.fillna("", inplace=True)

# 🔹 2. Проверяем, что `tconst` и `nconst` заполнены
df = df[(df["tconst"] != "") & (df["nconst"] != "")]

# 🔹 3. Преобразуем `ordering` в `int`, если есть ошибки → 0
df["ordering"] = pd.to_numeric(df["ordering"], errors="coerce").fillna(0).astype(int)

# 🔹 4. Очищаем `job` и `characters`
df["job"] = df["job"].replace("", "Unknown")  # Если нет должности → Unknown
df["characters"] = df["characters"].replace("", "Unknown")  # Если нет персонажа → Unknown

# 🔹 5. Сохраняем очищенный файл
df.to_csv(output_file, index=False)

print(f"✅ Файл очищен и сохранён в {output_file}!")
