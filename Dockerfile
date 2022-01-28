FROM python:3.10

# add a user so we're not running as root
RUN useradd sprintf
RUN mkdir -p /home/sprintf/
RUN chown sprintf /home/sprintf -R

RUN mkdir -p build/sprintf

WORKDIR /build

COPY sprintf sprintf
COPY poetry.lock .
COPY pyproject.toml .

RUN python -m pip install poetry

RUN chown sprintf /build -R
WORKDIR /build/
USER sprintf

RUN poetry install

# Now we just want to our WORKDIR to be /build/app for simplicity
# We could skip this part and then type
# python -m uvicorn main.app:app ... below

CMD poetry run uvicorn sprintf:app --host 0.0.0.0 --port 8090
