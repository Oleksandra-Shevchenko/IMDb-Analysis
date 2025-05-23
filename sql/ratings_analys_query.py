# Rating analysis
# Correlation between ratings and votes
query_correlation_ratings_votes = """
SELECT 
  r.averageRating,
  r.numVotes
FROM `imdb-dataset-453510.IMDb_dataset.title_with_ratings` AS r
WHERE r.numVotes > 1000000
"""


# Genres over time
query_genres_over_time = """
WITH top_5_genres AS (
  SELECT genre
  FROM (
    SELECT 
      genre, 
      COUNT(*) AS total_titles
    FROM `imdb-dataset-453510.IMDb_dataset.title_with_ratings` AS t
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
    CAST(SAFE_CAST(startYear AS INT64) / 20 AS INT64) * 20 AS period_5yr,
    ROUND(AVG(averageRating), 2) AS avg_rating,
    COUNT(*) AS num_titles,
  
  FROM `imdb-dataset-453510.IMDb_dataset.title_with_ratings`
  JOIN UNNEST(SPLIT(genres, ',')) AS genre
  WHERE startYear BETWEEN 1900 AND 2025
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

#Share of genres as a percentage of total films
genre_share_by_decade = """
WITH top_5_genres AS (
  SELECT genre
  FROM (
    SELECT genre, COUNT(*) AS total
    FROM `imdb-dataset-453510.IMDb_dataset.title_with_ratings`,
         UNNEST(SPLIT(genres, ',')) AS genre
    WHERE startYear BETWEEN 1900 AND 2025
    GROUP BY genre
    ORDER BY total DESC
    LIMIT 5
  )
),

 all_films_by_decade AS (
  select count(*) as count_of_films,
  CAST(SAFE_CAST(startYear AS INT64) / 20 AS INT64) * 20 AS period_20yr,
  from `imdb-dataset-453510.IMDb_dataset.title_with_ratings`
  WHERE startYear BETWEEN 1900 AND 2025
  GROUP BY period_20yr
),

count_genres_by_decade AS (
  SELECT 
    genre, 
    COUNT(*) AS count_by_genre,
    CAST(SAFE_CAST(startYear AS INT64) / 20 AS INT64) * 20 AS period_20yr
  FROM `imdb-dataset-453510.IMDb_dataset.title_with_ratings`
  JOIN UNNEST(SPLIT(genres, ',')) AS genre
  WHERE startYear BETWEEN 1900 AND 2025
  GROUP BY genre, period_20yr
)


SELECT 
  c.genre, 
  c.period_20yr,
  ROUND(c.count_by_genre * 100.0 / a.count_of_films, 2) AS genre_share_percent
FROM count_genres_by_decade c
JOIN all_films_by_decade a ON c.period_20yr = a.period_20yr
JOIN top_5_genres t ON c.genre = t.genre
ORDER BY c.genre, c.period_20yr;


"""

# Show how movie ratings are distributed.
average_rating_distribution = """
SELECT
  ROUND(averageRating * 2) / 2 AS rating_bin,
  COUNT(*) AS num_titles
FROM `imdb-dataset-453510.IMDb_dataset.title_with_ratings`
WHERE averageRating IS NOT NULL
GROUP BY rating_bin
ORDER BY rating_bin;

"""

# Show how skewed the distribution of vote counts is.
num_votes_distribution = """
SELECT
  CASE
    WHEN numVotes < 10 THEN '<10'
    WHEN numVotes BETWEEN 10 AND 99 THEN '10-99'
    WHEN numVotes BETWEEN 100 AND 999 THEN '100-999'
    WHEN numVotes BETWEEN 1000 AND 9999 THEN '1K-9K'
    WHEN numVotes BETWEEN 10000 AND 99999 THEN '10K-99K'
    WHEN numVotes BETWEEN 100000 AND 999999 THEN '100K-999K'
    ELSE '1M+'
  END AS vote_bin,
  COUNT(*) AS num_titles
FROM `imdb-dataset-453510.IMDb_dataset.title_with_ratings`
GROUP BY vote_bin
ORDER BY
  CASE vote_bin
    WHEN '<10' THEN 1
    WHEN '10-99' THEN 2
    WHEN '100-999' THEN 3
    WHEN '1K-9K' THEN 4
    WHEN '10K-99K' THEN 5
    WHEN '100K-999K' THEN 6
    ELSE 7
  END;
"""

# Does the runtime of a film (runtimeMinutes) affect its average rating (averageRating)?
runtimeMinutes_vs_averageRating = """
SELECT
  CAST(runtimeMinutes / 10 AS INT64) * 10 AS runtime_bin,
  COUNT(*) AS num_titles,
  ROUND(AVG(averageRating), 2) AS avg_rating
FROM `imdb-dataset-453510.IMDb_dataset.title_with_ratings`
WHERE runtimeMinutes BETWEEN 30 AND 240 
GROUP BY runtime_bin
ORDER BY runtime_bin;

"""

# Does the runtime of a film (runtimeMinutes) affect the number of votes (numVotes)?
runtimeMinutes_vs_numVotes = """
SELECT
  CAST(runtimeMinutes / 10 AS INT64) * 10 AS runtime_bin,
  COUNT(*) AS num_titles,
  ROUND(AVG(numVotes), 2) AS avg_votes
FROM `imdb-dataset-453510.IMDb_dataset.title_with_ratings`
WHERE runtimeMinutes BETWEEN 30 AND 240
GROUP BY runtime_bin
ORDER BY runtime_bin;

"""