# Directors analysis

# Directors with the most films produced
query_directors_films = """
SELECT 
      n.primaryName,
      COUNT(*) AS film_count
FROM `imdb-dataset-453510.IMDb_dataset.title_crew_cleaned` as c
JOIN UNNEST(SPLIT(c.directors, ',')) AS directors
JOIN `imdb-dataset-453510.IMDb_dataset.name_basics` AS n 
  ON directors = n.nconst
group by directors, n.primaryName
ORDER BY film_count DESC
LIMIT 10
"""

# top directors with the highest average ratings.
query_top_directors = """
SELECT 
      n.primaryName,
      COUNT(*) AS film_count,
      round(avg(r.averageRating),2) AS avg_rating
FROM `imdb-dataset-453510.IMDb_dataset.title_crew_cleaned` as c
JOIN UNNEST(SPLIT(c.directors, ',')) AS directors
JOIN `imdb-dataset-453510.IMDb_dataset.name_basics` AS n 
  ON directors = n.nconst
JOIN `imdb-dataset-453510.IMDb_dataset.title_with_ratings` AS r
  ON c.tconst = r.tconst
WHERE r.numVotes >=10000
GROUP BY directors, n.primaryName
HAVING COUNT(*) >= 10
ORDER BY avg_rating DESC
LIMIT 10
"""

# the connection between famous directors and high ratings
query_directors_vs_ratings = """
WITH director_stats AS (
  SELECT 
    directors AS director_id,
    COUNT(*) AS film_count,
    SUM(r.numVotes) AS total_votes,
    AVG(r.averageRating) AS avg_rating
  FROM `imdb-dataset-453510.IMDb_dataset.title_crew_cleaned` AS c
  JOIN UNNEST(SPLIT(c.directors, ',')) AS directors
  JOIN `imdb-dataset-453510.IMDb_dataset.title_with_ratings` AS r
    ON c.tconst = r.tconst
  WHERE r.numVotes >= 1000
  GROUP BY directors
),
labeled AS (
  SELECT *,
    CASE 
      WHEN film_count >= 10 AND total_votes >= 100000 THEN 'famous'
      ELSE 'regular'
    END AS status
  FROM director_stats
)

SELECT 
  status,
  COUNT(*) AS director_count,
  round(AVG(avg_rating),2) AS avg_director_rating
FROM labeled
GROUP BY status
"""