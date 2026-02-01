# 🫁 Multimodal AI - Trợ Lý Chẩn Đoán Hình Ảnh (PneumoScan AI)

> Ứng dụng AI y tế tiên tiến kết hợp Computer Vision và Large Language Models (LLM) để hỗ trợ bác sĩ chẩn đoán viêm phổi từ ảnh X-quang và dữ liệu lâm sàng.

![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white)
![Groq](https://img.shields.io/badge/Groq(Llama3)-F55036?style=for-the-badge&logo=pytorch&logoColor=white)
![TailwindCSS](https://img.shields.io/badge/TailwindCSS-06B6D4?style=for-the-badge&logo=tailwindcss&logoColor=white)

---

## 📖 Mục Lục

- [📖 Giới Thiệu](#-giới-thiệu-dự-án)
- [🌟 Tính Năng Chính](#-tính-năng-chính)
- [🏗️ Kiến Trúc Hệ Thống](#️-kiến-trúc-hệ-thống)
- [🛠️ Công Nghệ Sử Dụng](#️-công-nghệ-sử-dụng)
- [🚀 Hướng Dẫn Cài Đặt](#-hướng-dẫn-cài-đặt-và-chạy)
- [📖 Hướng Dẫn Sử Dụng](#-hướng-dẫn-sử-dụng)

---

## 📖 Giới Thiệu Dự Án

**PneumoScan AI** là một hệ thống hỗ trợ quyết định lâm sàng, được thiết kế theo kiến trúc phân tích đa phương thức (multimodal).

**Thành phần thị giác máy tính** sử dụng các mô hình học sâu để phát hiện và định vị các vùng bất thường trên ảnh X-quang ngực, đồng thời trích xuất đặc trưng hình ảnh phục vụ cho quá trình phân tích tiếp theo. Các mô hình này không đưa ra chẩn đoán bệnh danh mà chỉ cung cấp thông tin định vị và đặc trưng hình ảnh.

**Thành phần lập luận y khoa** tổng hợp các đặc trưng hình ảnh cùng dữ liệu lâm sàng của bệnh nhân (xét nghiệm máu, sinh hiệu) nhằm hỗ trợ bác sĩ trong việc đánh giá nguy cơ, phân tầng mức độ và định hướng xử trí. Hệ thống không thay thế bác sĩ mà đóng vai trò hỗ trợ ra quyết định dựa trên dữ liệu hiện có.


---

## 🌟 Tính Năng Chính

### 🏥 Phân Tích Đa Phương Thức
- **Dữ liệu hình ảnh**: Xử lý ảnh X-quang ngực thẳng (PA/AP).
- **Dữ liệu lâm sàng**: Tích hợp các chỉ số quan trọng như Bạch cầu (WBC), CRP, SpO2, Tuổi, v.v.

### 🤖 Core AI Engine (Backend)
- **Phân Loại (Classification)**: Sử dụng **DenseNet121** để xác định xác suất viêm phổi.
- **Phân Vùng (Segmentation)**: Sử dụng **U-Net** (ResNet34 backbone) để tách vùng phổi, loại bỏ nhiễu từ xương/mô mềm.
- **Phát Hiện (Detection)**: Sử dụng **YOLOv8** để khoanh vùng (Bounding Box) các đám mờ bất thường.
- **Tổng Hợp (Reasoning)**: Sử dụng **LLM Llama 3.3 (via Groq Cloud)** để đóng vai trò bác sĩ, tổng hợp báo cáo.

### 📊 Đánh Giá Rủi Ro Tự Động
- Tự động tính điểm **CURB-65** / **CRB-65** để đánh giá mức độ nghiêm trọng.
- Phân tầng rủi ro (Ngoại trú vs Nhập viện).

---

## 🏗️ Kiến Trúc Hệ Thống

```mermaid
graph LR
    User -->|1. Upload Image| Frontend
    Frontend -->|2. POST /analyze| Backend[FastAPI Backend]
    
    subgraph AI_Engine
        Backend -->|3. Invoke| Orchestrator
        
        Orchestrator -->|4. Request| Vision[Vision Engine]
        
        subgraph Vision_Models
            Vision -->|5. Segment| UNet[U-Net]
            Vision -->|6. Classify| DenseNet[DenseNet]
            Vision -->|7. Detect| YOLO[YOLO]
        end
        
        UNet -- 5b. Mask --> Orchestrator
        DenseNet -- 6b. Pneumonia Prob --> Orchestrator
        YOLO -- 7b. Bounding Boxes --> Orchestrator
        
        Orchestrator -->|8. Send Context| LLM[Groq LLM<br/>Llama 3.3]
    end
    
    LLM -->|9. Generate Report| Orchestrator
    Orchestrator -->|10. FinalResponseDTO| Backend
    Backend -->|11. JSON Response| Frontend

```

---

## 🛠️ Công Nghệ Sử Dụng

### Frontend 🎨
*   **React 19**: Library UI mới nhất.
*   **Vite**: Build tool siêu tốc.
*   **TypeScript**: Đảm bảo type-safety cho dữ liệu y tế.
*   **TailwindCSS**: Styling hiện đại, responsive.

### Backend ⚙️
*   **FastAPI**: Python web framework hiệu năng cao.
*   **PyTorch & TensorFlow**: Chạy các model AI chuyên biệt.
*   **Albumentations / OpenCV**: Xử lý ảnh y tế.
*   **Groq Cloud API**: Chạy mô hình ngôn ngữ lớn (LLM) với tốc độ thời gian thực.

---

## 🚀 Hướng Dẫn Cài Đặt và Chạy

### 1️⃣ Thiết lập Backend

```bash
cd backend

# Tạo môi trường ảo (Khuyến nghị)
python -m venv venv
venv\Scripts\activate   # Windows

# Cài đặt thư viện
pip install -r requirements.txt
```

**Cấu hình Environment:**
Tạo file `.env` trong thư mục `backend/` dựa trên mẫu bên dưới. **Quan trọng**: Cần có API Key của Groq.

```ini
# .env
GROQ_API_KEY=gsk_your_groq_api_key_here
PORT=8000
HOST=0.0.0.0
```

**Chạy Server:**
```bash
python main.py
# Server chạy tại: http://localhost:8000
```

### 2️⃣ Thiết lập Frontend

```bash
cd frontend

# Cài đặt packages
npm install

# Chạy dev server
npm run dev
# App chạy tại: http://localhost:5173
```

---

## 📖 Hướng Dẫn Sử Dụng

1.  Mở trình duyệt tại `http://localhost:5173`.
2.  Nhập thông tin bệnh nhân (Tuổi, Nhiệt độ, SP02...).
3.  Upload ảnh X-quang.
4.  Nhấn **Analyze**. Hệ thống sẽ:
    *   Hiển thị vùng tổn thương trên ảnh.
    *   Đưa ra chẩn đoán xác suất.
    *   Viết báo cáo chi tiết kèm khuyến nghị điều trị.
