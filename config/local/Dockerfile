FROM python:3.9

EXPOSE 8888

RUN mkdir -p /usr/src/app && \
    mkdir -p /usr/src/config

WORKDIR /usr/src/app

COPY src .
COPY config/local /usr/src/config

RUN pip install --no-cache-dir -r ../config/requirements.txt

ENTRYPOINT ["../config/start_app.sh"]