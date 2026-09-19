"""
🌐 AeroSense — Flask backend for AQI monitoring & next-day prediction.
"""

import os
import joblib
import requests
import numpy as np
from datetime import datetime
from flask import Flask, jsonify, render_template, request
import math

# ─────────────────────────────────────────────
#  App init
# ─────────────────────────────────────────────
app = Flask(__name__)

WAQI_TOKEN   = "97926bde88d74ac8e9c433dc0381a9ccad65aa73"
WAQI_URL     = "https://api.waqi.info/feed/{city}/?token={token}"
DEFAULT_CITY = "Gandhinagar"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ─────────────────────────────────────────────
#  Load ML artifacts at startup
# ─────────────────────────────────────────────
try:
    model         = joblib.load(os.path.join(BASE_DIR, "aqi_model.pkl"))
    scaler        = joblib.load(os.path.join(BASE_DIR, "scaler.pkl"))
    feature_names = joblib.load(os.path.join(BASE_DIR, "feature_names.pkl"))
    print(f"[startup] Model loaded. Features: {feature_names}")
except FileNotFoundError as e:
    print(f"[WARNING] Could not load model artifacts: {e}")
    model = scaler = feature_names = None

# ─────────────────────────────────────────────
#  Constants
# ─────────────────────────────────────────────
POPULAR_CITIES = [
    # Popular / Metro
    "Bangalore", "Delhi", "Mumbai", "Chennai", "Kolkata",
    "Hyderabad", "Pune", "Ahmedabad",
    # Andhra Pradesh
    "Visakhapatnam", "Vijayawada", "Tirupati", "Guntur",
    # Assam
    "Guwahati",
    # Bihar
    "Patna", "Gaya", "Muzaffarpur",
    # Chhattisgarh
    "Raipur", "Bilaspur",
    # Delhi NCR
    "Noida", "Gurugram", "Faridabad", "Ghaziabad",
    # Gujarat
    "Surat", "Vadodara", "Rajkot", "Gandhinagar",
    # Haryana
    "Ambala", "Hisar",
    # Jharkhand
    "Ranchi", "Jamshedpur", "Dhanbad",
    # Karnataka
    "Mysuru", "Mangaluru", "Hubli", "Belgaum",
    # Kerala
    "Kochi", "Thiruvananthapuram", "Kozhikode", "Thrissur", "Kannur", "Kollam",
    # Madhya Pradesh
    "Bhopal", "Indore", "Gwalior", "Jabalpur", "Ujjain",
    # Maharashtra
    "Nagpur", "Nashik", "Aurangabad", "Solapur", "Kolhapur", "Navi Mumbai",
    # Odisha
    "Bhubaneswar", "Cuttack", "Rourkela",
    # Punjab
    "Ludhiana", "Amritsar", "Jalandhar", "Chandigarh", "Patiala",
    # Rajasthan
    "Jaipur", "Jodhpur", "Udaipur", "Kota", "Ajmer", "Bikaner",
    # Tamil Nadu
    "Coimbatore", "Madurai", "Tiruchirappalli", "Salem", "Tirunelveli",
    # Telangana
    "Warangal", "Nizamabad",
    # Uttar Pradesh
    "Lucknow", "Kanpur", "Agra", "Varanasi", "Prayagraj",
    "Meerut", "Mathura", "Bareilly",
    # Uttarakhand
    "Dehradun", "Haridwar",
    # West Bengal
    "Howrah", "Durgapur", "Asansol",
    # J&K / Himachal
    "Srinagar", "Jammu", "Shimla",
]

# Expected feature order (must match training)
FEATURE_ORDER = [
    "PM2.5", "PM10", "NO", "NO2", "NOx", "NH3",
    "CO", "SO2", "O3", "Benzene", "Toluene", "Xylene",
    "Month", "DayOfWeek",
]

# City-level typical background concentrations (μg/m³) for imputation
CITY_DEFAULTS = {
    "PM2.5":   30.0,
    "PM10":    60.0,
    "NO":       8.0,
    "NO2":     25.0,
    "NOx":     33.0,
    "NH3":     10.0,
    "CO":       0.9,
    "SO2":      8.0,
    "O3":      35.0,
    "Benzene":  2.0,
    "Toluene":  6.0,
    "Xylene":   1.5,
}

