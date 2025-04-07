from utils.bq_query import get_bq_client
from sql.ratings_analys_query import query_top_films as query
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


# 👇 Объединяем название и год для Y-оси
df["label"] = df["movie_name"] + " (" + df["year"].astype(str) + ")"

# Сортируем от меньшего к большему для красивого отображения
df_sorted = df.sort_values("rating", ascending=True)

plt.figure(figsize=(10, 6))

bars = plt.barh(df_sorted["label"], df_sorted["rating"], color="slateblue")

# Добавим подписи рейтингов на правом краю
for bar, rating in zip(bars, df_sorted["rating"]):
    plt.text(
        bar.get_width() + 0.05,
        bar.get_y() + bar.get_height() / 2,
        f"{rating:.2f}",
        va='center',
        fontsize=9
    )

plt.xlabel("IMDb Rating")
plt.title("Top 10 Highest-Rated Movies")
plt.xlim(8, 10)  # т.к. IMDb максимум — 10
plt.tight_layout()
plt.savefig("../plots/top_films.png", dpi=300)

plt.show()