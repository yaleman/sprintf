FROM python:3.13-slim

########################################
# add a user so we're not running as root
########################################
RUN useradd sprintf

RUN apt-get update
RUN apt-get install -y curl
RUN apt-get clean

RUN mkdir -p /home/sprintf/
RUN chown sprintf /home/sprintf -R

RUN mkdir -p build/sprintf

WORKDIR /build

COPY sprintf sprintf
COPY pyproject.toml .

RUN chown sprintf:sprintf /build -R
RUN chown sprintf:sprintf /home/sprintf -R
WORKDIR /build/


USER sprintf

RUN python -m pip install --user --upgrade pip /build


# clean up after ourselves
USER root
WORKDIR /
RUN rm -rf /build/

USER sprintf
# to allow xff headers from docker IPs
ENV FORWARDED_ALLOW_IPS="*"
# tell people where we're running the thing
EXPOSE 8000
ENV PATH="/home/sprintf/.local/bin"
CMD [ "sprintf", "--host", "0.0.0.0", "--port", "8000", "--proxy-headers"]