AQI_CATEGORIES = [
    {
        "min": 0,   "max": 50,
        "category": "Good",
        "color":    "#22C55E",
        "advice":   "Air quality is considered satisfactory. Enjoy outdoor activities.",
        "recommendations": [
            "Great day for outdoor exercise",
            "Air quality poses little or no risk",
            "Ideal conditions — open windows for fresh air",
        ],
    },
    {
        "min": 51,  "max": 100,
        "category": "Satisfactory",
        "color":    "#84CC16",
        "advice":   "Air quality is acceptable. Sensitive people should limit prolonged outdoor exertion.",
        "recommendations": [
            "Sensitive groups should limit prolonged outdoor exertion",
            "Keep windows closed during peak traffic hours",
            "Consider using an air purifier indoors",
        ],
    },
    {
        "min": 101, "max": 200,
        "category": "Moderate",
        "color":    "#F59E0B",
        "advice":   "May cause breathing discomfort to people with lung disease, asthma, and heart disease.",
        "recommendations": [
            "People with respiratory conditions should avoid strenuous outdoor activity",
            "Wear a mask if spending extended time outdoors",
            "Keep indoor air clean with purifiers and ventilation filters",
        ],
    },
    {
        "min": 201, "max": 300,
        "category": "Poor",
        "color":    "#F97316",
        "advice":   "May cause breathing discomfort on prolonged exposure. Avoid outdoor activities.",
        "recommendations": [
            "Avoid all prolonged outdoor exertion",
            "Wear an N95 mask when outdoors",
            "Keep windows and doors closed",
            "Run air purifier on medium-high setting",
        ],
    },
    {
        "min": 301, "max": 400,
        "category": "Very Poor",
        "color":    "#EF4444",
        "advice":   "May cause respiratory illness on prolonged exposure. Avoid outdoor activities, use N95 masks.",
        "recommendations": [
            "Avoid all outdoor activity",
            "N95 masks mandatory if going outdoors",
            "Children and elderly should remain indoors",
            "Seal gaps in doors and windows",
            "Run air purifiers at high setting",
        ],
    },
    {
        "min": 401, "max": 500,
        "category": "Severe",
        "color":    "#991B1B",
        "advice":   "Serious health effects. Everyone should avoid outdoor exposure. Stay indoors, use air purifiers.",
        "recommendations": [
            "Do not go outdoors under any circumstances",
            "Seal windows with tape/wet cloth",
            "Run air purifiers at maximum capacity",
            "Seek medical help if experiencing symptoms",
            "Avoid physical exertion even indoors",
        ],
    },
    {
        "min": 501, "max": float("inf"),
        "category": "Hazardous",
        "color":    "#581C87",
        "advice":   "Health emergency. Do not go outside. Seal windows. Run air purifiers at maximum.",
        "recommendations": [
            "HEALTH EMERGENCY — remain indoors",
            "Seal all windows and doors immediately",
            "Air purifiers at maximum — change filters",
            "Call emergency services if feeling unwell",
            "Evacuate area if instructed by authorities",
        ],
    },
]


def get_aqi_info(aqi_value: float) -> dict:
    """Return category metadata for a given AQI value."""
    aqi = max(0.0, float(aqi_value))
    for band in AQI_CATEGORIES:
        if band["min"] <= aqi <= band["max"]:
            return {
                "category":        band["category"],
                "color":           band["color"],
                "health_advice":   band["advice"],
                "recommendations": band["recommendations"],
            }
    # Fallback — should never be reached
    return {
        "category":        "Unknown",
        "color":           "#64748B",
        "health_advice":   "Data unavailable.",
        "recommendations": [],
    }


def safe_float(value, default=0.0) -> float:
    """Safely coerce a value to float, returning default on failure."""
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


# ─────────────────────────────────────────────
#  Routes
# ─────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html", default_city=DEFAULT_CITY)


@app.route("/predict")
def predict_page():
    return render_template("predict.html")


@app.route("/about")
def about_page():
    return render_template("about.html")


