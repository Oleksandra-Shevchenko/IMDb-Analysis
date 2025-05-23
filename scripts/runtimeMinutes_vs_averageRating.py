from utils.bq_query import get_bq_client
from sql.ratings_analys_query import runtimeMinutes_vs_averageRating as query
import matplotlib.pyplot as plt

import matplotlib

matplotlib.use('TkAgg')

client = get_bq_client()
query_job = client.query(query)
df = query_job.to_dataframe()

plt.figure(figsize=(10, 6))
plt.scatter(df["runtime_bin"], df["avg_rating"], alpha=0.5, color="royalblue", edgecolor="k")

plt.title("Runtime vs Average IMDb Rating")
plt.xlabel("Runtime (minutes)")
plt.ylabel("Average IMDb Rating")
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()

plt.savefig("../plots/runtime_vs_rating.png", dpi=300)
plt.show()
