# ==========================================
# PneumoScanAI Frontend - React + Vite + Nginx
# ==========================================

# --- Stage 1: Build ---
FROM node:18-alpine AS build

WORKDIR /app

# Copy package files trước để tận dụng Docker cache
COPY package.json package-lock.json ./
RUN npm ci

# Copy toàn bộ source code
COPY . .

# Đặt biến môi trường API URL trỏ đến backend container
# Biến này được inject lúc build time cho Vite
ARG VITE_API_URL=http://localhost:8000
ENV VITE_API_URL=$VITE_API_URL

# Build production
RUN npm run build

# --- Stage 2: Serve với Nginx ---
FROM nginx:alpine

# Copy custom nginx config
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy build output từ stage 1
COPY --from=build /app/dist /usr/share/nginx/html

# Mở port 80
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
