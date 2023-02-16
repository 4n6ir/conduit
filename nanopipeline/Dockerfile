# CDK v2.65.0
FROM public.ecr.aws/lambda/python:latest
RUN yum -y update
RUN curl -sL https://rpm.nodesource.com/setup_16.x | bash -
RUN yum list available nodejs
RUN yum install -y nodejs
RUN npm install -g aws-cdk@latest
RUN yum clean all
COPY nanopipeline.py requirements.txt ./
RUN pip --no-cache-dir install -r requirements.txt --upgrade
CMD ["nanopipeline.handler"]
