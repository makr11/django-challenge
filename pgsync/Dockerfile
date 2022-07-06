FROM python:3.10.5-alpine3.15
ARG WORKDIR=/code
RUN mkdir $WORKDIR
ADD pgsync/ $WORKDIR
ADD .env/ $WORKDIR
WORKDIR $WORKDIR
RUN pip install pgsync