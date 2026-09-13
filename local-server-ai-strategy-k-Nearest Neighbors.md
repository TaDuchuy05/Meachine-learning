### Hướng dẫn tích hợp Máy chủ Cục bộ và Chiến lược Triển khai AI

#### Chủ đề: Thiết lập, Kiểm thử và Triển khai mô hình K-Nearest Neighbors (KNN Model Integration)

---

### 1. Mục tiêu

- Vận hành đồng thời API Service Server và máy chủ AI sử dụng mô hình K-Nearest Neighbors (KNN) ổn định trên máy tính cục bộ.
- Làm chủ hoàn toàn mã nguồn, đặc biệt là quy trình chuẩn bị dữ liệu, tính khoảng cách, tìm K láng giềng gần nhất và dự đoán của mô hình KNN.
- Thực hiện ảo hóa bằng Docker để đồng bộ môi trường chạy mô hình giữa môi trường phát triển cục bộ và Production.
- Đóng gói, kiểm thử Endpoint dự đoán, kiểm tra trạng thái hệ thống và triển khai mô hình KNN ổn định trên Production.

---

### 2. Công nghệ bắt buộc

- Docker
- K-Nearest Neighbors Model (Mô hình K láng giềng gần nhất)
- Data Preprocessing (Tiền xử lý dữ liệu)
- Model Training & Prediction (Huấn luyện và dự đoán)
- API Service Server (Máy chủ dịch vụ tích hợp)
- RESTful Endpoint
- Health Check Monitoring (Kiểm tra trạng thái hệ thống)
- Command Line Testing Tools (Kiểm thử qua dòng lệnh)

---

### 3. Kiến trúc

Áp dụng kiến trúc đa cấu phần (Multi-component Architecture), trong đó API Server tiếp nhận dữ liệu đầu vào, chuyển dữ liệu cho tầng tiền xử lý và mô hình K-Nearest Neighbors, sau đó trả về lớp dự đoán cùng thông tin liên quan đến kết quả dự đoán.

```text
Hệ thống tích hợp (Local Integration Suite)

Cục bộ (Local Machine) / Container:
 ├── Component 1 (API Endpoint)
 ├── Component 2 (Tiền xử lý dữ liệu)
 ├── KNN Model (Tính khoảng cách & tìm K láng giềng gần nhất)
 └── Docker Environment (Môi trường ảo hóa)
```

Tách riêng API, tiền xử lý và mô hình KNN để có thể kiểm thử từng thành phần độc lập.

---

### 4. Luồng hoạt động chi tiết

#### 4.1 Thiết kế cấu phần (Component Design)

- Dựng API Endpoint đầu tiên để nhận dữ liệu cần phân loại và chạy thử nghiệm độc lập.
- Phân tách riêng bước tiền xử lý dữ liệu, tính toán khoảng cách, tìm K láng giềng gần nhất và trả kết quả dự đoán để dễ kiểm thử.
- Khởi tạo Endpoint và xác định đường dẫn để API giao tiếp với tầng xử lý mô hình.
- Xác định giá trị K phù hợp cho mô hình KNN và cấu hình các tham số cần thiết.

---

#### 4.2 Kiểm thử tham số đầu vào (Parameter Testing)

- Hỗ trợ truyền dữ liệu đầu vào dưới dạng JSON, file hoặc chuỗi dữ liệu tùy theo đặc tả Endpoint.
- Kiểm tra dữ liệu đầu vào sau tiền xử lý trước khi đưa vào mô hình KNN.
- Chuẩn hóa dữ liệu đầu vào để các đặc trưng có cùng thang đo, giúp việc tính khoảng cách đạt hiệu quả tốt hơn.
- Kiểm tra mã trạng thái phản hồi của Endpoint, đồng thời đối chiếu lớp dự đoán với kết quả mong đợi.
- Thực thi lệnh kiểm thử trực tiếp từ dòng lệnh để xác thực Endpoint và mô hình.

---

#### 4.3 Tích hợp máy chủ AI cục bộ (Local AI Integration)

- Chuẩn bị tập dữ liệu và thực hiện tiền xử lý trước khi sử dụng cho mô hình KNN.
- Huấn luyện hoặc nạp tập dữ liệu tham chiếu cần thiết cho quá trình dự đoán của mô hình.
- Khi có request, API Server thực hiện tiền xử lý và chuẩn hóa dữ liệu đầu vào trước khi truyền vào mô hình KNN.
- Mô hình KNN tính khoảng cách giữa dữ liệu đầu vào và các điểm dữ liệu trong tập huấn luyện.
- Mô hình lựa chọn K điểm dữ liệu gần nhất với dữ liệu đầu vào.
- Dựa trên đa số phiếu của K láng giềng gần nhất, mô hình đưa ra lớp dự đoán cuối cùng.
- API Server trả kết quả dự đoán cho người dùng thông qua RESTful Endpoint.
- Vận hành API Server và mô hình KNN trên môi trường cục bộ để kiểm chứng toàn bộ luồng từ input đến prediction.

---

