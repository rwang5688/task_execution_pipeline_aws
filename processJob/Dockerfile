FROM ubuntu:18.04

# set up OS, compilers, dependencies
RUN apt update -y && \
    apt install -y python3.8 python3-pip python3.8-dev
RUN pip3 install --upgrade pip
RUN pip3 install --no-cache-dir boto3
RUN apt install -y g++

# create working directory
ADD . /processJob
WORKDIR /processJob

# compile XVSA mock
RUN make

# download and install AWS CLI V2
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
RUN unzip awscliv2.zip
RUN ./aws/install

# configure AWS credentials
RUN aws configure import –csv file://aws-admin_accessKeys.csv

# set entry point
ENTRYPOINT ["/bin/sh", "processJob.sh"]

