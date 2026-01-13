from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from util import PricePredictionService
from pydantic import BaseModel, Field
from fastapi import HTTPException
from fastapi.responses import JSONResponse

app = FastAPI(title="Real Estate Price Prediction API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


service = PricePredictionService()
service.load_artifacts()


class PriceRequest(BaseModel):
    total_sqft: float = Field(..., gt=0,
                              description="Total area in square feet")
    bhk: int = Field(..., ge=1, le=10)
    bath: int = Field(..., ge=1, le=10)
    location: str = Field(..., min_length=2)
    address: str | None = Field(
        default=None,
        description="Optional full property address"
    )


@app.get("/")
def root():
    return {
        "message": "Real Estate Price Prediction API is running",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "model_loaded": service.model is not None,
        "features": len(service.data_columns)
    }


@app.get("/locations")
def get_locations():
    return {
        "count": len(service.locations),
        "locations": service.locations
    }


@app.post("/predict")
def predict_price(request: PriceRequest):
    price = service.predict_price(
        request.location,
        request.total_sqft,
        request.bhk,
        request.bath
    )

    return {
        "estimated_price": price,
        "currency": "INR",
        "location": request.location,
        "address": request.address
    }


@app.exception_handler(Exception)
def global_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error"}
    )
