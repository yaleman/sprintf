FROM python:3.10-slim
# FROM python:3.10-alpine

########################################
# add a user so we're not running as root
########################################
# ubuntu mode
RUN useradd sprintf

# alpine mode
# RUN apk add --no-cache curl
# RUN addgroup -S appgroup && adduser -S sprintf -G appgroup

RUN apt-get update
RUN apt-get install -y curl
RUN apt-get clean

RUN mkdir -p /home/sprintf/
RUN chown sprintf /home/sprintf -R

RUN mkdir -p build/sprintf

WORKDIR /build

COPY sprintf sprintf
COPY pyproject.toml .

RUN chown sprintf /build -R
WORKDIR /build/
USER sprintf

RUN python -m pip install --upgrade --no-warn-script-location pip
RUN python -m pip install --no-warn-script-location /build

# clean up after ourselves
USER root
WORKDIR /
RUN rm -rf /build/

USER sprintf
# to allow xff headers from docker IPs
ENV FORWARDED_ALLOW_IPS="*"

CMD python -m sprintf --host 0.0.0.0 --port 8000 --proxy-headers
