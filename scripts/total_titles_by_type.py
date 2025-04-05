from utils.bq_query import get_bq_client
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('TkAgg')

client = get_bq_client()


query = """
    SELECT titleType, count(*) as count
    FROM `imdb-dataset-453510.IMDb_dataset.title_basics`
    GROUP BY titleType
    ORDER BY count DESC;
"""

# Выполняем запрос
query_job = client.query(query)

# Преобразуем результат в DataFrame
df = query_job.to_dataframe()

# Выводим первые строки
print(df)


# df — результат твоего запроса (titleType, count)
df_sorted = df.sort_values("count", ascending=False)

# 🔍 Фильтруем — убираем те, у кого слишком мало записей
df_filtered = df_sorted[df_sorted["count"] > 100_000].reset_index(drop=True)

print(df_filtered)
plt.figure(figsize=(10, 6))
plt.barh(df_filtered["titleType"], df_filtered["count"], color="skyblue")


for i, value in enumerate(df_filtered["count"]):
    if value >= 100_000:
        plt.text(
            value + 50_000,
            i,
            f'{value/1_000_000:.2f}M',
            va='center',
            fontsize=9
        )

plt.xlabel("Count")
plt.title("Distribution of Titles by Type")

plt.tight_layout()
plt.show()
