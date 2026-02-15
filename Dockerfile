FROM registry.access.redhat.com/ubi9/python-312:latest

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

WORKDIR /opt/app-root/src

COPY pyproject.toml uv.lock .python-version ./
RUN uv sync --frozen --no-dev --no-install-project

COPY src/ src/
RUN uv sync --frozen --no-dev

EXPOSE 9185

ENTRYPOINT [".venv/bin/rhdh-plugin-heartbeat"]
