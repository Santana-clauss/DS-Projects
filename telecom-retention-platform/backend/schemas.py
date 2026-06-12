# schemas.py
from pydantic import BaseModel
from typing import Optional

class CustomerInput(BaseModel):
    # Demographics
    gender: str                    # Male or Female
    SeniorCitizen: str             # Yes or No
    Partner: str                   # Yes or No
    Dependents: str                # Yes or No

    # Service info
    tenure: int                    # months 0-72
    PhoneService: str              # Yes or No
    MultipleLines: str             # Yes, No, No phone service
    InternetService: str           # DSL, Fiber optic, No
    OnlineSecurity: str            # Yes, No, No internet service
    OnlineBackup: str
    DeviceProtection: str
    TechSupport: str
    StreamingTV: str
    StreamingMovies: str

    # Contract and billing
    Contract: str         # Month-to-month, One year, Two year
    PaperlessBilling: str          # Yes or No
    PaymentMethod: str             # Electronic check etc
    MonthlyCharges: float          # e.g. 65.50
    TotalCharges: float            # e.g. 786.00


class PredictionOutput(BaseModel):
    # Core prediction
    churn_probability: float       # 0.0 to 1.0
    churn_prediction: str          # High Risk, Medium Risk, Low Risk
    confidence: str                # High, Medium, Low

    # Business context
    estimated_monthly_revenue_at_risk: float
    risk_factors: list             # Top reasons for risk score

    # Recommendations
    recommendations: list          # Actionable retention suggestions

    # Model info
    model_used: str
    model_recall: float


class HealthResponse(BaseModel):
    status: str
    model_loaded: bool
    api_version: str


class ModelInfoResponse(BaseModel):
    model_name: str
    recall: float
    auc_roc: float
    f1_score: float
    training_features: int
    selection_reason: str