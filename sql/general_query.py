# 📊 1. Общая статистика и overview

# Сколько всего фильмов и сериалов в базе
query = """
    SELECT titleType, count(*) as count
    FROM `imdb-dataset-453510.IMDb_dataset.title_basics`
    GROUP BY titleType
    ORDER BY count DESC;
"""

# Распределение по годам выпуска
# Вариант A — по годам

query1 = """SELECT startYear, COUNT(*) AS num_titles
FROM `imdb-dataset-453510.IMDb_dataset.title_basics`
WHERE startYear IS NOT NULL
GROUP BY startYear
ORDER BY startYear;
"""

# Вариант B — по десятилетиям
query2 = """
SELECT
  CAST(SAFE_CAST(startYear AS INT64) / 10 AS INT64) * 10 AS decade,
  COUNT(*) AS num_titles
FROM `imdb-dataset-453510.IMDb_dataset.title_basics`
WHERE SAFE_CAST(startYear AS INT64) IS NOT NULL
GROUP BY decade
ORDER BY decade;
"""

# Средняя продолжительность фильмов/серий
query3 = """
SELECT titleType, round(avg(runtimeMinutes),2) as average 
FROM `imdb-dataset-453510.IMDb_dataset.title_basics` 
where runtimeMinutes != 0 
group by titleType

"""

# Топ жанры по средней оценке

query4 = """

SELECT 
  genre,
  COUNT(*) AS count,
  ROUND(AVG(averageRating), 2) AS avg_rating
FROM (
  SELECT r.averageRating, t.genres
  FROM `imdb-dataset-453510.IMDb_dataset.title_basics` AS t
  JOIN `imdb-dataset-453510.IMDb_dataset.title_ratings` AS r
    ON r.tconst = t.tconst
  WHERE t.genres IS NOT NULL
)
JOIN UNNEST(SPLIT(genres, ',')) AS genre
GROUP BY genre
ORDER BY avg_rating DESC;

"""
