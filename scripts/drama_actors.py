from utils.bq_query import get_bq_client
from sql.actors_analys_query import query_drama_actors as query
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('TkAgg')

client = get_bq_client()
query_job = client.query(query)
df = query_job.to_dataframe()

df_sorted = df.sort_values("num_drama_titles", ascending=False).reset_index(drop=True)

plt.figure(figsize=(12, 4))

x = range(len(df_sorted))
y = [1] * len(df_sorted)

sizes = [n * 30 for n in df_sorted["num_drama_titles"]]
plt.scatter(
    x, y,
    s=sizes,
    c=df_sorted["num_drama_titles"],
    cmap="Blues",
    edgecolors="black",
    alpha=0.7
)

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


plt.xticks([])
plt.yticks([])
plt.title("Top 10 Actors/Actresses by Number of Drama Movies", fontsize=14)
plt.box(False)
plt.tight_layout()
plt.savefig("../plots/drama_actors.png", dpi=300)

plt.show()
