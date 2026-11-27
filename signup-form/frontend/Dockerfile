# Khung dùng cho bài ④ của form đăng ký người dùng. Hãy điền các chỗ TODO.
# Chạy React bằng dev server của Vite. /api/ được chuyển tiếp sang backend (vite.config.ts).
FROM node:22-slim
WORKDIR /app
RUN corepack enable pnpm
# TODO: copy package.json, pnpm-lock.yaml, pnpm-workspace.yaml rồi cài thư viện bằng pnpm install --frozen-lockfile
COPY . .
EXPOSE 5173
CMD ["pnpm", "run", "dev", "--host", "0.0.0.0"]
