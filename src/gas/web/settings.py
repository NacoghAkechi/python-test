"""Cấu hình tối thiểu cho đào tạo. Không dùng nguyên như vậy cho môi trường thật."""

SECRET_KEY = "insecure-key-for-training-only"
ALLOWED_HOSTS = ["localhost", "127.0.0.1", "testserver"]
INSTALLED_APPS = ["gas.web"]
ROOT_URLCONF = "gas.web.urls"
DATABASES = {
    "default": {"ENGINE": "django.db.backends.sqlite3", "NAME": "gas.sqlite3"},
}
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
USE_TZ = True
STATIC_URL = "static/"
MAILERS = {
    "default": {"BACKEND": "django.core.mail.backends.console.EmailBackend"},
}
