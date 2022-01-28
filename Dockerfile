FROM python:3.10-alpine

# add a user so we're not running as root
# RUN useradd sprintf
RUN addgroup -S appgroup && adduser -S sprintf -G appgroup

RUN mkdir -p /home/sprintf/
RUN chown sprintf /home/sprintf -R

RUN mkdir -p build/sprintf

WORKDIR /build

COPY sprintf sprintf
COPY poetry.lock .
COPY pyproject.toml .

# RUN python -m pip install poetry

RUN chown sprintf /build -R
WORKDIR /build/
USER sprintf

RUN python -m pip install --upgrade pip
RUN python -m pip install /build

# to allow xff headers from docker IPs
ENV FORWARDED_ALLOW_IPS="*"

CMD /home/sprintf/.local/bin/uvicorn sprintf:app --host 0.0.0.0 --port 8090 --proxy-headers
