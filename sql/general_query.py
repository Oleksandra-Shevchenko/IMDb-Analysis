# Distribution by year of production

# By decades
query_decade = """
SELECT
  CAST(SAFE_CAST(startYear AS INT64) / 10 AS INT64) * 10 AS decade,
  COUNT(*) AS num_titles
FROM `imdb-dataset-453510.IMDb_dataset.title_with_ratings`
WHERE SAFE_CAST(startYear AS INT64) IS NOT NULL
  AND SAFE_CAST(startYear AS INT64) BETWEEN 1900 AND 2025
GROUP BY decade
ORDER BY decade;

"""

# Average runtime
query_average = """
SELECT titleType, round(avg(runtimeMinutes),2) as average 
FROM `imdb-dataset-453510.IMDb_dataset.title_with_ratings` 
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
  SELECT averageRating, genres
  FROM `imdb-dataset-453510.IMDb_dataset.title_with_ratings` 
  WHERE genres IS NOT NULL
  and numVotes >=100000
)
JOIN UNNEST(SPLIT(genres, ',')) AS genre
GROUP BY genre
having count(*) >=100
ORDER BY avg_rating DESC
LIMIT 10;
"""