@app.route("/api/cities")
def api_cities():
    return jsonify({"cities": POPULAR_CITIES})


@app.route("/api/predict", methods=["POST"])
def api_predict():
    """
    Accept a JSON body with pollutant values and temporal features,
    run the trained XGBoost model, and return the predicted AQI.
    """
    body = request.get_json(force=True, silent=True) or {}

    # Pull each feature with a sensible fallback
    pollutant_map = {
        "PM2.5":   safe_float(body.get("PM2.5"),   CITY_DEFAULTS["PM2.5"]),
        "PM10":    safe_float(body.get("PM10"),    CITY_DEFAULTS["PM10"]),
        "NO":      safe_float(body.get("NO"),      CITY_DEFAULTS["NO"]),
        "NO2":     safe_float(body.get("NO2"),     CITY_DEFAULTS["NO2"]),
        "NOx":     safe_float(body.get("NOx"),     CITY_DEFAULTS["NOx"]),
        "NH3":     safe_float(body.get("NH3"),     CITY_DEFAULTS["NH3"]),
        "CO":      safe_float(body.get("CO"),      CITY_DEFAULTS["CO"]),
        "SO2":     safe_float(body.get("SO2"),     CITY_DEFAULTS["SO2"]),
        "O3":      safe_float(body.get("O3"),      CITY_DEFAULTS["O3"]),
        "Benzene": safe_float(body.get("Benzene"), CITY_DEFAULTS["Benzene"]),
        "Toluene": safe_float(body.get("Toluene"), CITY_DEFAULTS["Toluene"]),
        "Xylene":  safe_float(body.get("Xylene"),  CITY_DEFAULTS["Xylene"]),
    }

    now = datetime.now()
    month       = int(safe_float(body.get("Month"),      now.month))
    day_of_week = int(safe_float(body.get("DayOfWeek"),  now.weekday()))

    # Clamp temporal values to valid ranges
    month       = max(1,  min(12, month))
    day_of_week = max(0,  min(6,  day_of_week))

    feature_vector = [
        pollutant_map.get(f, CITY_DEFAULTS.get(f, 0.0))
        if f not in ("Month", "DayOfWeek")
        else (month if f == "Month" else day_of_week)
        for f in FEATURE_ORDER
    ]

    # Rough estimated current AQI from PM2.5 (for reference display)
    pm25          = pollutant_map["PM2.5"]
    estimated_aqi = round(min(pm25 * 2.5, 500), 1)

    if model is not None and scaler is not None:
        try:
            arr           = np.array(feature_vector, dtype=float).reshape(1, -1)
            scaled        = scaler.transform(arr)
            raw           = float(model.predict(scaled)[0])
            predicted_aqi = max(0.0, round(raw, 1))
        except Exception as exc:
            return jsonify({"success": False, "error": str(exc)}), 500
    else:
        predicted_aqi = round(estimated_aqi * 1.05, 1)

    info = get_aqi_info(predicted_aqi)

    return jsonify({
        "success":       True,
        "predicted_aqi": predicted_aqi,
        "category":      info["category"],
        "color":         info["color"],
        "health_advice": info["health_advice"],
        "recommendations": info["recommendations"],
        "inputs": {k: round(v, 3) for k, v in pollutant_map.items()},
    })


