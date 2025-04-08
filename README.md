# IMDb Data Analysis
&nbsp; 
## Project Overview 

This project explores trends in the IMDb dataset to better understand what types of content are produced, how audiences rate them, and who the most active or successful contributors are. 
I focus on visualizing key metrics like genre popularity, production volume over time, average ratings, and contributor performance in a clear and approachable way.

&nbsp; 
## Key Objectives
The goal of this project is to extract meaningful insights from the IMDb dataset by answering several key questions:

  - What types of content (e.g. movies, series, episodes) are most common?

  - How has production volume changed over time?

  - Which genres are the most popular and which receive the highest ratings?

  - What is the typical runtime for different types of content?

  - Who are the most active and highest-rated actors and directors?

  - Is there a connection between how popular a title is (number of votes) and how well it's rated?
    
&nbsp;
 ## Data Sources
The analysis is based on IMDb data files manually downloaded from the official [IMDb datasets](https://datasets.imdbws.com/) page and then uploaded to Google BigQuery for querying. 
The following tables were created from the corresponding TSV files:


  - **IMDb_dataset.title_basics → title.basics.tsv**
    
Contains metadata about titles, including type (movie, short, TV episode), primary title, original title, start/end year, runtime, and genres.

  - **IMDb_dataset.title_ratings → title.ratings.tsv**
    
Includes the average IMDb rating and the number of votes each title has received

  - **IMDb_dataset.title_principals → title.principals.tsv**
    
Maps titles to their main cast and crew (actors, actresses, directors, etc.), including their role categories and order of appearance.

  - **IMDb_dataset.name → name.basics.tsv**
    
rovides information about individuals (e.g. actors, directors), including their birth/death years and known titles.

  - **IMDb_dataset.title_crew → title.crew.tsv**
    
 Contains directors and writers for each title, often stored as comma-separated IDs.

 &nbsp; 
## Tools & Technologies
  - **Google BigQuery** for SQL querying large datasets

  - **Python** for data analysis and visualization

  - **Libraries:** pandas, matplotlib, seaborn, numpy, scipy

&nbsp; 
## Key Insights from the Analysis

&nbsp; 
## Insights Deep-Dive

### Title Type Distribution
---
![imdb analysis](plots/general_count.png)
This chart shows how different types of content are distributed in the IMDb dataset. TV episodes make up the largest portion by far, followed by short films and movies. This is largely due to the high number of episodes per TV series, each counted as a separate record.

&nbsp;
### Production Over Time
---
![imdb analysis](plots/titles_by_decade.png)
This line chart displays the number of titles released per decade. While production remained relatively low and steady throughout the first half of the 20th century, there was a dramatic increase starting in the 1990s. The peak occurred in the 2010s, with over 4 million titles produced, driven largely by the explosion of TV content and digital platforms. The sharp drop in the 2020s reflects incomplete data for the decade.

&nbsp;
### Average Runtime by Title Type
---
![imdb analysis](plots/runtime_by_type.png)
This chart presents the average runtime for each title type in the dataset. As expected, video games and feature films have the longest durations, while TV episodes, shorts, and TV shorts are significantly shorter in length.

&nbsp;
### Top-Rated Genres
---
![imdb analysis](plots/top_genres_by_rating.png)
This chart displays the average IMDb rating across different genres. Genres such as History, Documentary, and Biography top the list with average ratings above 7.2, suggesting these types of content tend to resonate more strongly with audiences. This insight can help identify which genres consistently maintain high viewer satisfaction.




