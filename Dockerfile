FROM python:3.10-slim
WORKDIR /app
COPY run.sh /usr/local/bin/server
COPY src/clock_server/ /app/clock_server/
RUN chmod +x /usr/local/bin/server
CMD ["/usr/local/bin/server", "subscribers.json"]