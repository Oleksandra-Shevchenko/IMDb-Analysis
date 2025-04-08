from utils.bq_query import get_bq_client
from sql.general_query import query_total as query
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('TkAgg')

client = get_bq_client()
query_job = client.query(query)
df = query_job.to_dataframe()

df_sorted = df.sort_values("count", ascending=False)

df_filtered = df_sorted[df_sorted["count"] > 100_000].reset_index(drop=True)

plt.figure(figsize=(10, 6))
plt.barh(df_filtered["titleType"], df_filtered["count"], color="skyblue")

for i, value in enumerate(df_filtered["count"]):
    if value >= 100_000:
        plt.text(
            value + 50_000,
            i,
            f'{value/1_000_000:.2f}M',
            va='center',
            fontsize=9
        )

plt.xlabel("Count")
plt.title("Distribution of Titles by Type")

plt.tight_layout()
plt.savefig("../plots/general_count.png", dpi=300)

plt.show()
