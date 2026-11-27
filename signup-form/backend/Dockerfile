# Khung dùng cho bài ④ của form đăng ký người dùng. Hãy điền các chỗ TODO.
# Chạy Django (API và màn hình của bài ①).
FROM python:3.14.9-slim
COPY --from=ghcr.io/astral-sh/uv:0.13.10 /uv /uvx /bin/
ENV UV_LINK_MODE=copy
WORKDIR /app
# TODO: copy pyproject.toml, uv.lock, .python-version rồi cài thư viện bằng uv sync --locked
COPY . .
EXPOSE 8000
CMD ["sh", "-c", "uv run python manage.py migrate && uv run python manage.py loaddata prefs && uv run python manage.py runserver 0.0.0.0:8000"]
