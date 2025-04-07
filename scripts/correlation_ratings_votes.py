# from utils.bq_query import get_bq_client
# from sql.ratings_analys_query import query_correlation_ratings_votes as query
# import matplotlib
# import matplotlib.pyplot as plt
# import matplotlib.ticker as ticker
# from scipy.stats import linregress
# import numpy as np
# matplotlib.use('TkAgg')
#
# client = get_bq_client()
#
# # Выполняем запрос
# query_job = client.query(query)
#
# # Преобразуем результат в DataFrame
# df = query_job.to_dataframe()
#
# # Выводим первые строки
# print(df)
#
# # 🔹 Логарифмируем количество голосов (потому что разброс большой)
# df["log_votes"] = np.log10(df["numVotes"])
#
# # 🔹 Линейная регрессия
# slope, intercept, r_value, p_value, std_err = linregress(df["log_votes"], df["averageRating"])
# regression_line = slope * df["log_votes"] + intercept
#
# # 🔹 Строим график
# plt.figure(figsize=(10, 6))
# plt.scatter(df["numVotes"], df["averageRating"], alpha=0.5, color="teal", edgecolors='w', s=50, label="Movies")
# plt.plot(df["numVotes"], regression_line, color="crimson", linewidth=2, label=f"Trend line (r = {r_value:.2f})")
#
#
# plt.xscale("log")
# plt.gca().xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{x/1e6:.0f}M'))
#
# plt.xlabel("Number of Votes (log scale)")
# plt.ylabel("Average IMDb Rating")
# plt.title("IMDb Rating vs Number of Votes")
# plt.legend()
# plt.grid(True, linestyle='--', alpha=0.3)
# plt.tight_layout()
# plt.show()

from utils.bq_query import get_bq_client
from sql.ratings_analys_query import query_correlation_ratings_votes as query
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from scipy.stats import linregress
matplotlib.use('TkAgg')

client = get_bq_client()

query_job = client.query(query)
df = query_job.to_dataframe()
print(df)

slope, intercept, r_value, _, _ = linregress(df["numVotes"], df["averageRating"])
regression_line = slope * df["numVotes"] + intercept

plt.figure(figsize=(10, 6))
plt.scatter(df["numVotes"], df["averageRating"], alpha=0.5, color="teal", edgecolors='w', s=50, label="Movies")
plt.plot(df["numVotes"], regression_line, color="crimson", linewidth=2, label=f"Trend line (r = {r_value:.2f})")
plt.gca().xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{x/1_000_000:.1f}M'))


plt.xlabel("Number of Votes")
plt.ylabel("Average IMDb Rating")
plt.title("IMDb Rating vs Number of Votes")
plt.legend()
plt.grid(True, linestyle='--', alpha=0.3)
plt.tight_layout()
plt.savefig("../plots/correlation_ratings_votes.png", dpi=300)

plt.show()
