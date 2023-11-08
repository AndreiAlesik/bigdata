-- Create table for mapreduce_output
CREATE TABLE IF NOT EXISTS mapreduce_output (
    artist_id STRING,
    decade INT,
    genre STRING,
    releases_count INT
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY '\t'
STORED AS TEXTFILE;

-- Load data into mapreduce_output table
LOAD DATA INPATH '${input_dir3}' INTO TABLE mapreduce_output;

-- Create table for datasource4
CREATE TABLE IF NOT EXISTS datasource4 (
    label_id STRING,
    label_name STRING
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY '\001'
STORED AS TEXTFILE;

-- Load data into datasource4 table
LOAD DATA INPATH '${input_dir4}' INTO TABLE datasource4;

-- Create a view for top labels
CREATE VIEW top_labels AS
SELECT d.label_name, m.decade, COUNT(DISTINCT m.artist_id) AS artists_count, SUM(m.releases_count) AS releases_count
FROM mapreduce_output m
JOIN datasource4 d ON m.artist_id = d.label_id
GROUP BY d.label_name, m.decade
DISTRIBUTE BY m.decade
SORT BY m.decade ASC, releases_count DESC;

-- Select the top 3 labels for each decade
CREATE TABLE IF NOT EXISTS top_three_labels AS
SELECT label_name, decade, artists_count, releases_count
FROM (
    SELECT label_name, decade, artists_count, releases_count,
           ROW_NUMBER() OVER (PARTITION BY decade ORDER BY releases_count DESC) as rank
    FROM top_labels
) t
WHERE rank <= 3;

-- Create external table to store the final results in JSON format
CREATE EXTERNAL TABLE IF NOT EXISTS json_res (
    label_name STRING,
    decade INT,
    artists_count INT,
    releases_count INT
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.JsonSerDe'
STORED AS TEXTFILE
LOCATION '${output_dir6}';

-- Insert data into json_res with the results in JSON format
INSERT OVERWRITE TABLE json_res
SELECT CONCAT(
    '{',
    '"label_name": "', label_name, '",',
    '"decade": ', CAST(decade AS STRING), ',',
    '"artists_count": ', CAST(artists_count AS STRING), ',',
    '"releases_count": ', CAST(releases_count AS STRING),
    '}'
) AS json_output
FROM top_three_labels;
