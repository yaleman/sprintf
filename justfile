docker:
    docker buildx build \
        --load \
        -t ghcr.io/yaleman/sprintf:latest .

run_docker: docker
    docker run --rm -it \
        --name sprintf \
        -p 127.0.0.1:8000:8000 \
        ghcr.io/yaleman/sprintf:latest

check:
    uv run ruff check tests sprintf
    uv run pytest
    uv run mypy --strict sprintf tests