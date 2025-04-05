import pandas as pd

# 📂 Пути к файлам
input_file = "../data/tsv/title.crew.tsv"
output_file = "../data/clean_csv/title.crew_clean.csv"

# Загружаем TSV
df = pd.read_csv(input_file, sep="\t", dtype=str, na_values=["\\N"], low_memory=False)

# 🔹 1. Заполняем отсутствующие значения
df.fillna("", inplace=True)

# 🔹 2. Проверяем, что `tconst` заполнен
df = df[df["tconst"] != ""]

# 🔹 3. Обрабатываем `directors` и `writers`
df["directors"] = df["directors"].replace("", "Unknown")  # Если нет режиссёра → Unknown
df["writers"] = df["writers"].replace("", "Unknown")  # Если нет сценариста → Unknown

# 🔹 4. Сохраняем очищенный файл
df.to_csv(output_file, index=False)

print(f"✅ Файл очищен и сохранён в {output_file}!")