#### 4.4 Đóng gói ảo hóa và Triển khai Production (Dockerization & Production)

- Sử dụng Docker để đóng gói API Server, mã nguồn mô hình KNN và các dependency cần thiết.
- Thiết lập Dockerfile để tạo môi trường chạy thống nhất cho toàn bộ hệ thống.
- Sử dụng Docker Compose để hỗ trợ chạy và quản lý các thành phần của hệ thống.
- Thiết lập Health Check để kiểm tra API và trạng thái mô hình KNN đã sẵn sàng phục vụ dự đoán.
- Kiểm tra khả năng hoạt động của Endpoint trong môi trường Container.
- Thực hiện đóng gói sản phẩm hoàn chỉnh và triển khai lên Production sau khi kiểm thử thành công.

---

### 5. API Response mẫu

Phản hồi Endpoint dự đoán K-Nearest Neighbors thành công:

```json
{
  "success": true,
  "status": 200,
  "message": "Dự đoán K-Nearest Neighbors thành công",
  "data": {
    "model": "knn",
    "endpoint": "/api/v1/predict",
    "prediction": "class_1",
    "k_neighbors": 5,
    "health_status": "healthy"
  }
}
```

---

### 6. Thao tác Docker cơ bản

Tệp cấu hình chạy thử nghiệm cục bộ nhanh:

```bash
# Khởi chạy API Server và mô hình KNN bằng Docker
docker compose up --build

# Kiểm thử Endpoint dự đoán
curl -X POST http://localhost:3000/api/v1/predict \
  -H "Content-Type: application/json" \
  -d '{"features":[1.2,3.4,5.6]}'
```

Sau khi chạy Docker thành công, API Server sẽ sẵn sàng tiếp nhận dữ liệu đầu vào và chuyển dữ liệu đến mô hình KNN để thực hiện dự đoán.

---

### 7. Tiêu chí đánh giá

| Hạng mục                                      | Điểm |
| --------------------------------------------- | ---: |
| Kiến trúc tách cấu phần (Architecture)        |   20 |
| Tiền xử lý & Kiểm thử dữ liệu đầu vào         |   20 |
| Huấn luyện & Dự đoán bằng K-Nearest Neighbors |   25 |
| Đóng gói Container & Cấu hình Docker          |   15 |
| Health Check & Triển khai Production          |   10 |
| Tư duy tự chủ mã nguồn (Code Ownership)       |   10 |

---

### 8. Yêu cầu nộp bài

- Mã nguồn API và mô hình K-Nearest Neighbors hoàn chỉnh.
- Tệp cấu hình Dockerfile và docker-compose.yml.
- Tài liệu mô tả dữ liệu đầu vào, quy trình tiền xử lý, huấn luyện hoặc chuẩn bị dữ liệu, tính khoảng cách và dự đoán.
- Mô tả giá trị K được sử dụng trong mô hình và phương pháp lựa chọn K phù hợp.
- Kịch bản kiểm thử Endpoint bằng dòng lệnh.
- Video hoặc hình ảnh minh chứng hệ thống chạy mô hình K-Nearest Neighbors thành công.

---

### 9. Nguyên lý hoạt động của K-Nearest Neighbors

K-Nearest Neighbors (KNN) là một thuật toán học máy được sử dụng phổ biến cho các bài toán phân loại và dự đoán.

Quy trình hoạt động cơ bản của mô hình gồm:

1. Nhận dữ liệu đầu vào từ người dùng hoặc API.
2. Tiền xử lý và chuẩn hóa dữ liệu.
3. Tính khoảng cách giữa dữ liệu đầu vào với các dữ liệu trong tập tham chiếu.
4. Sắp xếp các khoảng cách từ nhỏ đến lớn.
5. Chọn K điểm dữ liệu gần nhất.
6. Thực hiện bỏ phiếu đa số đối với bài toán phân loại.
7. Trả về lớp có số lượng láng giềng xuất hiện nhiều nhất làm kết quả dự đoán.

Ví dụ:

Nếu lựa chọn K = 5, mô hình sẽ tìm 5 điểm dữ liệu gần nhất với dữ liệu đầu vào. Nếu trong 5 điểm đó có:

- 3 điểm thuộc Class A
- 2 điểm thuộc Class B

Thì mô hình sẽ dự đoán dữ liệu đầu vào thuộc **Class A**.

---

### 10. Luồng xử lý tổng quát của hệ thống

```text
Người dùng
    │
    ▼
API Request
    │
    ▼
API Service Server
    │
    ▼
Tiền xử lý & Chuẩn hóa dữ liệu
    │
    ▼
KNN Model
    │
    ├── Tính khoảng cách
    │
    ├── Tìm K láng giềng gần nhất
    │
    └── Bỏ phiếu đa số
    │
    ▼
Prediction Result
    │
    ▼
API Response
```

Toàn bộ hệ thống được chạy trong môi trường Docker để đảm bảo tính ổn định, dễ triển khai và đồng nhất giữa môi trường phát triển cục bộ và môi trường Production.
