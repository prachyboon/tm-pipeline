from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

import sys
import pytz
from datetime import datetime

from pyspark.sql.types import StructField, StringType, TimestampType, DecimalType, StructType
from pyspark.sql.functions import col

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
    StructField("hours", DecimalType(5, 2), True),
    StructField("project", StringType(), True),
])

IS_HARD_TESTING = False
HAS_FAILED_TESTS = False
TABLE = 'dailycheckins'

PATH = "s3://tm-staging-zone/table={}/year={}/month={}/day={}/".format(TABLE, year, month, day)
df = spark.read.schema(schema).csv(PATH, header=True)


def find_missing(tmp_df):
    missing_values = {}
    for index, tmp_column in enumerate(tmp_df.columns):
        missing_count = tmp_df.filter(
            col(tmp_column).eqNullSafe(None) | col(tmp_column).isNull() | col(tmp_column).isin([None])).count()
        missing_values.update({tmp_column: missing_count})
    return missing_values


missing_dict = find_missing(df)
missing_data = {}

for key, value in missing_dict.items():
    if value != 0:
        HAS_FAILED_TESTS = True
        values = df.filter(col(str(key)).eqNullSafe(None) | col(str(key)).isNull() | col(str(key)).isin([None]))
        missing_data[str(key)] = values

for key in missing_data.keys():
    missing_data[key].write \
        .option("header", "true") \
        .mode('overwrite') \
        .csv(
        "s3://tm-staging-zone/state=failed_tests/table={}/year={}/month={}/day={}/".format(TABLE, year, month, day))

if IS_HARD_TESTING and HAS_FAILED_TESTS:
    raise Exception("The dataset contains instances of failed tests, ingestion would be suspended.")

job.commit()
