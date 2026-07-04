FROM ghcr.io/astral-sh/uv:python3.11-bookworm-slim

WORKDIR /app

COPY pyproject.toml uv.lock ./
COPY src ./src
COPY README.md ./
RUN uv sync --frozen --no-dev --extra api

COPY api ./api

# ユーザー辞書のコンパイル先(実行時ユーザーが書ける場所に)
ENV SORAMIMI_YOMI_CACHE=/tmp/soramimi-yomi

EXPOSE 8080
CMD ["uv", "run", "--no-sync", "uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8080"]
