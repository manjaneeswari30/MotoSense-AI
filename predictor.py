"""
MotoSense AI risk estimator.

This starter uses transparent rules rather than pretending to have a validated
motorcycle-failure ML model. The included training script creates a synthetic
demo dataset and trains a scikit-learn model for experimentation. Its results
must not be treated as real mechanical diagnostics.
"""
MODEL_NOTE = ("Demo estimate only: rules use the supplied sample thresholds. "
              "This is not a validated diagnostic tool and does not replace a qualified mechanic.")


def predict_risk(odometer_km, days_since_service, engine_temp_c, vibration_mm_s):
    score = 0
    reasons = []

    if odometer_km >= 20000:
        score += 1
        reasons.append("Odometer is at or above 20,000 km")
    if days_since_service >= 180:
        score += 1
        reasons.append("At least 180 days since the last service")
    if engine_temp_c >= 105:
        score += 2
        reasons.append("Engine temperature is high for this demo's thresholds")
    elif engine_temp_c >= 95:
        score += 1
        reasons.append("Engine temperature is elevated for this demo's thresholds")
    if vibration_mm_s >= 7:
        score += 2
        reasons.append("Vibration reading is high for this demo's thresholds")
    elif vibration_mm_s >= 4:
        score += 1
        reasons.append("Vibration reading is elevated for this demo's thresholds")

    if score >= 3:
        level = "High"
        advice = "Arrange an inspection soon; stop riding if warning signs or unsafe behaviour occur."
    elif score >= 1:
        level = "Medium"
        advice = "Review the service schedule and consider a qualified inspection."
    else:
        level = "Low"
        advice = "No risk flags from the demo rules. Continue routine maintenance and follow the owner's manual."

    return {"risk_level": level, "risk_score": score, "risk_reasons": reasons, "advice": advice}
