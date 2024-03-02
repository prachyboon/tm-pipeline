# Project: TM-ETL Data Pipline

# Description:
The ETL project for TM-Data Engineer exam which crafted as Serverless-ETL pipeline on AWS stacks.  

# Overview 
- diagram

# Components 
- **Storage Layer**
  - s3: landing-zone and staging-zone, to store raw data, clean data and failed test data
  - DynamoDB: logging table, to monitor and save progress in any states in pipeline 
- **Processing Layer**
  - Glue: is main processor for transforming, testing and loading
  - StepFunction: is main workflow orchestration of serving the pipeline
- **Consumption Layer**
  - Aurora Postgres: main destination database
- **External Layer**
  - Lambda: the pipeline executor, responsibility to submit incoming/landing file to be ingested periodically. 
  (Note: this demonstrated data pipeline is firstly designed to ingest daily)
  - SNS: alert and notification center, alert in both cases including FAILED and SUCCESS of ingestion in any states in running pipeline. 