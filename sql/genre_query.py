# Genre analysis

# 1.What genres are the most films/TV series made in?
query_movie_vs_series = """
WITH genre_counts AS (
  SELECT 
    genre,
    titleType,
    COUNT(*) AS count
  FROM `imdb-dataset-453510.IMDb_dataset.title_with_ratings`
  JOIN UNNEST(SPLIT(genres, ',')) AS genre
  WHERE titleType IN ('movie', 'tvSeries')
  GROUP BY genre, titleType
),

-- sum all by genre
genre_totals AS (
  SELECT 
    genre,
    SUM(count) AS total_count
  FROM genre_counts
  GROUP BY genre
  ORDER BY total_count DESC
  LIMIT 15
)


SELECT 
  gc.genre,
  gc.titleType,
  gc.count
FROM genre_counts gc
JOIN genre_totals gt ON gc.genre = gt.genre
ORDER BY gt.total_count DESC, gc.titleType

"""