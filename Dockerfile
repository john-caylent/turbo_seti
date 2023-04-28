FROM jupyter/pyspark-notebook

ARG DEBIAN_FRONTEND=noninteractive
USER root
RUN apt-get update -y
RUN apt-get upgrade -y

COPY . /turboseti
WORKDIR /turboseti
RUN chmod a+rwx /turboseti
#RUN cat dependencies.txt | xargs -n 1 apt install --no-install-recommends -y
RUN apt-get install -y python3-pip
RUN apt-get install -y python3-dev
RUN apt-get install -y python3-setuptools
RUN apt-get install -y libhdf5-dev
RUN apt-get install -y gcc
RUN apt-get install -y gfortran
RUN apt-get install -y wget
RUN apt-get install -y curl
RUN apt-get install -y git

RUN python3 -m pip install pip
RUN python3 -m pip install git+https://github.com/john-caylent/blimpy
#RUN python3 -m pip install git+https://github.com/john-caylent/turbo_seti@spark
RUN python3 -m pip install -r requirements.txt
#RUN python3 -m pip install -r requirements_test.txt
RUN python3 setup.py install
#RUN cd test && python3 download_test_data.py && cd ..
# RUN cd test && bash run_tests.sh && cd ..

WORKDIR /home