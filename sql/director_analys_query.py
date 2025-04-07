# Directors analysis

# Directors with the most films produced
query_directors_films = """
SELECT 
      n.primaryName,
      COUNT(*) AS film_count
FROM `imdb-dataset-453510.IMDb_dataset.title_crew` as c
JOIN UNNEST(SPLIT(string_field_1, ',')) AS directors
JOIN `imdb-dataset-453510.IMDb_dataset.name` AS n 
  on directors = n.nconst

where string_field_1 != 'Unknown'
and string_field_2 != 'Unknown'
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
FROM `imdb-dataset-453510.IMDb_dataset.title_crew` as c
JOIN UNNEST(SPLIT(string_field_1, ',')) AS directors
JOIN `imdb-dataset-453510.IMDb_dataset.name` AS n 
  on directors = n.nconst
join `imdb-dataset-453510.IMDb_dataset.title_ratings` AS r
  on c.string_field_0 = r.tconst

where directors != 'Unknown'
and string_field_2 != 'Unknown'
and r.numVotes >=10000

group by directors, n.primaryName
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
  FROM `imdb-dataset-453510.IMDb_dataset.title_crew` AS c
  JOIN UNNEST(SPLIT(string_field_1, ',')) AS directors
  JOIN `imdb-dataset-453510.IMDb_dataset.title_ratings` AS r
    ON c.string_field_0 = r.tconst
  WHERE c.string_field_1 != 'Unknown'
    AND r.numVotes >= 1000
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