FROM python:3.10.5-alpine3.15
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY . /app
RUN apk --no-cache add curl
RUN pip install -r requirements.txt