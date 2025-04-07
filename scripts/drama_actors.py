from utils.bq_query import get_bq_client
from sql.actors_analys_query import query_drama_actors as query
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

df_sorted = df.sort_values("num_drama_titles", ascending=False).reset_index(drop=True)

plt.figure(figsize=(12, 4))

# X — просто индекс (чтобы равномерно расположить круги)
x = range(len(df_sorted))
y = [1] * len(df_sorted)  # Все на одной линии

# Рисуем пузырьки
sizes = [n * 30 for n in df_sorted["num_drama_titles"]]  # масштабируем размер
plt.scatter(
    x, y,
    s=sizes,
    c=df_sorted["num_drama_titles"],  # теперь цвет зависит от кол-ва драм
    cmap="Blues",
    edgecolors="black",
    alpha=0.7
)

# Подписи имён под пузырьками
for i, row in df_sorted.iterrows():
    plt.text(
        x[i],
        y[i] - 0.08,
        row["primaryName"],
        ha="center",
        fontsize=9
    )
    plt.text(
        x[i],
        y[i] + 0.08,
        f'{row["num_drama_titles"]} dramas',
        ha="center",
        fontsize=8,
        color='gray'
    )

# Убираем оси и лишнее
plt.xticks([])
plt.yticks([])
plt.title("Top 10 Actors/Actresses by Number of Drama Movies", fontsize=14)
plt.box(False)
plt.tight_layout()
plt.savefig("../plots/drama_actors.png", dpi=300)

plt.show()