@app.route("/api/aqi")
def api_aqi():
    city = request.args.get("city", DEFAULT_CITY).strip()

    # ── 1. Fetch from WAQI ────────────────────────────────────
    try:
        resp = requests.get(
            WAQI_URL.format(city=city, token=WAQI_TOKEN),
            timeout=8,
        )
        resp.raise_for_status()
        data = resp.json()
    except requests.RequestException as exc:
        return jsonify({"success": False, "error": f"WAQI fetch failed: {exc}"}), 502

    if data.get("status") != "ok":
        return jsonify({
            "success": False,
            "error":   data.get("data", "City not found or API error"),
        }), 404

    waqi_data = data["data"]
    iaqi      = waqi_data.get("iaqi", {})

    # ── 2. Extract pollutants ─────────────────────────────────
    current_aqi          = safe_float(waqi_data.get("aqi"))
    dominant_pollutant   = waqi_data.get("dominentpol", "pm25")

    # Map WAQI keys → model feature names
    pollutant_map = {
        "PM2.5": safe_float(iaqi.get("pm25", {}).get("v"), CITY_DEFAULTS["PM2.5"]),
        "PM10":  safe_float(iaqi.get("pm10", {}).get("v"), CITY_DEFAULTS["PM10"]),
        "NO":    safe_float(iaqi.get("no",   {}).get("v"), CITY_DEFAULTS["NO"]),
        "NO2":   safe_float(iaqi.get("no2",  {}).get("v"), CITY_DEFAULTS["NO2"]),
        "NOx":   safe_float(iaqi.get("nox",  {}).get("v"), CITY_DEFAULTS["NOx"]),
        "NH3":   safe_float(iaqi.get("nh3",  {}).get("v"), CITY_DEFAULTS["NH3"]),
        "CO":    safe_float(iaqi.get("co",   {}).get("v"), CITY_DEFAULTS["CO"]),
        "SO2":   safe_float(iaqi.get("so2",  {}).get("v"), CITY_DEFAULTS["SO2"]),
        "O3":    safe_float(iaqi.get("o3",   {}).get("v"), CITY_DEFAULTS["O3"]),
        "Benzene": CITY_DEFAULTS["Benzene"],
        "Toluene": CITY_DEFAULTS["Toluene"],
        "Xylene":  CITY_DEFAULTS["Xylene"],
    }

    # Temporal features derived from now
    now        = datetime.now()
    month      = now.month
    day_of_week = now.weekday()   # 0=Monday

    # Build feature vector in training order
    feature_vector = [
        pollutant_map.get(f, CITY_DEFAULTS.get(f, 0.0))
        if f not in ("Month", "DayOfWeek")
        else (month if f == "Month" else day_of_week)
        for f in FEATURE_ORDER
    ]

    # ── 3. Predict tomorrow's AQI ─────────────────────────────
    predicted_aqi = None
    pred_info     = {}
    if model is not None and scaler is not None:
        try:
            arr    = np.array(feature_vector, dtype=float).reshape(1, -1)
            scaled = scaler.transform(arr)
            raw    = float(model.predict(scaled)[0])
            predicted_aqi = max(0.0, round(raw, 1))
            pred_info     = get_aqi_info(predicted_aqi)
        except Exception as exc:
            predicted_aqi = None
            pred_info     = {"error": str(exc)}
    else:
        # Graceful degradation when model not available
        predicted_aqi = round(current_aqi * 1.05, 1)
        pred_info     = get_aqi_info(predicted_aqi)

    # ── 4. Current AQI info ───────────────────────────────────
    current_info = get_aqi_info(current_aqi)

    # Friendly pollutant display dict (lower-case keys for JS)
    pollutants_display = {
        "pm25": pollutant_map["PM2.5"],
        "pm10": pollutant_map["PM10"],
        "co":   pollutant_map["CO"],
        "so2":  pollutant_map["SO2"],
        "no2":  pollutant_map["NO2"],
        "o3":   pollutant_map["O3"],
    }

    # Timestamp from WAQI or fallback
    try:
        ts_raw = waqi_data.get("time", {}).get("s", "")
        ts     = ts_raw if ts_raw else now.strftime("%Y-%m-%d %H:%M:%S")
    except Exception:
        ts = now.strftime("%Y-%m-%d %H:%M:%S")

    return jsonify({
        "success": True,
        "city":    city,
        "current": {
            "aqi":                current_aqi,
            "category":           current_info["category"],
            "color":              current_info["color"],
            "health_advice":      current_info["health_advice"],
            "dominant_pollutant": dominant_pollutant,
            "pollutants":         pollutants_display,
            "timestamp":          ts,
        },
        "prediction": {
            "aqi":             predicted_aqi,
            "category":        pred_info.get("category", "N/A"),
            "color":           pred_info.get("color", "#64748B"),
            "health_advice":   pred_info.get("health_advice", ""),
            "recommendations": pred_info.get("recommendations", []),
        },
    })


if __name__ == "__main__":
    app.run(debug=True, port=5001)
