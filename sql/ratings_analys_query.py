# ⭐ 2. Rating analysis
# test
# top films
query_top_films = """
SELECT 
  t.primaryTitle as movie_name,
  t.startYear as year,
  r.averageRating as rating,
  r.numVotes
FROM `imdb-dataset-453510.IMDb_dataset.title_basics` AS t
JOIN `imdb-dataset-453510.IMDb_dataset.title_ratings` AS r
  ON r.tconst = t.tconst
WHERE r.numVotes >= 1000000 AND t.titleType = 'movie'
ORDER BY r.averageRating DESC
LIMIT 10;
"""

# 2.Correlation between ratings and votes
query_correlation_ratings_votes = """
SELECT 
  r.averageRating,
  r.numVotes
FROM `imdb-dataset-453510.IMDb_dataset.title_ratings` AS r
WHERE r.numVotes > 1000000
"""


# Genres over time

query_genres_over_time = """
-- Top 5 most popular genres
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

-- aversge rating by genre and 20 years gap
genre_rating_by_period AS (
  SELECT 
    genre,
    CAST(SAFE_CAST(t.startYear AS INT64) / 20 AS INT64) * 20 AS period_5yr,
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

-- filtered only 5 genres
SELECT 
  g.genre,
  g.period_5yr,
  g.avg_rating
FROM genre_rating_by_period g
JOIN top_5_genres t5 ON g.genre = t5.genre
ORDER BY g.genre, g.period_5yr;

"""