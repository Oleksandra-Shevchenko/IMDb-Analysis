from utils.bq_query import get_bq_client
from sql.director_analys_query import query_top_directors as query
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('TkAgg')

client = get_bq_client()
query_job = client.query(query)
df = query_job.to_dataframe()

plt.figure(figsize=(10, 6))
bars = plt.barh(df["primaryName"], df["avg_rating"], color="seagreen")

for bar, rating in zip(bars, df["avg_rating"]):
    plt.text(
        bar.get_width() + 0.01,
        bar.get_y() + bar.get_height() / 2,
        f"{rating:.2f}",
        va='center',
        fontsize=9
    )

plt.xlim(8.5, 9.4)
plt.xlabel("Average IMDb Rating")
plt.title("Top 10 Highest-Rated Directors")
plt.tight_layout()
plt.savefig("../plots/top_rated_directors.png", dpi=300)

plt.show()
