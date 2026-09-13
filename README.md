<<<<<<< HEAD
# Local KNN Prediction API

Project triển khai REST API phân loại bằng K-Nearest Neighbors, chạy được trực tiếp trên máy local hoặc bằng Docker.

## Cấu trúc

- `app/model.py`: chuẩn hóa dữ liệu, tính Euclidean distance và bỏ phiếu KNN.
- `app/schemas.py`: schema request/response và validation 3 features.
- `app/main.py`: FastAPI endpoints.
- `tests/test_api.py`: kiểm thử health check, dự đoán và dữ liệu không hợp lệ.
- `Dockerfile`, `docker-compose.yml`: đóng gói và health check container.

## Chạy local

Yêu cầu Python 3.11+.

```bash
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload --port 3000
```

Kiểm tra:

```bash
curl http://localhost:3000/health
curl -X POST http://localhost:3000/api/v1/predict ^
  -H "Content-Type: application/json" ^
  -d "{\"features\":[1.2,3.4,5.6]}"
```

Swagger UI có tại `http://localhost:3000/docs`.

## Test bằng Postman

Tạo biến môi trường `baseUrl` với giá trị `http://localhost:3000`. Với các request
POST, chọn `Body > raw > JSON` và thêm header `Content-Type: application/json`.

### Case 1: Health check thành công

- Method: `GET`
- URL: `{{baseUrl}}/health`
- Body: không có
- Expected status: `200`

Expected response:

```json
{
  "success": true,
  "status": 200,
  "message": "API and KNN model are healthy",
  "model_ready": true,
  "k_neighbors": 5
}
```

### Case 2: Dự đoán class_0 thành công

- Method: `POST`
- URL: `{{baseUrl}}/api/v1/predict`
- Expected status: `200`

```json
{
  "features": [1.0, 1.2, 1.1]
}
```

Expected value: `data.prediction = "class_0"`.

### Case 3: Dự đoán class_1 thành công

- Method: `POST`
- URL: `{{baseUrl}}/api/v1/predict`
- Expected status: `200`

```json
{
  "features": [5.0, 5.0, 5.0]
}
```

Expected value: `data.prediction = "class_1"`.

### Case 4: Dự đoán class_2 thành công

- Method: `POST`
- URL: `{{baseUrl}}/api/v1/predict`
- Expected status: `200`

```json
{
  "features": [9.0, 9.0, 9.0]
}
```

Expected value: `data.prediction = "class_2"`.

### Case 5: Thiếu feature

- Method: `POST`
- URL: `{{baseUrl}}/api/v1/predict`
- Expected status: `422`

```json
{
  "features": [1.0, 2.0]
}
```

### Case 6: Thừa feature

- Method: `POST`
- URL: `{{baseUrl}}/api/v1/predict`
- Expected status: `422`

```json
{
  "features": [1.0, 2.0, 3.0, 4.0]
}
```

### Case 7: Sai kiểu dữ liệu feature

- Method: `POST`
- URL: `{{baseUrl}}/api/v1/predict`
- Expected status: `422`

```json
{
  "features": ["one", 2.0, 3.0]
}
```

### Case 8: Thiếu trường features

- Method: `POST`
- URL: `{{baseUrl}}/api/v1/predict`
- Expected status: `422`

```json
{}
```

Các response lỗi `422` do FastAPI/Pydantic trả về và có trường `detail` mô tả
vị trí dữ liệu không hợp lệ.

## Chạy test

```bash
python -m pytest -q
```

## Chạy bằng Docker

```bash
docp --buildker compose u
```

Container lắng nghe tại port `3000`. Compose kiểm tra `GET /health` mỗi 30 giây.

## Dữ liệu và KNN

Mô hình dùng 9 điểm tham chiếu cố định với 3 đặc trưng số và 3 lớp (`class_0`, `class_1`, `class_2`). Trước khi tính khoảng cách, mỗi đặc trưng được chuẩn hóa theo mean và độ lệch chuẩn của tập tham chiếu. Với `k=5`, mô hình chọn 5 khoảng cách Euclidean nhỏ nhất và trả về lớp xuất hiện nhiều nhất. Giá trị K lẻ giúp tránh hòa phiếu trong bài toán phân loại.

Request hợp lệ:

```json
{ "features": [1.2, 3.4, 5.6] }
```

Response thành công có dạng:

```json
{
  "success": true,
  "status": 200,
  "message": "K-Nearest Neighbors prediction succeeded",
  "data": {
    "model": "knn",
    "endpoint": "/api/v1/predict",
    "prediction": "class_1",
    "k_neighbors": 5,
    "health_status": "healthy"
  }
}
```

