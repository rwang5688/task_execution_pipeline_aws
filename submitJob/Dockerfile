FROM ubuntu:18.04

# set up OS, compilers, dependencies
RUN apt update -y
RUN apt install -y python3.8 python3-pip python3.8-dev
RUN pip3 install --upgrade pip
RUN pip3 install --no-cache-dir boto3

# download and install AWS CLI V2
RUN apt install -y curl unzip
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
RUN unzip awscliv2.zip
RUN ./aws/install

# create working directory
ADD . /submitJob
WORKDIR /submitJob

# import AWS credentials
RUN aws configure import --csv "file://aws-admin_accessKeys.csv"
RUN cat ~/.aws/credentials

# set entry point
ENTRYPOINT ["/bin/sh", "submitJob.sh"]

