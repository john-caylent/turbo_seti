FROM 755674844232.dkr.ecr.us-east-1.amazonaws.com/notebook-spark/emr-6.9.0:latest
USER root
### Add customization commands here ####
RUN yum install -y git
RUN pip3 install requests boto3
RUN pip3 install git+https://github.com/john-caylent/blimpy
RUN pip3 install git+https://github.com/john-caylent/turbo_seti

USER hadoop:hadoop
COPY seti_example.py /scripts/seti_example.py