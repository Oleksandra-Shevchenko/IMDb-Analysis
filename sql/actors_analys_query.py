# Actors analysis

# 1. Most active actors
query_active = """
SELECT 
  n.primaryName,
  COUNT(DISTINCT b.tconst) AS film_count
FROM `imdb-dataset-453510.IMDb_dataset.title_principals` AS p
JOIN `imdb-dataset-453510.IMDb_dataset.name_basics` AS n
  ON p.nconst = n.nconst
JOIN `imdb-dataset-453510.IMDb_dataset.title_with_ratings` AS b
  ON p.tconst = b.tconst
WHERE p.category IN ('actor', 'actress')
  AND b.titleType IN ('movie', 'tvMovie') 
  AND p.ordering = 1
GROUP BY n.primaryName
HAVING film_count >= 10
ORDER BY film_count DESC
LIMIT 20;
"""


# 2. Actors in dramas
query_drama_actors = """
SELECT 
  n.primaryName,
  COUNT(*) AS num_drama_titles
FROM `imdb-dataset-453510.IMDb_dataset.title_principals` AS p
JOIN `imdb-dataset-453510.IMDb_dataset.name_basics` AS n ON p.nconst = n.nconst
JOIN `imdb-dataset-453510.IMDb_dataset.title_with_ratings` AS t ON p.tconst = t.tconst
JOIN UNNEST(SPLIT(t.genres, ',')) AS genre
WHERE genre = 'Drama'
  AND p.category IN ('actor', 'actress')
  AND t.titleType = 'movie'
  AND t.numVotes >= 10000
GROUP BY n.primaryName
ORDER BY num_drama_titles DESC
LIMIT 10;
"""