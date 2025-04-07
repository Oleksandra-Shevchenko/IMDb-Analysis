from utils.bq_query import get_bq_client
from sql.genre_query import query_movie_vs_series as query
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

pivot_df = df.pivot(index='genre', columns='titleType', values='count')

# Сохраняем порядок сортировки по сумме (он уже был в SQL)
pivot_df = pivot_df.loc[pivot_df.sum(axis=1).sort_values(ascending=False).index]

# Строим график
pivot_df.plot(kind='bar', figsize=(12, 6), width=0.7, color=["#4c72b0", "#dd8452"])

# Оформление
plt.title("Top 15 Genres by Count of Movies and TV Series")
plt.xlabel("Genre")
plt.ylabel("Number of Titles")
plt.xticks(rotation=45, ha='right')
plt.legend(title="Title Type")
plt.tight_layout()
plt.savefig("../plots/movies_vs_series_by_genres.png", dpi=300)

plt.show()