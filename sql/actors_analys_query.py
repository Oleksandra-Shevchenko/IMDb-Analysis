# Actors analysis

# 1. Most active actors
query_active = """
SELECT 
  n.primaryName,
  COUNT(DISTINCT b.tconst) AS film_count
FROM `imdb-dataset-453510.IMDb_dataset.title_principals` AS p
JOIN `imdb-dataset-453510.IMDb_dataset.name` AS n
  ON p.nconst = n.nconst
JOIN `imdb-dataset-453510.IMDb_dataset.title_basics` AS b
  ON p.tconst = b.tconst
WHERE p.category IN ('actor', 'actress')
  AND b.titleType IN ('movie', 'tvMovie') 
  AND p.ordering = 1
GROUP BY n.primaryName
HAVING film_count >= 10
ORDER BY film_count DESC
LIMIT 20;
"""

# 2. Top movie actors
query_top_movie_actors = """
SELECT 
  r.averageRating,
  r.numVotes,
  b.primaryTitle,
  n.primaryName AS actor_name
FROM `imdb-dataset-453510.IMDb_dataset.title_ratings` AS r
JOIN `imdb-dataset-453510.IMDb_dataset.title_basics` AS b
  ON r.tconst = b.tconst
JOIN `imdb-dataset-453510.IMDb_dataset.title_principals` AS p
  ON b.tconst = p.tconst
JOIN `imdb-dataset-453510.IMDb_dataset.name` AS n
  ON p.nconst = n.nconst
WHERE b.titleType = 'movie'
  AND r.numVotes >= 10000
  AND p.category IN ('actor', 'actress')
  AND p.ordering = 1

ORDER BY r.averageRating DESC
LIMIT 10;
"""

# 3. Actors in dramas
query_drama_actors = """
SELECT 
  n.primaryName,
  COUNT(*) AS num_drama_titles
FROM `imdb-dataset-453510.IMDb_dataset.title_principals` AS p
JOIN `imdb-dataset-453510.IMDb_dataset.name` AS n ON p.nconst = n.nconst
JOIN `imdb-dataset-453510.IMDb_dataset.title_basics` AS t ON p.tconst = t.tconst
join `imdb-dataset-453510.IMDb_dataset.title_ratings` AS r on p.tconst = r.tconst
JOIN UNNEST(SPLIT(t.genres, ',')) AS genre
WHERE genre = 'Drama'
  AND p.category IN ('actor', 'actress')
  AND t.titleType = 'movie'
  AND r.numVotes >= 10000
GROUP BY n.primaryName
ORDER BY num_drama_titles DESC
LIMIT 10;
"""