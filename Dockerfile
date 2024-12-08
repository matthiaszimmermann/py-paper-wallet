ARG DEBIAN_VERSION=bookworm
ARG UV_VERSION=0.5.4
ARG VARIANT=3.12

FROM ghcr.io/astral-sh/uv:$UV_VERSION AS uv

FROM python:$VARIANT-slim-$DEBIAN_VERSION
LABEL maintainer="matthias zimmermann"

ENV PYTHONDONTWRITEBYTECODE=True
ENV PYTHONUNBUFFERED=True
ENV UV_LINK_MODE=copy

WORKDIR /app

COPY --from=uv /uv /uvx /bin/

COPY pyproject.toml uv.lock ./
COPY ./resources ./resources
COPY ./src ./src

RUN uv sync --frozen --no-install-project

CMD [ "bash" ]
