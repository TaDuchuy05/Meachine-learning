from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app.model import KNNModel
from app.schemas import HealthResponse, PredictRequest, PredictResponse

model = KNNModel(k=5)
model.fit_default_data()


@asynccontextmanager
async def lifespan(_: FastAPI):
    yield


app = FastAPI(
    title="Local KNN Prediction API",
    version="1.0.0",
    description="Local REST API for a from-scratch K-Nearest Neighbors classifier.",
    lifespan=lifespan,
)


@app.get("/health", response_model=HealthResponse, tags=["system"])
def health() -> HealthResponse:
    return HealthResponse(
        success=True,
        status=200,
        message="API and KNN model are healthy",
        model_ready=model.is_ready,
        k_neighbors=model.k,
    )


@app.post("/api/v1/predict", response_model=PredictResponse, tags=["prediction"])
def predict(request: PredictRequest) -> PredictResponse | JSONResponse:
    if not model.is_ready:
        return JSONResponse(status_code=503, content={"detail": "Model is not ready"})

    prediction = model.predict(request.features)
    return PredictResponse(
        success=True,
        status=200,
        message="K-Nearest Neighbors prediction succeeded",
        data={
            "model": "knn",
            "endpoint": "/api/v1/predict",
            "prediction": prediction,
            "k_neighbors": model.k,
            "health_status": "healthy",
        },
    )
