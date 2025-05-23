from utils.bq_query import get_bq_client
from sql.ratings_analys_query import genre_share_by_decade as query
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use('TkAgg')

client = get_bq_client()
query_job = client.query(query)
df = query_job.to_dataframe()

pivot_df = df.pivot_table(
    index="period_20yr",
    columns="genre",
    values="genre_share_percent",
    fill_value=0
).sort_index()

custom_colors = [
    "#1f77b4",
    "#ff7f0e",
    "#2ca02c",
    "#d62728",
    "#9467bd",
]

ax = pivot_df.plot(
    kind='bar',
    stacked=True,
    figsize=(12, 6),
    color=custom_colors[:len(pivot_df.columns)],
    width=0.85
)

plt.title("Genre Popularity Over Time (% of Total Films)", fontsize=14)
plt.xlabel("20-Year Period", fontsize=12)
plt.ylabel("Genre Share (%)", fontsize=12)
plt.xticks(rotation=45, fontsize=10)
plt.yticks(fontsize=10)
plt.grid(axis='y', linestyle='--', alpha=0.5)

plt.legend(
    title="Genre",
    title_fontsize=11,
    fontsize=10,
    bbox_to_anchor=(1.02, 1),
    loc='upper left'
)

plt.tight_layout()
plt.savefig("../plots/genre_share_by_period_colored.png", dpi=300)
plt.show()
