# ⭐ 2. Анализ оценок

# 🎯 1. Фильмы/сериалы с наивысшими рейтингами и большим числом голосов (например, > 10,000)

query = """
SELECT 
  t.primaryTitle as movie_name,
  t.startYear as year,
  r.averageRating as rating,
  r.numVotes
FROM `imdb-dataset-453510.IMDb_dataset.title_basics` AS t
JOIN `imdb-dataset-453510.IMDb_dataset.title_ratings` AS r
  ON r.tconst = t.tconst
WHERE r.numVotes >= 10000 AND t.titleType = 'movie'
ORDER BY r.averageRating DESC
LIMIT 50;
"""

# 📈 2. Связь между оценкой и количеством голосов (корреляция, выбросы)

query2 = """
SELECT 
  r.averageRating,
  r.numVotes
FROM `imdb-dataset-453510.IMDb_dataset.title_ratings` AS r
WHERE r.numVotes > 100  -- уберём мусор с 5-10 голосами

"""


# изменение рейтинговых трендов с годами

query5 = """
-- Шаг 1: Находим 5 самых популярных жанров (по количеству фильмов)
WITH top_5_genres AS (
  SELECT genre
  FROM (
    SELECT 
      genre, 
      COUNT(*) AS total_titles
    FROM `imdb-dataset-453510.IMDb_dataset.title_basics` AS t
    JOIN UNNEST(SPLIT(t.genres, ',')) AS genre
    WHERE genre IS NOT NULL
    GROUP BY genre
    ORDER BY total_titles DESC
    LIMIT 5
  )
),

-- Шаг 2: Расчёт среднего рейтинга по жанрам и 5-леткам
genre_rating_by_period AS (
  SELECT 
    genre,
    CAST(SAFE_CAST(t.startYear AS INT64) / 5 AS INT64) * 5 AS period_5yr,
    ROUND(AVG(r.averageRating), 2) AS avg_rating,
    COUNT(*) AS num_titles
  FROM `imdb-dataset-453510.IMDb_dataset.title_basics` AS t
  JOIN `imdb-dataset-453510.IMDb_dataset.title_ratings` AS r
    ON r.tconst = t.tconst
  JOIN UNNEST(SPLIT(t.genres, ',')) AS genre
  WHERE t.startYear BETWEEN 1900 AND 2025
  GROUP BY genre, period_5yr
  HAVING COUNT(*) >= 10
)

-- Шаг 3: Фильтрация только по топ-5 жанрам
SELECT 
  g.genre,
  g.period_5yr,
  g.avg_rating
FROM genre_rating_by_period g
JOIN top_5_genres t5 ON g.genre = t5.genre
ORDER BY g.genre, g.period_5yr;

"""