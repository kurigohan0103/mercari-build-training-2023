FROM alpine

RUN addgroup -S mercari && adduser -S trainee -G mercari
# RUN chown -R trainee:mercari /path/to/db

RUN apk add python3

USER trainee

CMD ["python", "-V"]
