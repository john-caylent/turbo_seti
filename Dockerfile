ARG IMAGE=755674844232.dkr.ecr.us-east-1.amazonaws.com/notebook-python/emr-6.10.0:latest
FROM ${IMAGE}

USER root

RUN yum -y update && yum install -y sudo

COPY --chown=hadoop:hadoop . /turboseti
WORKDIR /turboseti

#RUN cat dependencies.txt | xargs -n 1 yum install -y
#RUN xargs -n 1 yum install -y < dependencies.txt
RUN amazon-linux-extras install epel -y
RUN yum install -y hdf5-devel
RUN yum install -y python3-pip
RUN yum install -y yum install python3-devel.x86_64
RUN yum install -y python3-setuptools
#RUN yum install -y libhdf5-dev
RUN yum install -y gcc
RUN yum install -y gcc-gfortran
RUN yum install -y wget
RUN yum install -y curl
RUN yum install -y git

RUN python3 -m pip install -U pip
RUN python3 -m pip install git+https://github.com/UCBerkeleySETI/blimpy
RUN python3 -m pip install -r requirements.txt
RUN python3 -m pip install -r requirements_test.txt
RUN python3 setup.py install
#RUN cd test && python3 download_test_data.py && cd ..
# RUN cd test && bash run_tests.sh && cd ..

RUN find test -name "*.h5" -type f -delete
RUN find test -name "*.log" -type f -delete
RUN find test -name "*.dat" -type f -delete
RUN find test -name "*.fil" -type f -delete
RUN find test -name "*.png" -type f -delete
RUN find . -path '*/__pycache__*' -delete

USER hadoop:hadoop

WORKDIR /home/hadoop
