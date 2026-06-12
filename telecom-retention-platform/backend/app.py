# app.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from schemas import (
    CustomerInput, PredictionOutput,
    HealthResponse, ModelInfoResponse
)
from predict import predict_churn, model, feature_names
import uvicorn

# ── Initialize FastAPI app ─────────────────────────────────────
app = FastAPI(
    title="Telecom Churn Prediction API",
    description=(
        "Predicts customer churn probability using XGBoost. "
        "Returns risk score, risk factors, and actionable "
        "retention recommendations."
    ),
    version="1.0.0"
)

# ── CORS — allows Flutter app to call this API ─────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)


# ── Endpoints ──────────────────────────────────────────────────

@app.get("/health", response_model=HealthResponse)
def health_check():
    """
    Check if API is running and model is loaded.
    Flutter app calls this on startup.
    """
    return {
        "status": "healthy",
        "model_loaded": model is not None,
        "api_version": "1.0.0"
    }


@app.get("/model/info", response_model=ModelInfoResponse)
def model_info():
    """
    Returns model performance metrics and metadata.
    """
    return {
        "model_name": "XGBoost Classifier",
        "recall": 0.727,
        "auc_roc": 0.810,
        "f1_score": 0.602,
        "training_features": len(feature_names),
        "selection_reason": (
            "Selected for highest Recall (0.727) — "
            "minimizes missed churners which represent "
            "direct revenue loss to the business"
        )
    }


@app.post("/predict", response_model=PredictionOutput)
def predict(customer: CustomerInput):
    """
    Predict churn probability for a single customer.
    Returns risk score, risk factors, and recommendations.
    """
    try:
        customer_dict = customer.dict()
        result = predict_churn(customer_dict)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(e)}"
        )


@app.post("/predict/batch")
def predict_batch(customers: list[CustomerInput]):
    """
    Predict churn for multiple customers at once.
    Returns list of predictions in same order as input.
    """
    try:
        results = []
        for customer in customers:
            customer_dict = customer.dict()
            result = predict_churn(customer_dict)
            results.append(result)
        return {
            "total_customers": len(results),
            "high_risk_count": sum(
                1 for r in results
                if r['churn_prediction'] == 'High Risk'
            ),
            "predictions": results
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Batch prediction failed: {str(e)}"
        )


# ── Run server ─────────────────────────────────────────────────
if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )