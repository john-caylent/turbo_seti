import sys
import os
import glob
import time
import requests
import boto3
from blimpy import Waterfall
from turbo_seti.find_doppler.find_doppler import FindDoppler
from pyspark.sql import SparkSession

if __name__ == "__main__":

    spark = SparkSession\
        .builder\
        .appName("SETI")\
        .getOrCreate()

    h5_url = sys.argv[1]
    s3_bucket = sys.argv[2]
    s3_prefix = sys.argv[3]

    response = requests.get(h5_url)

    if response.status_code == 200:
        with open("/data/dataset.h5", 'wb') as f:
            f.write(response.content)
        print("File dataset.h5 downloaded successfully!")
    else:
        print("Failed to download file")
        sys.exit(1)

    H5DIR = "/data/"
    H5PATH = H5DIR + "dataset.h5"

    # print("\nUsing HDF5 file: {}\nHeader and data shape:".format(H5PATH))
    # # -- Get a report of header and data shape
    # wf = Waterfall(H5PATH)
    # wf.info()
    # # -- Instantiate FindDoppler.
    # print("\nInstantiating the FindDoppler object.")
    # fdop = FindDoppler(datafile=H5PATH, max_drift=4, snr=25,out_dir="/data")
    # # -- Search for hits and report elapsed time.
    # print("\nBegin doppler search.  Please wait ...")
    # t1 = time.time()
    # fdop.search()
    # elapsed_time = time.time() - t1
    # print("\nFindDoppler.search() elapsed time = {} seconds".format(elapsed_time))


    # glob will create a list of specific files in a directory. In this case, any file ending in .h5.
    h5list = sorted(glob.glob("/data/" + '*.h5'))

    # Iterate over the 6 HDF5 files
    print("tutorial_1: Please wait for the \"End\" message,\n")
    for file in h5list:
        # Execute turboSETI in the terminal
        console = 'turboSETI ' + file + ' -M 4 -s 10 -o ' + "/data/"
        os.system(console)

    print("\ntutorial_1: All HDF5 files have been successfully processed.")
    print("tutorial_1: End.")

    print("tutorial_1: Please wait for the \"End\" message,\n")
    console = "plotSETI -f 3 -o " + "/data/" + " " + "/data/"
    os.system(console)
    print("\ntutorial_1: All PNG files have been generated.")
    print("tutorial_1: End.")

    directory_path = "/data"
    # Create an S3 client
    s3 = boto3.client('s3')
    # Set the directory path where the PNG images are located

    # Loop through each file in the directory and upload any PNG images to the S3 bucket
    for file_name in os.listdir(directory_path):
        if file_name.endswith('.png'):
            file_path = os.path.join(directory_path, file_name)
            with open(file_path, 'rb') as f:
                s3.upload_fileobj(f, s3_bucket, f'{s3_prefix}/{file_name}')
                print(f'Successfully uploaded {file_name} to S3 bucket {s3_bucket} in directory {s3_prefix}')
                url_expiration = 3600 # URL expiration time in seconds (set to 1 hour)
                url = s3.generate_presigned_url('get_object', Params={'Bucket': s3_bucket, 'Key': f'{s3_prefix}/{file_name}'}, ExpiresIn=url_expiration)
                print(f'Pre-signed URL for {file_name}: {url}')

    spark.stop()
