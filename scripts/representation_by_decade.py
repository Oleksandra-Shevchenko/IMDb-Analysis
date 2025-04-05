from utils.bq_query import get_bq_client
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('TkAgg')

client = get_bq_client()


query = """
SELECT
    CAST(CAST(startYear AS INT64) / 10 AS INT64) * 10 AS decade,
    COUNT(*) AS num_titles
FROM `imdb-dataset-453510.IMDb_dataset.title_basics`
WHERE startYear IS NOT NULL
  AND startYear >= 1900
GROUP BY decade
ORDER BY decade;

"""

# Выполняем запрос
query_job = client.query(query)

# Преобразуем результат в DataFrame
df = query_job.to_dataframe()

# Выводим первые строки
print(df)

# Строим линейный график
plt.figure(figsize=(10, 5))
plt.plot(df["decade"], df["num_titles"], marker="o", linestyle="-", color="royalblue")

for x, y in zip(df["decade"], df["num_titles"]):
    plt.text(x, y + 100_000, f'{y:,}', ha='center', fontsize=9)


# Подписи и оформление
plt.xticks(df["decade"])
plt.title("Number of Titles by Decade")
plt.xlabel("Decade")
plt.ylabel("Number of Titles")
plt.grid(True)
plt.tight_layout()
plt.show()
