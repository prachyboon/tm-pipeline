from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

import pytz
from datetime import datetime

from pyspark.sql.types import *
from pyspark.sql.functions import *

local_timezone = pytz.timezone('Asia/Bangkok')
execute_time = datetime.now(local_timezone)
year = execute_time.year
month = execute_time.month
day = execute_time.day

print(execute_time)
print("year:{} | month={} | day={}".format(year, month, day))

args = getResolvedOptions(sys.argv, ['JOB_NAME'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

schema = StructType([
    StructField("user", StringType(), True),
    StructField("timestamp", TimestampType(), True),
    StructField("hours", FloatType(), True),
    StructField("project", StringType(), True),
])

TABLE = 'dailycheckins'

path = "s3://tm-staging-zone/table={}/year={}/month={}/day={}/".format(TABLE, year, month, day)
df = spark.read.schema(schema).csv(path, header=True)
df = df.withColumnRenamed('user', 'username').drop('user')

aurora_postgres_url = "jdbc:postgresql://database-1.cluster-cqnnuqtyqggk.ap-southeast-1.rds.amazonaws.com:5432/tm"
aurora_postgres_properties = {
    "user": "prachya",
    "password": "prachya2024",
    "driver": "org.postgresql.Driver"
}

df.write \
    .format("jdbc") \
    .option("url", aurora_postgres_url) \
    .option("dbtable", "daily_checkins") \
    .option("user", aurora_postgres_properties["user"]) \
    .option("password", aurora_postgres_properties["password"]) \
    .option("driver", aurora_postgres_properties["driver"]) \
    .mode("append") \
    .save()

job.commit()
