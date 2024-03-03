# Project: TM-ETL Data Pipline

The ETL project for TM-Data Engineer exam which crafted as Serverless-ETL pipeline on AWS stacks.

---

## Part I: Algorithmic Thinking

the final code is on `1_algorithm/quadratic_problem.py`

Result:
![1-algorithm.png](image%2F1-algorithm.png)
---

## Part II: Pipeline Architecture and Diagram 🛤️

![architecture-diagram.png](image%2Farchitecture-diagram.png)

All components and infrastructure are created from Cloudformation template as IaC. All services designed to be
serverless data pipeline
to gain advantages over cost-optimization, scalability and rapid operation and less administration.

---

## Part II.I: Components 🛠️

- **Storage Layer**
    - s3: landing-zone and staging-zone, to store raw data, clean data and failed test data
    - DynamoDB: logging table, to monitor and save progress in any states in pipeline
- **Processing Layer**
    - Glue: is main processor for transforming, testing and loading
    - StepFunction: is main workflow orchestration of serving the pipeline
- **Consumption Layer**
    - Aurora Postgres: main destination database
    - Lambda and API Gateway: created to be Web Service to serve API calling to query interested data for a given user.
- **External Layer**
    - Lambda: the pipeline executor, responsibility to submit incoming/landing file to be ingested periodically.
      (Note: this demonstrated data pipeline is firstly designed to ingest daily)
    - Lambda Layer: to contain library dependencies for app-service.
    - SNS: alert and notification center, alert in both cases including FAILED and SUCCESS of ingestion in any states in
      running pipeline.

> In this project, **SNS** and **Aurora Postgres** are not created and included in Cloudformation.
---

### Part II.II: Workflow and States Transitions ⏳

![stepfunctions_graph_services.png](image%2Fstepfunctions_graph_services.png)

Inside workflow composed of states which provide a specific task to work with data. Main states can be divided into
three states as follows:

1. Transform - read raw data from incoming/landing data file in raw bucket which trigger by **s3-event trigger to a
   Lambda** which act as main controller of data pipeline. Transformed data will be wrote and store in staging bucket.
2. Test - after transformation succeeded, testing state will run through those data. Testing will check for correctness
   and completeness of data to be load to destination. Anyway, Test state can be passed by setting `HARD_TESTING=False`
   which designed to only log failed data, and will not suspend running of pipeline
3. Load - clean and ready of data in staging from transformation state is going to read and final step manipulate to
   match schema of destination and then load to it.

All processing unit, using **Glue** as main service to manipulate and process data.

* `SUCCESS` status will be sent as message via **SNS** to the team by email for notification
* `FAIL` in any states, failed message will be sent the team by email with the halt reason in the given state.
* all `status` in `state` will also save to **DynamoDB** which define to be main logging table of monitoring the
  progress of running workflow

---

### Part II.III: API and Webservice 🪟

Base URL from API Gateway:

```
https://yef61g0li2.execute-api.ap-southeast-1.amazonaws.com
```

With Query Parameter eg. user=foo

```
https://yef61g0li2.execute-api.ap-southeast-1.amazonaws.com/Prod/get?user=${user} 
```

Item in logging table (dynamodb)

```
{
  "ingestedID": {
    "S": "20240301-A001"
  },
  "ingestedTable": {
    "S": "dailycheckin"
  },
  "state": {
    "S": "load"
  },
  "status": {
    "S": "success"
  }
}
```

Alert from SNS
![tm-pipeline-noti.png](image%2Ftm-pipeline-noti.png)

Raw data from loading in Postgres (destination)
![data-in-postgres.png](image%2Fdata-in-postgres.png)

---