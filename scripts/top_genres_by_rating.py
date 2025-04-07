from utils.bq_query import get_bq_client
from sql.general_query import query_top_genres as query
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


df_sorted = df.sort_values("avg_rating", ascending=True)

plt.figure(figsize=(10, 6))
plt.barh(df_sorted["genre"], df_sorted["avg_rating"], color="mediumslateblue")

for i, value in enumerate(df_sorted["avg_rating"]):
    plt.text(value + 0.02, i, f'{value:.2f}', va='center', fontsize=9)

plt.xlabel("Average Rating")
plt.xlim(6, 10)
plt.title("Average IMDb Rating by Genre")
plt.tight_layout()
plt.savefig("../plots/top_genres_by_rating.png", dpi=300)

plt.show()
