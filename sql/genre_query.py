# 5. Жанровый анализ
# фильмы какого жанра снималось больше всего

query = """
  WITH genre_counts AS (
  SELECT 
    CAST(SAFE_CAST(startYear AS INT64) / 5 AS INT64) * 5 AS period_5yr,
    genre,
    COUNT(*) AS num_titles
  FROM `imdb-dataset-453510.IMDb_dataset.title_basics` AS t
  JOIN UNNEST(SPLIT(genres, ',')) AS genre

  WHERE SAFE_CAST(startYear AS INT64) BETWEEN 1900 AND 2025
    AND titleType = 'movie'
    
  GROUP BY genre, period_5yr
  HAVING COUNT(*) >= 10
),
ranked AS (
  SELECT *,
    RANK() OVER (PARTITION BY period_5yr ORDER BY num_titles DESC) AS rank
  FROM genre_counts
)

SELECT *
FROM ranked
WHERE rank = 1
ORDER BY period_5yr

"""
# 2.Какие жанры получают наивысшие оценки?
query1 = """
SELECT 
  genre,
  round(avg(averageRating),2) as rating,
  COUNT(*) AS num_movies,
  SUM(r.numVotes) AS total_votes,
FROM `imdb-dataset-453510.IMDb_dataset.title_basics` AS t
  JOIN `imdb-dataset-453510.IMDb_dataset.title_ratings` AS r
    ON r.tconst = t.tconst
JOIN UNNEST(SPLIT(genres, ',')) AS genre
where r.numVotes >= 10000
and titleType = 'movie'
group by genre
having COUNT(*) >= 100
order by rating desc
limit 50
"""


# 3.В каких жанрах снимается больше всего фильмов/сериалов?
query2 = """
SELECT 
  genre,
  titleType,
  COUNT(*) AS count
FROM `imdb-dataset-453510.IMDb_dataset.title_basics`
JOIN UNNEST(SPLIT(genres, ',')) AS genre
WHERE titleType IN ('movie', 'tvSeries')
GROUP BY genre, titleType
ORDER BY genre, count DESC

"""