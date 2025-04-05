# 4. Режиссёры и съёмочные группы (title.crew_clean.csv)

# 1. Режиссёры с наибольшим количеством фильмов
query = """
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
LIMIT 50

"""

# 2. топ режисеров с самыми высокими средними рейтингами.

query1 = """
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
HAVING COUNT(*) >= 5
ORDER BY avg_rating DESC
LIMIT 50


"""

# 3. Есть ли связь между известными режиссёрами и высокими оценками?

query2 = """
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