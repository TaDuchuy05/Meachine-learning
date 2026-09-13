from typing import Literal

from pydantic import BaseModel, Field


class PredictRequest(BaseModel):
    features: list[float] = Field(..., min_length=3, max_length=3)


class PredictionData(BaseModel):
    model: Literal["knn"]
    endpoint: str
    prediction: str
    k_neighbors: int
    health_status: Literal["healthy"]


class PredictResponse(BaseModel):
    success: bool
    status: int
    message: str
    data: PredictionData


class HealthResponse(BaseModel):
    success: bool
    status: int
    message: str
    model_ready: bool
    k_neighbors: int
