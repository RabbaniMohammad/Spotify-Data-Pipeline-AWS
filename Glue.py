import sys
from pyspark.context import SparkContext
from pyspark.sql import SparkSession
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions


args = getResolvedOptions(sys.argv, ['JOB_NAME'])


sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)


staging_bucket = "s3://medalian-architecture/staging/"
albums_path = f"{staging_bucket}albums.csv"
artists_path = f"{staging_bucket}artists.csv"
tracks_path = f"{staging_bucket}tracks.csv"


albums_df = spark.read.option("header", "true").csv(albums_path)
artists_df = spark.read.option("header", "true").csv(artists_path)
tracks_df = spark.read.option("header", "true").csv(tracks_path)


albums_artists_df = albums_df.join(
    artists_df, albums_df.artist_id == artists_df.id, "inner"
)


final_df = albums_artists_df.join(
    tracks_df, albums_artists_df.track_id == tracks_df.track_id, "inner"
)


columns_to_drop = ["artist_id", "id"]  # Adjust these based on column names
final_df_cleaned = final_df.drop(*columns_to_drop)


target_bucket = "s3://datawarehouse/"
output_path = f"{target_bucket}processed_data/"
final_df_cleaned.write.mode("overwrite").parquet(output_path, compression="snappy")


job.commit()
