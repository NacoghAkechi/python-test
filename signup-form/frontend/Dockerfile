# ユーザー登録フォームの課題④で使う雛形。TODO を埋める。
# React を、Vite の開発サーバーで動かす。/api/ は、backend に転送する（vite.config.ts）。
FROM node:22-slim
WORKDIR /app
RUN corepack enable pnpm
# TODO: package.json・pnpm-lock.yaml・pnpm-workspace.yaml をコピーして、pnpm install --frozen-lockfile で依存を入れる
COPY . .
EXPOSE 5173
CMD ["pnpm", "run", "dev", "--host", "0.0.0.0"]
