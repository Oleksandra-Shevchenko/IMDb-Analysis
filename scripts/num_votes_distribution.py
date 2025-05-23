from utils.bq_query import get_bq_client
from sql.ratings_analys_query import num_votes_distribution as query
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use('TkAgg')

client = get_bq_client()
query_job = client.query(query)
df = query_job.to_dataframe()

plt.figure(figsize=(10, 5))
plt.bar(df["vote_bin"], df["num_titles"], width=0.6, color="#2ca02c")

for x, y in zip(df["vote_bin"], df["num_titles"]):
    plt.text(x, y + 100, f"{y:,}", ha='center', fontsize=8)

plt.title("Distribution of Number of Votes (Log Scale Bins)")
plt.xlabel("Vote Count Bin")
plt.ylabel("Number of Titles")
plt.grid(axis='y', linestyle='--', alpha=0.5)
plt.tight_layout()
plt.savefig("../plots/num_votes_log_bins.png", dpi=300)
plt.show()
