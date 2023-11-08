CREATE TABLE IF NOT EXISTS mapreduce_output (
    label_id STRING,
    artist_id STRING,
    artist_name STRING,
    decade INT,
    genre STRING,
    releases_count INT
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY '\t'
STORED AS TEXTFILE;

LOAD DATA INPATH 'gs://fsbd23/project1/output.tsv' INTO TABLE mapreduce_output;

CREATE TABLE IF NOT EXISTS datasource4 (
    label_id STRING,
    label_name STRING
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY '\u0001'
STORED AS TEXTFILE;

-- Assuming you have datasource4 data in GCS, load it into the Hive table
LOAD DATA INPATH 'gs://fsbd23/datasource4/part-00000' INTO TABLE datasource4;


CREATE VIEW top_labels AS
SELECT d.label_name, m.decade, COUNT(DISTINCT m.artist_id) AS artists_count, SUM(m.releases_count) AS releases_count, COLLECT_SET(m.genre) AS genres
FROM mapreduce_output m
JOIN datasource4 d ON m.label_id = d.label_id
GROUP BY d.label_name, m.decade
DISTRIBUTE BY m.decade
SORT BY m.decade ASC, releases_count DESC;

-- Now, select the top 3 labels for each decade
CREATE TABLE top_three_labels AS
SELECT label_name, decade, artists_count, releases_count, genres
FROM (
    SELECT label_name, decade, artists_count, releases_count, genres,
           ROW_NUMBER() OVER (PARTITION BY decade ORDER BY releases_count DESC) as rank
    FROM top_labels
) t
WHERE rank <= 3;

INSERT OVERWRITE DIRECTORY 'output'
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.JsonSerDe'
SELECT
  CONCAT(
    '{',
    '"label_name": "', label_name, '",',
    '"decade": ', CAST(decade AS STRING), ',',
    '"artists_count": ', CAST(artists_count AS STRING), ',',
    '"releases_count": ', CAST(releases_count AS STRING), ',',
    '"genres": ["', CONCAT_WS('","', genres), '"]',
    '}'
  ) AS json_output
FROM top_three_labels;