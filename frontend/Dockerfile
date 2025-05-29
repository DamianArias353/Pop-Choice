# ---------- build stage ----------
FROM node:20-alpine AS builder
WORKDIR /web
COPY package*.json ./
# Usa npm ci cuando existe package‑lock.json; si no, cae a npm install
RUN if [ -f package-lock.json ]; then \
      npm ci --no-audit --progress=false ; \
    else \
      npm install --no-audit --progress=false ; \
    fi
COPY . .
RUN npm run build          # genera /web/dist

# ---------- runtime stage ----------
FROM nginx:alpine
COPY --from=builder /web/dist /usr/share/nginx/html
# opcional: copia tu propio nginx.conf si quieres SPA fallback
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]