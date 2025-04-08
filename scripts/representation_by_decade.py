from utils.bq_query import get_bq_client
from sql.general_query import query_decade as query
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('TkAgg')

client = get_bq_client()
query_job = client.query(query)
df = query_job.to_dataframe()

plt.figure(figsize=(10, 5))
plt.plot(df["decade"], df["num_titles"], marker="o", linestyle="-", color="royalblue")

for x, y in zip(df["decade"], df["num_titles"]):
    plt.text(x, y + 100_000, f'{y:,}', ha='center', fontsize=9)

plt.xticks(df["decade"])
plt.title("Number of Titles by Decade")
plt.xlabel("Decade")
plt.ylabel("Number of Titles")
plt.grid(True)
plt.tight_layout()
plt.savefig("../plots/titles_by_decade.png", dpi=300)

plt.show()
