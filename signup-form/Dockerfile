# Khung dùng cho bài ④ của form đăng ký người dùng. Hãy điền các chỗ TODO.

# 1. Build React (Node.js 22)
FROM node:22-slim AS frontend
WORKDIR /app/frontend
RUN corepack enable pnpm
# TODO: copy package.json, pnpm-lock.yaml, pnpm-workspace.yaml trong frontend/,
#       rồi cài thư viện bằng pnpm install --frozen-lockfile
# TODO: copy phần còn lại của frontend/, rồi build bằng pnpm run build

# 2. Chạy Django (Python 3.14.9)
FROM python:3.14.9-slim
COPY --from=ghcr.io/astral-sh/uv:0.13.10 /uv /uvx /bin/
ENV UV_LINK_MODE=copy
WORKDIR /app/backend
# TODO: copy pyproject.toml, uv.lock, .python-version trong backend/,
#       rồi cài thư viện bằng uv sync --locked
COPY backend/ ./
# TODO: copy /app/frontend/dist của stage thứ nhất (frontend) vào /app/frontend/dist
EXPOSE 8000
CMD ["sh", "-c", "uv run python manage.py migrate && uv run python manage.py loaddata prefs && uv run python manage.py runserver 0.0.0.0:8000"]
