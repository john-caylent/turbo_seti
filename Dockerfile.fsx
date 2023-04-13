FROM 755674844232.dkr.ecr.us-east-1.amazonaws.com/spark/emr-6.9.0:latest
USER root
### Add customization commands here ####
RUN yum install -y git
RUN pip3 install requests
RUN pip3 install git+https://github.com/john-caylent/blimpy
RUN pip3 install git+https://github.com/john-caylent/turbo_seti
RUN mkdir /data
RUN chmod 777 /data

USER hadoop:hadoop
COPY seti_example.py /scripts/seti_example.py