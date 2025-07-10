--DDL for creating a table
--same script for uploading all the tables

CREATE EXTERNAL TABLE IF NOT EXISTS samples3db.fact_table (
  payment_key STRING,
  coustomer_key STRING,
  time_key STRING,
  item_key STRING,
  store_key STRING,
  quantity INT,
  unit STRING,
  unit_price DOUBLE,
  total_price DOUBLE
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES (
  "separatorChar" = ",",
  "quoteChar" = '"',
  "escapeChar" = "\\"
)
STORED AS TEXTFILE
LOCATION 's3://assurebuckets32pkkuppili/input/fact_table/'
TBLPROPERTIES ('has_encrypted_data'='false', 'skip.header.line.count'='1',
'serialization.null.format' = ''
);
