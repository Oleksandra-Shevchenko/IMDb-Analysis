# General statistics and  overview

# The total number of movies and TV series
query_total = """
    SELECT titleType, count(*) as count
    FROM `imdb-dataset-453510.IMDb_dataset.title_basics`
    GROUP BY titleType
    ORDER BY count DESC;
"""

# Distribution by year of production

# By decades
query_decade = """
SELECT
  CAST(SAFE_CAST(startYear AS INT64) / 10 AS INT64) * 10 AS decade,
  COUNT(*) AS num_titles
FROM `imdb-dataset-453510.IMDb_dataset.title_basics`
WHERE SAFE_CAST(startYear AS INT64) IS NOT NULL
GROUP BY decade
ORDER BY decade;
"""

# Average runtime
query_average = """
SELECT titleType, round(avg(runtimeMinutes),2) as average 
FROM `imdb-dataset-453510.IMDb_dataset.title_basics` 
where runtimeMinutes != 0 
group by titleType

"""

# Top 10 Genres by Average Rating
query_top_genres = """

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
ORDER BY avg_rating DESC
LIMIT 10;
"""
