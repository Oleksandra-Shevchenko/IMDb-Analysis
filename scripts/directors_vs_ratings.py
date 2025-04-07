from utils.bq_query import get_bq_client
from sql.director_analys_query import query_directors_vs_ratings as query
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

colors = ["#2E8B57", "#87CEEB"]  # зелёный и голубой

plt.figure(figsize=(6, 4))
bars = plt.bar(df["status"], df["avg_director_rating"], color=colors)

# Добавим подписи сверху
for bar, rating in zip(bars, df["avg_director_rating"]):
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 0.05,
        f"{rating:.2f}",
        ha='center',
        fontsize=10
    )

plt.ylim(0, 10)
plt.ylabel("Average IMDb Rating")
plt.title("Average Rating: Famous vs Regular Directors")
plt.tight_layout()
plt.savefig("../plots/directors_vs_ratings.png", dpi=300)

plt.show()