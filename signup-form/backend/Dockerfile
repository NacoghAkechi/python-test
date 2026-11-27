# ユーザー登録フォームの課題④で使う雛形。TODO を埋める。
# Django（API と課題①の画面）を動かす。
FROM python:3.14.9-slim
COPY --from=ghcr.io/astral-sh/uv:0.13.10 /uv /uvx /bin/
ENV UV_LINK_MODE=copy
WORKDIR /app
# TODO: pyproject.toml・uv.lock・.python-version をコピーして、uv sync --locked で依存を入れる
COPY . .
EXPOSE 8000
CMD ["sh", "-c", "uv run python manage.py migrate && uv run python manage.py loaddata prefs && uv run python manage.py runserver 0.0.0.0:8000"]
