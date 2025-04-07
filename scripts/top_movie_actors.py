from utils.bq_query import get_bq_client
from sql.actors_analys_query import query_top_movie_actors as query
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

# Сортируем по рейтингу
df_sorted = df.sort_values("averageRating", ascending=True).reset_index(drop=True)

plt.figure(figsize=(10, 8))

# Координаты по оси Y — просто индексы
y = df_sorted.index
x = df_sorted["averageRating"]

# Строим точки
plt.scatter(x, y, color="mediumseagreen", s=60)

# Подписи справа от каждой точки
for i, row in df_sorted.iterrows():
    plt.text(
        row["averageRating"] + 0.01,
        i,
        f'{row["actor_name"]} — "{row["primaryTitle"]}"',
        va='center',
        fontsize=8
    )

plt.xlabel("IMDb Rating")
plt.yticks([])  # Убираем ось Y, чтобы не засорять
plt.title("Top 10 Highest Rated Movies — Lead Actor & Film")
plt.grid(axis='x', linestyle='--', alpha=0.4)
plt.tight_layout()
plt.savefig("../plots/top_movie_actors.png", dpi=300)

plt.show()
