from pyspark.sql import SparkSession
from pyspark.sql.functions import month, col
from datetime import datetime
import sys

if __name__ == "__main__":

    spark = SparkSession\
        .builder\
        .appName("StockAnalysis")\
        .getOrCreate()

    dataset_mode = sys.argv[1]

    if dataset_mode == "complete":
        s3_url = "s3://sandbox-terraform-aws-caylenttwo-emr/dataset/stocks"
    else:
        s3_url = "s3://sandbox-terraform-aws-caylenttwo-emr/dataset/stocks-minimal"


    # Set a date to use dinamic naming on the output
    now = datetime.now()
    datetime_string = now.strftime("%Y%m%d%H%M%S")

    # Read a large dataset from a file or any other data source
    data = spark.read.csv(s3_url, header=True, inferSchema=True)

    # Show schema
    data.printSchema()

    # Perform transformations and actions on the data
    processed_data = data.filter((col("open") >= 1000) & (col("close") < 1000)) \
        .groupBy(month(col("date")).alias("month")).count()

    # Show the processed data
    processed_data.show()

    # Write the processed data to an output file or any other data sink
    processed_data.write.csv(
        "s3://sandbox-terraform-aws-caylenttwo-emr/dataset/{}-output.csv".format(datetime_string), header=True)

    # Stop the SparkSession
    spark.stop()
