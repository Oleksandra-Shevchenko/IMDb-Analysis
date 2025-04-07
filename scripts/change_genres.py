from utils.bq_query import get_bq_client
from sql.ratings_analys_query import query_genres_over_time as query
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('TkAgg')

client = get_bq_client()

# Выполняем запрос
query_job = client.query(query)

# Преобразуем результат в DataFrame
df = query_job.to_dataframe()

# Выводим первые строки
print(df)

# df = твой DataFrame с колонками genre, period_5yr, avg_rating
df_sorted = df.sort_values(["genre", "period_5yr"])

# 🎨 Строим график
plt.figure(figsize=(12, 6))

# Поочередно рисуем линии для каждого жанра
for genre in df_sorted["genre"].unique():
    genre_df = df_sorted[df_sorted["genre"] == genre]
    plt.plot(genre_df["period_5yr"], genre_df["avg_rating"], label=genre, marker="o")

plt.xlabel("20-Year Period")
plt.ylabel("Average IMDb Rating")
plt.title("Genre Rating Trends Over Time (Top 5 Genres)")
plt.legend(title="Genre")
plt.grid(True, linestyle="--", alpha=0.3)
plt.tight_layout()
plt.savefig("../plots/genres_over_time.png", dpi=300)

plt.show()