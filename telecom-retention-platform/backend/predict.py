# predict.py
import pickle
import pandas as pd
import numpy as np
import os

# ── Load model artifacts once at startup ──────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, 'models')

with open(os.path.join(MODEL_DIR, 'best_model.pkl'), 'rb') as f:
    model = pickle.load(f)

with open(os.path.join(MODEL_DIR, 'scaler.pkl'), 'rb') as f:
    scaler = pickle.load(f)

with open(os.path.join(MODEL_DIR, 'feature_names.pkl'), 'rb') as f:
    feature_names = pickle.load(f)

print("Model artifacts loaded successfully")


def preprocess_input(customer: dict) -> pd.DataFrame:
    """
    Convert raw customer input into the encoded format
    the model expects. Mirrors the preprocessing in Notebook 2.
    """
    df = pd.DataFrame([customer])

    # ── Engineer features ──────────────────────────────────────
    # Tenure group
    def tenure_group(t):
        if t <= 12:   return 'Early'
        elif t <= 24: return 'Developing'
        elif t <= 48: return 'Established'
        else:         return 'Loyal'

    df['TenureGroup'] = df['tenure'].apply(tenure_group)

    # Service count
    service_cols = [
        'PhoneService', 'MultipleLines', 'InternetService',
        'OnlineSecurity', 'OnlineBackup', 'DeviceProtection',
        'TechSupport', 'StreamingTV', 'StreamingMovies'
    ]
    def count_services(row):
        count = 0
        for col in service_cols:
            if row[col] not in ['No', 'No phone service',
                                 'No internet service']:
                count += 1
        return count

    df['ServiceCount'] = df.apply(count_services, axis=1)

    # High risk flag
    df['IsHighRisk'] = (
        (df['Contract'] == 'Month-to-month') &
        (df['tenure'] <= 12) &
        (df['MonthlyCharges'] > 65)
    ).astype(int)

    # Charges category
    def charges_cat(c):
        if c < 35:   return 'Low'
        elif c < 65: return 'Medium'
        else:        return 'High'

    df['ChargesCategory'] = df['MonthlyCharges'].apply(charges_cat)

    # Premium services
    df['HasPremiumServices'] = (
        (df['StreamingTV'] == 'Yes') &
        (df['StreamingMovies'] == 'Yes')
    ).astype(int)

    # ── Label encode binary columns ───────────────────────────
    binary_map = {'Yes': 1, 'No': 0,
                  'Male': 1, 'Female': 0}
    binary_cols = [
        'gender', 'Partner', 'Dependents',
        'PhoneService', 'PaperlessBilling', 'SeniorCitizen'
    ]
    for col in binary_cols:
        df[col] = df[col].map(binary_map)

    # ── One hot encode multi-category columns ─────────────────
    ohe_cols = [
        'MultipleLines', 'InternetService', 'OnlineSecurity',
        'OnlineBackup', 'DeviceProtection', 'TechSupport',
        'StreamingTV', 'StreamingMovies', 'Contract',
        'PaymentMethod', 'TenureGroup', 'ChargesCategory'
    ]
    df = pd.get_dummies(df, columns=ohe_cols)

    # ── Align columns with training features ──────────────────
    # Add missing columns as 0
    for col in feature_names:
        if col not in df.columns:
            df[col] = 0

    # Keep only training columns in correct order
    df = df[feature_names]

    # ── Scale numerical features ──────────────────────────────
    numerical_cols = ['tenure', 'MonthlyCharges',
                      'TotalCharges', 'ServiceCount']
    df[numerical_cols] = scaler.transform(df[numerical_cols])

    return df


def generate_risk_factors(customer: dict,
                           churn_prob: float) -> list:
    """
    Generate human-readable risk factors based on
    customer attributes and churn probability.
    """
    factors = []

    if customer['Contract'] == 'Month-to-month':
        factors.append(
            "Month-to-month contract — no long term commitment"
        )
    if customer['tenure'] <= 12:
        factors.append(
            f"New customer — only {customer['tenure']} months "
            f"tenure, highest churn risk window"
        )
    if customer['PaymentMethod'] == 'Electronic check':
        factors.append(
            "Electronic check payment — associated with "
            "45% churn rate in historical data"
        )
    if customer['InternetService'] == 'Fiber optic':
        factors.append(
            "Fiber optic subscriber — segment shows "
            "41.9% churn rate"
        )
    if customer['MonthlyCharges'] > 65:
        factors.append(
            f"High monthly charges (${customer['MonthlyCharges']}"
            f") — above average for churned customers"
        )
    if not factors:
        factors.append(
            "No major individual risk factors detected — "
            "risk driven by combination of attributes"
        )

    return factors


def generate_recommendations(customer: dict,
                              churn_prob: float) -> list:
    """
    Generate actionable retention recommendations
    based on customer risk profile.
    """
    recommendations = []

    if customer['Contract'] == 'Month-to-month':
        recommendations.append({
            "action": "Offer annual contract upgrade",
            "detail": "Provide 15-20% discount on first "
                      "annual contract to reduce churn risk "
                      "from 42.7% to 11.3%",
            "priority": "High",
            "team": "Retention Marketing"
        })

    if customer['tenure'] <= 12:
        recommendations.append({
            "action": "Enroll in onboarding program",
            "detail": "Assign to 90-day structured onboarding "
                      "journey with proactive check-ins at "
                      "day 30, 60, and 90",
            "priority": "High",
            "team": "Customer Success"
        })

    if customer['PaymentMethod'] == 'Electronic check':
        recommendations.append({
            "action": "Migrate to automatic payment",
            "detail": "Offer $10 bill credit to switch to "
                      "bank transfer or credit card — "
                      "reduces churn risk significantly",
            "priority": "Medium",
            "team": "Billing Operations"
        })

    if customer['InternetService'] == 'Fiber optic':
        recommendations.append({
            "action": "Fiber optic loyalty offer",
            "detail": "Schedule proactive service quality "
                      "check and offer loyalty pricing "
                      "if tenure is under 24 months",
            "priority": "Medium",
            "team": "Customer Experience"
        })

    if not recommendations:
        recommendations.append({
            "action": "Standard retention monitoring",
            "detail": "Customer shows low churn risk — "
                      "maintain regular engagement touchpoints",
            "priority": "Low",
            "team": "Customer Success"
        })

    return recommendations


def predict_churn(customer_data: dict) -> dict:
    """
    Main prediction function.
    Takes raw customer dict, returns full prediction response.
    """
    # Preprocess
    processed = preprocess_input(customer_data)

    # Predict
    churn_prob = float(
        model.predict_proba(processed)[0][1]
    )

    # Risk band
    if churn_prob >= 0.7:
        risk_band = "High Risk"
        confidence = "High"
    elif churn_prob >= 0.4:
        risk_band = "Medium Risk"
        confidence = "Medium"
    else:
        risk_band = "Low Risk"
        confidence = "High"

    # Revenue at risk
    revenue_at_risk = round(
        customer_data['MonthlyCharges'] * churn_prob, 2
    )

    # Risk factors and recommendations
    risk_factors = generate_risk_factors(
        customer_data, churn_prob
    )
    recommendations = generate_recommendations(
        customer_data, churn_prob
    )

    return {
        "churn_probability": round(churn_prob, 4),
        "churn_prediction": risk_band,
        "confidence": confidence,
        "estimated_monthly_revenue_at_risk": revenue_at_risk,
        "risk_factors": risk_factors,
        "recommendations": recommendations,
        "model_used": "XGBoost",
        "model_recall": 0.727
    }