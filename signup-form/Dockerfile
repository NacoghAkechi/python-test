# ユーザー登録フォームの課題④で使う雛形。TODO を埋める。

# 1. React をビルドする（Node.js 22）
FROM node:22-slim AS frontend
WORKDIR /app/frontend
RUN corepack enable pnpm
# TODO: frontend/ の package.json・pnpm-lock.yaml・pnpm-workspace.yaml をコピーして、
#       pnpm install --frozen-lockfile で依存を入れる
# TODO: frontend/ の残りをコピーして、pnpm run build でビルドする

# 2. Django を動かす（Python 3.14.9）
FROM python:3.14.9-slim
COPY --from=ghcr.io/astral-sh/uv:0.13.10 /uv /uvx /bin/
ENV UV_LINK_MODE=copy
WORKDIR /app/backend
# TODO: backend/ の pyproject.toml・uv.lock・.python-version をコピーして、
#       uv sync --locked で依存を入れる
COPY backend/ ./
# TODO: 1 つめのステージ（frontend）の /app/frontend/dist を、/app/frontend/dist にコピーする
EXPOSE 8000
CMD ["sh", "-c", "uv run python manage.py migrate && uv run python manage.py loaddata prefs && uv run python manage.py runserver 0.0.0.0:8000"]
