from utils.bq_query import get_bq_client
from sql.ratings_analys_query import query_genres_over_time as query
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('TkAgg')

client = get_bq_client()

query_job = client.query(query)

df = query_job.to_dataframe()

df_sorted = df.sort_values(["genre", "period_5yr"])

plt.figure(figsize=(12, 6))

for genre in df_sorted["genre"].unique():
    genre_df = df_sorted[df_sorted["genre"] == genre]
    plt.plot(genre_df["period_5yr"], genre_df["avg_rating"], label=genre, marker="o")

plt.xlabel("20-Year Period")
plt.ylabel("Average IMDb Rating")
plt.title("Genre Rating Trends Over Time (Top 5 Genres)")
plt.legend(title="Genre")
plt.grid(True, linestyle="--", alpha=0.3)
plt.tight_layout()
plt.savefig("../plots/genres_over_time.png", dpi=300)

plt.show()
