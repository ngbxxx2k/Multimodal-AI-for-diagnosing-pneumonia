# ==========================================
# PneumoScanAI - Hugging Face Spaces
# ==========================================
FROM python:3.10-slim

# Cài đặt thư viện hệ thống cần thiết cho OpenCV headless
RUN apt-get update && apt-get install -y --no-install-recommends \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

# Tạo user non-root (yêu cầu bảo mật của HF Spaces)
RUN useradd -m -u 1000 user
USER user
ENV PATH="/home/user/.local/bin:$PATH"

WORKDIR /app

# Copy requirements trước để tận dụng Docker cache
COPY --chown=user requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy toàn bộ code vào container
COPY --chown=user . .

# Mở port 7860 (yêu cầu của Hugging Face Spaces)
EXPOSE 7860

# Chạy FastAPI bằng Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]
