from utils.bq_query import get_bq_client
from sql.director_analys_query import query_directors_films as query
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

df_sorted = df.sort_values("film_count", ascending=True)

plt.figure(figsize=(10, 6))

# Горизонтальные полосы
plt.barh(df_sorted["primaryName"], df_sorted["film_count"], color="steelblue")

# Подписи количества справа от полос
for i, value in enumerate(df_sorted["film_count"]):
    plt.text(value + 0.5, i, str(value), va='center', fontsize=9)

# Подписи осей и заголовок
plt.xlabel("Number of Directed Films")
plt.title("Top 10 Most Active Directors")

# Аккуратное размещение
plt.tight_layout()
plt.savefig("../plots/directors_films.png", dpi=300)

plt.show()