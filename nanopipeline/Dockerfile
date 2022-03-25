FROM public.ecr.aws/lambda/python:latest
RUN yum -y update && \
    curl -sL https://rpm.nodesource.com/setup_16.x | bash - && \
    yum list available nodejs && \
    yum install -y nodejs && \
    npm install -g aws-cdk && \
    yum clean all && \
    date +%s
COPY nanopipeline.py requirements.txt ./
RUN pip --no-cache-dir install -r requirements.txt --upgrade
CMD ["nanopipeline.handler"]