FROM python:3.10.6-alpine

WORKDIR /app

COPY db db
COPY python python

RUN addgroup -S mercari && adduser -S trainee -G mercari
# RUN chown -R trainee:mercari /path/to/db

RUN apk add --update python3
RUN pip3 install --upgrade pip

RUN pip3 install fastapi
RUN pip3 install uvicorn

USER trainee

WORKDIR /app/python

CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "9000"]



