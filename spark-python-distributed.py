from pyspark.sql import SparkSession
import os

if __name__ == "__main__":

    spark = SparkSession\
        .builder\
        .appName("StartupAnalysis")\
        .getOrCreate()

    # Read a large dataset from a file or any other data source
    data = spark.read.csv("s3://sandbox-terraform-aws-caylenttwo-emr/dataset/acquisitions.csv", header=True, inferSchema=True)

    # Perform transformations and actions on the data
    processed_data = data.filter(data["price_amount"] > 500000000) \
                        .groupBy("term_code") \
                        .agg({"price_amount": "avg"}) \
                        .orderBy("term_code")

    # Show the processed data
    processed_data.show()

    # Write the processed data to an output file or any other data sink
    processed_data.write.csv("s3://sandbox-terraform-aws-caylenttwo-emr/dataset/output.csv", header=True)

    # Stop the SparkSession
    spark.stop()