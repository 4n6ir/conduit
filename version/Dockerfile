FROM public.ecr.aws/lambda/python:latest
RUN yum -y update && yum clean all
COPY version.py requirements.txt ./
RUN pip --no-cache-dir install -r requirements.txt --upgrade
CMD ["version.handler"]