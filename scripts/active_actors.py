from utils.bq_query import get_bq_client
from sql.actors_analys_query import query_active as query
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

df_top = df.sort_values("film_count", ascending=True).tail(20)

plt.figure(figsize=(10, 8))
plt.barh(df_top["primaryName"], df_top["film_count"], color="teal")

# Подписи на столбиках
for i, value in enumerate(df_top["film_count"]):
    plt.text(value + 0.5, i, str(value), va='center', fontsize=9)

plt.title("Top 20 Most Active Leading Actors/Actresses")
plt.xlabel("Number of Movies (as Lead)")
plt.ylabel("Actor/Actress")
plt.tight_layout()
plt.savefig("../plots/top_active_actors.png", dpi=300)

plt.show()