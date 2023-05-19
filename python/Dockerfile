FROM alpine

RUN addgroup -S mercari && adduser -S trainee -G mercari
# RUN chown -R trainee:mercari /path/to/db

RUN apk add --update python3
RUN apk add --update py3-pip

USER trainee

CMD ["python", "-V"]
