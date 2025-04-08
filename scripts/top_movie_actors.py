from utils.bq_query import get_bq_client
from sql.actors_analys_query import query_top_movie_actors as query
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('TkAgg')

client = get_bq_client()
query_job = client.query(query)
df = query_job.to_dataframe()

df_sorted = df.sort_values("averageRating", ascending=True).reset_index(drop=True)

plt.figure(figsize=(10, 8))

y = df_sorted.index
x = df_sorted["averageRating"]

plt.scatter(x, y, color="mediumseagreen", s=60)

for i, row in df_sorted.iterrows():
    plt.text(
        row["averageRating"] + 0.01,
        i,
        f'{row["actor_name"]} — "{row["primaryTitle"]}"',
        va='center',
        fontsize=8
    )

plt.xlabel("IMDb Rating")
plt.yticks([])
plt.title("Top 10 Highest Rated Movies — Lead Actor & Film")
plt.grid(axis='x', linestyle='--', alpha=0.4)
plt.tight_layout()
plt.savefig("../plots/top_movie_actors.png", dpi=300)

plt.show()
