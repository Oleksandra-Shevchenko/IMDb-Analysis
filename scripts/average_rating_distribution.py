from utils.bq_query import get_bq_client
from sql.ratings_analys_query import average_rating_distribution as query
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use('TkAgg')

client = get_bq_client()
query_job = client.query(query)
df = query_job.to_dataframe()

plt.figure(figsize=(10, 5))
plt.bar(df["rating_bin"], df["num_titles"], width=0.4, color="royalblue")

for x, y in zip(df["rating_bin"], df["num_titles"]):
    plt.text(x, y + 100, f"{y:,}", ha='center', fontsize=8)

plt.title("Distribution of Average Ratings")
plt.xlabel("Average Rating (binned)")
plt.ylabel("Number of Titles")
plt.grid(axis='y', linestyle='--', alpha=0.5)
plt.xticks(df["rating_bin"])
plt.tight_layout()
plt.savefig("../plots/average_rating_hist.png", dpi=300)
plt.show()
