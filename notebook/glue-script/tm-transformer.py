from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

import sys
import pytz
from datetime import datetime

from pyspark.sql.types import StringType, TimestampType, DecimalType
from pyspark.sql.functions import (col, monotonically_increasing_id, regexp_replace,
                                   to_utc_timestamp, from_unixtime, unix_timestamp)

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

spark.conf.set("spark.sql.legacy.timeParserPolicy", "LEGACY")
spark.conf.set("spark.sql.parquet.datetimeRebaseModeInWrite", "CORRECTED")

TABLE = 'dailycheckins'


def make_datetime_ru(tmp_df):
    month_mapping = {
        'января': 'January',
        'февраля': 'February',
        'марта': 'March',
        'апреля': 'April',
        'мая': 'May',
        'июня': 'June',
        'июля': 'July',
        'августа': 'August',
        'сентября': 'September',
        'октября': 'October',
        'ноября': 'November',
        'декабря': 'December'
    }
    for russian_month, english_month in month_mapping.items():
        tmp_df = tmp_df.withColumn('timestamp', regexp_replace(col('timestamp'), russian_month, english_month))
    return tmp_df


PATH = "s3://tm-raw-zone/table={}/year={}/month={}/day={}/".format(TABLE, year, month, day)
df = spark.read.csv(PATH, header=True)

df = df.withColumn("id", monotonically_increasing_id())

# casting to be right
df2 = df.withColumn('user', col('user').cast(StringType()))
df2 = df2.withColumn('hours', col('hours').cast(DecimalType(5, 2)))
df2 = df2.withColumn('project', col('project').cast(StringType()))
df2 = df2.withColumn('timestamp', col('timestamp').cast(TimestampType()))

# transform 'timestamp' column
nullIds = df2.filter(col('timestamp').eqNullSafe(None) | col('timestamp').isNull()).select('id').rdd.flatMap(
    lambda x: x).collect()
clean_df = df2.filter(~col("id").isin(nullIds))
df3 = df.filter(col("id").isin(nullIds))

# transform 'alien format#1 - AM/PM'
format_1 = 'MM/dd/yyyy hh:mm a'
df3 = df3.withColumn('timestamp', to_utc_timestamp(from_unixtime(unix_timestamp(col('timestamp'), format_1)), 'UTC'))

ruIDs = df3.filter(col('timestamp').eqNullSafe(None) | col('timestamp').isNull()).select('id').rdd.flatMap(
    lambda x: x).collect()
clean_df2 = df3.filter(~col("id").isin(ruIDs))
df4 = df.filter(col("id").isin(ruIDs))

# transform 'alien format#2 - RU'
df4 = make_datetime_ru(df4)
format_2 = "dd MMMM y HH:mm"
df4 = df4.withColumn('timestamp', to_utc_timestamp(from_unixtime(unix_timestamp(col('timestamp'), format_2)), 'UTC'))

# final df
clean_df3 = df4.select('*')
final_df = clean_df.unionByName(clean_df2).unionByName(clean_df3)

final_df = final_df.withColumn('timestamp', col('timestamp').cast(StringType()))

final_df.write \
    .format("csv") \
    .option("header", "true") \
    .mode("overwrite") \
    .save("s3://tm-staging-zone/table={}/year={}/month={}/day={}/".format(TABLE, year, month, day))

job.commit()
