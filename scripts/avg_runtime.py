import matplotlib.pyplot as plt
from utils.bq_query import get_bq_client
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('TkAgg')

client = get_bq_client()

query = """
SELECT titleType, round(avg(runtimeMinutes),2) as average 
FROM `imdb-dataset-453510.IMDb_dataset.title_basics` 
where runtimeMinutes != 0 
group by titleType

"""

# Выполняем запрос
query_job = client.query(query)

# Преобразуем результат в DataFrame
df = query_job.to_dataframe()

print(df)

# df — DataFrame из запроса (titleType, average)
df_sorted = df.sort_values("average", ascending=True)

plt.figure(figsize=(10, 6))
plt.barh(df_sorted["titleType"], df_sorted["average"], color="mediumseagreen")

# Подписи на полосах
for i, value in enumerate(df_sorted["average"]):
    plt.text(value + 2, i, f'{value:.1f} min', va='center', fontsize=9)

plt.title("Average Runtime by Title Type")
plt.xlabel("Average Runtime (minutes)")
plt.ylabel("Title Type")
plt.tight_layout()
plt.savefig("../plots/runtime_by_type.png", dpi=300)

plt.show()

