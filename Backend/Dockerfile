FROM python:3.7.8-slim

COPY requirements/common.txt requirements/common.txt
RUN pip install -U pip && pip install -r requirements/common.txt

COPY ./api /app/api
COPY ./bin /app/bin
COPY wsgi.py /app/wsgi.py
COPY ./config /app/config
WORKDIR /app


# RUN useradd demo
# USER demo

EXPOSE 8080

# CMD ["--port 27017", "--smallfiles"]

ENTRYPOINT ["bash", "/app/bin/run.sh"]
# ENTRYPOINT ["./bin/run.sh"]
# ENTRYPOINT ["gunicorn"]
# CMD ["-w", "4", "-t", "100", "-b", "0.0.0.0:8080", "wsgi:app"]