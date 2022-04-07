FROM public.ecr.aws/lambda/python:latest
RUN yum update -y && \
    yum clean all
RUN pip --no-cache-dir install feedparser PyGithub
COPY version.py ./
CMD ["version.handler"]
