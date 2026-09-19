<div align="center">

# 🌬️ 🌐 AeroSense

Real-Time Air Quality Monitoring & Next-Day AQI Prediction Using XGBoost

AeroSense AI is a Flask-based Artificial Intelligence and Data Science application designed to monitor real-time air quality and predict the next day's Air Quality Index (AQI) for Indian cities.

The application combines real-time air-quality data, data preprocessing, feature engineering, machine learning, and interactive visualization to provide users with an easy way to understand current air pollution levels and estimated future AQI.

🚀 Project Overview

Air pollution is an important environmental and public-health concern. AeroSense AI provides a data-driven approach to air-quality monitoring by combining real-time pollutant information with a machine-learning model.

The system:

Fetches real-time air-quality information through the WAQI API
Processes pollutant-related data
Performs feature engineering and data preprocessing
Uses an XGBoost regression model for AQI prediction
Provides current AQI information for selected cities
Predicts next-day AQI based on available pollutant information
Displays pollutant levels through an interactive dashboard
Provides AQI categories and corresponding health guidance 

### AI-Powered Air Quality Index Prediction for Indian Cities

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.x-000000?style=flat-square&logo=flask&logoColor=white)](https://flask.palletsprojects.com)
[![XGBoost](https://img.shields.io/badge/XGBoost-3.1.1-FF6600?style=flat-square)](https://xgboost.readthedocs.io)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.6.1-F7931E?style=flat-square&logo=scikit-learn&logoColor=white)](https://scikit-learn.org)
[![License](https://img.shields.io/badge/License-MIT-22C55E?style=flat-square)](LICENSE)

**🌐 AeroSense** combines real-time data from the WAQI API with a gradient-boosted ML model
trained on 6 years of Indian city pollution records to **predict tomorrow's AQI** —
giving you actionable health insights before the day begins.

[Live Dashboard](#️-pages) · [API Docs](#-api-reference) · [ML Pipeline](#-ml-pipeline) · [Quick Start](#-quick-start)

</div>

---

## 📑 Table of Contents

1. [Project Overview](#-project-overview)
2. [Features](#-features)
3. [Screenshots](#-screenshots)
4. [Tech Stack](#️-tech-stack)
5. [Project Structure](#-project-structure)
6. [Dataset](#-dataset)
7. [ML Pipeline](#-ml-pipeline)
8. [Model Performance](#-model-performance)
9. [Quick Start](#-quick-start)
10. [Configuration](#️-configuration)
11. [Pages](#️-pages)
12. [API Reference](#-api-reference)
13. [AQI Reference](#-aqi-reference)
14. [Notebook Walkthrough](#-notebook-walkthrough)
15. [Troubleshooting](#-troubleshooting)

---

## 🔍 Project Overview

🌐 AeroSense is a production-quality, full-stack web application that tackles a real-world environmental problem: **knowing tomorrow's air quality today.**

The system works in two modes:

| Mode | How it works |
|------|-------------|
| **Live City Dashboard** | Fetches real-time sensor data from the WAQI API for any Indian city, pipes it through the trained XGBoost model, and renders current + predicted AQI on an interactive dashboard |
| **Manual Prediction** | Accepts custom pollutant readings (from your own sensors or lab data), runs them through the same ML pipeline, and returns a prediction with health advice |

The model is trained on the **Central Pollution Control Board (CPCB)** dataset sourced from Kaggle — 24,824 cleaned daily records across **29 Indian cities (2015–2020)**.

---

## ✨ Features

### Dashboard (Live Mode)
- 🔴 **Animated SVG Gauge** — circular AQI ring that fills and glows in real-time category color
- 🧪 **Pollutant Breakdown** — 6 glass-morphism cards (PM₂.₅, PM₁₀, CO, SO₂, NO₂, O₃) with animated values and level bars
- 🤖 **AI Forecast Card** — tomorrow's predicted AQI with category badge, health advice, and recommendations
- 📏 **AQI Scale Reference** — colour-banded reference bar with live position markers for current + predicted
- 🏙️ **10 City Selector** — styled dropdown for Bangalore, Delhi, Mumbai, Chennai, Kolkata, Hyderabad, Pune, Ahmedabad, Jaipur, Lucknow
- ⏳ **Skeleton Loaders** — shimmer placeholders while data loads
- 🔔 **Error Toasts** — graceful degradation with in-page notifications

### Manual Prediction Form
- 🎛️ **Synced Sliders + Number Inputs** — drag the slider or type a value; both stay in sync with live-fill gradients
- 📋 **4 Grouped Input Sections** — Particulate Matter, Nitrogen Compounds, Other Gases, Temporal Features
- 📅 **Smart Defaults** — month and day-of-week pre-set to today; all pollutants seeded with realistic city averages
- ✅ **Instant Result Card** — predicted AQI box, scale marker, recommendations — animates into view on submit
- 🔄 **Reset Button** — one click restores all defaults

### About Page
- 📊 **Quick Stats** — 29 cities, 72K+ records, 14 features, 500 trees
- 🔄 **Pipeline Diagram** — 4-step visual flow (Fetch → Engineer → Scale → Predict)
- 🗄️ **Dataset Documentation** — column reference table, data characteristics
- ⚙️ **Model Architecture** — full hyperparameter table, training details, design decisions
- 🎨 **AQI Category Reference** — 7-row table with color-coded categories, health impacts, and actions
- 💻 **Tech Stack Cards** — 6 technology cards with icons and descriptions

### UI/UX Design
- 🌑 **Custom Dark Theme** — `#0A0F1C` deep-navy base, zero Bootstrap
- 🔮 **Glass Morphism** — `backdrop-filter: blur(12px)` cards with subtle borders
- ✨ **Staggered Fade-In** — Intersection Observer drives section animations on scroll
- 📱 **Fully Responsive** — 5 breakpoints (1200px / 900px / 760px / 600px / 420px)
- 🚀 **GPU-Accelerated Animations** — only `transform` and `opacity` used in transitions

---

## 📸 Screenshots

### EDA Visualisations (`eda_plots.png`)
> Generated by Cell 4 of the Jupyter Notebook

- AQI distribution histogram with KDE overlay
- Monthly average AQI trend (2015–2020)
- Pollutant correlation heatmap (lower triangle)
- Top 10 most polluted cities (bar chart)
- AQI distribution by category bucket (boxplot)

### Model Evaluation (`model_evaluation.png`)
> Generated by Cell 7 of the Jupyter Notebook

- Actual vs Predicted scatter plot with R² annotation
- Residual distribution (histogram + KDE)
- Top-12 feature importance (horizontal bar chart)
- Actual vs Predicted line overlay for 100 test samples

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Backend** | Flask 3.x | REST API + Jinja2 server-side rendering |
| **ML Model** | XGBoost 3.1.1 | Gradient-boosted regressor (500 trees) |
| **ML Utils** | scikit-learn 1.6.1 | StandardScaler, metrics, train/test split |
| **Data** | pandas 2.3.3 + NumPy 2.2.6 | Cleaning, imputation, feature engineering |
| **Serialisation** | joblib | Saving/loading model artifacts (`.pkl`) |
| **External Data** | WAQI API | Real-time pollutant readings for Indian cities |
| **Notebook** | Jupyter + matplotlib + seaborn | EDA, training, evaluation |
| **Frontend** | Vanilla JS (ES2020) | Zero-dependency dynamic UI |
| **Styling** | Custom CSS (no Bootstrap) | Dark glassmorphism dashboard design |
| **Fonts** | Google Fonts — Outfit + DM Sans | Headings and body text |

---

## 📁 Project Structure

```
AQI Prediction/
│
├── app.py                    # Flask application — routes, ML inference, API
├── requirements.txt          # Python dependencies (7 packages)
├── AQI_Prediction.ipynb      # Jupyter Notebook — training pipeline (10 cells)
│
├── aqi_model.pkl             # Trained XGBoost regressor (~2.1 MB)
├── scaler.pkl                # Fitted StandardScaler (~1.3 KB)
├── feature_names.pkl         # Ordered list of 14 feature names
│
├── eda_plots.png             # EDA visualisations output
├── model_evaluation.png      # Model performance plots output
│
├── dataset/
│   ├── city_day.csv          # ✅ PRIMARY — daily AQI by city (2.5 MB, used for training)
│   ├── city_hour.csv         # Hourly granularity (63 MB)
│   ├── station_day.csv       # Station-level daily (8.2 MB)
│   ├── station_hour.csv      # Station-level hourly (209 MB)
│   └── stations.csv          # Station metadata + coordinates (14 KB)
│
├── templates/
│   ├── index.html            # Dashboard — live AQI + prediction
│   ├── predict.html          # Manual prediction form
│   └── about.html            # Project documentation page
│
└── static/
    ├── css/
    │   └── style.css         # Complete styling system (~1,600 lines)
    └── js/
        ├── app.js            # Dashboard logic — fetch, animate, render
        └── predict.js        # Prediction form — sliders, submit, result
```

---

## 🗄️ Dataset

**Source:** [Air Quality Data in India — Kaggle (CPCB)](https://www.kaggle.com/datasets/rohanrao/air-quality-data-in-india)

### Primary File: `city_day.csv`

| Property | Value |
|----------|-------|
| Rows | 29,531 (raw) → 24,824 (after cleaning) |
| Cities | 29 major Indian cities |
| Date Range | January 2015 — July 2020 |
| Frequency | Daily averaged readings |

### Columns

| Column | Type | Unit | Missing % |
|--------|------|------|-----------|
| City | Categorical | — | 0% |
| Date | Date | YYYY-MM-DD | 0% |
| PM2.5 | Pollutant | μg/m³ | 17.9% |
| PM10 | Pollutant | μg/m³ | 37.6% |
| NO | Pollutant | μg/m³ | 19.3% |
| NO2 | Pollutant | μg/m³ | 18.9% |
| NOx | Pollutant | ppb | 19.3% |
| NH3 | Pollutant | μg/m³ | 34.9% |
| CO | Pollutant | mg/m³ | 18.5% |
| SO2 | Pollutant | μg/m³ | 17.1% |
| O3 | Pollutant | μg/m³ | 20.7% |
| Benzene | VOC | μg/m³ | 29.2% |
| Toluene | VOC | μg/m³ | 38.5% |
| Xylene | VOC | μg/m³ | 61.3% |
| **AQI** | Target | 0–500+ | 15.8% |
| AQI_Bucket | Category | Text | 15.8% |

### Data Cleaning Steps

1. **Drop null AQI rows** — removes 4,681 rows (AQI is non-negotiable for training)
2. **City-level median imputation** — fills missing pollutants using the median for that specific city
3. **Global median fallback** — any remaining NaNs filled with the overall dataset median
4. **Date parsing** — `Date` column converted to `datetime64`, `Year`, `Month`, `DayOfWeek` extracted
5. **Target creation** — `AQI_Tomorrow = AQI.shift(-1)` within each city group
6. **Drop boundary rows** — removes last record per city (no "tomorrow" data available)

---

## 🤖 ML Pipeline

```
Raw Data (city_day.csv)
        │
        ▼
┌───────────────────┐
│  Data Cleaning    │  Drop null AQI, city-median imputation
└─────────┬─────────┘
          │
          ▼
┌───────────────────┐
│ Feature Eng.      │  Parse dates → Month, DayOfWeek
│                   │  Shift AQI by -1 → AQI_Tomorrow (target)
└─────────┬─────────┘
          │
          ▼
┌───────────────────┐     ┌──────────────────────┐
│ Train/Test Split  │────►│ 80% Train / 20% Test  │
│ (random, seed=42) │     │ 19,859  /  4,965 rows │
└─────────┬─────────┘     └──────────────────────┘
          │
          ▼
┌───────────────────┐
│ StandardScaler    │  Fit on train only → transform both sets
│ (saved to pkl)    │  Prevents data leakage
└─────────┬─────────┘
          │
          ▼
┌───────────────────┐     n_estimators=500, max_depth=6
│  XGBRegressor     │     learning_rate=0.05, subsample=0.8
│  (saved to pkl)   │     colsample_bytree=0.8
│                   │     reg_alpha=0.1, reg_lambda=1.0
└─────────┬─────────┘
          │
          ▼
    Predict AQI_Tomorrow  →  Map to category  →  Health Advice
```

### Feature Vector (14 features, in order)

```python
["PM2.5", "PM10", "NO", "NO2", "NOx", "NH3",
 "CO", "SO2", "O3", "Benzene", "Toluene", "Xylene",
 "Month", "DayOfWeek"]
```

> ⚠️ **Order matters.** The scaler was fit on features in exactly this sequence.
> Changing the order will produce incorrect predictions.

### Inference Pipeline (Live & Manual)

```
Sensor readings (WAQI API / form input)
        │
        ├── Fill missing pollutants with city-level defaults
        ├── Add temporal features: Month, DayOfWeek
        ▼
Build 14-element feature vector (in training order)
        │
        ▼
scaler.transform(vector)     ← loaded from scaler.pkl
        │
        ▼
model.predict(scaled)        ← loaded from aqi_model.pkl
        │
        ▼
Clip to ≥0  →  map to category  →  return JSON
```

---

## 📊 Model Performance

Evaluated on **4,965 held-out test samples** (20% of cleaned dataset):

| Metric | Description |
|--------|-------------|
| **MAE** | Mean Absolute Error (avg AQI points off) |
| **RMSE** | Root Mean Squared Error (penalises large errors) |
| **R²** | Proportion of AQI variance explained by model |
| **MAPE** | Mean Absolute Percentage Error |

> Run **Cell 7** of `AQI_Prediction.ipynb` to see exact values on your data.

### Feature Importance (approximate ranking)

1. **PM2.5** — strongest predictor of next-day AQI
2. **PM10** — second most important particulate
3. **CO** — carbon monoxide levels
4. **NO2** — nitrogen dioxide
5. **O3** — ground-level ozone
6. **Month** — seasonal patterns (winter peaks in India)
7. **SO2**, **NOx**, **NO**, **NH3**, **Benzene**, **Toluene**, **Xylene**, **DayOfWeek**

---

## ⚡ Quick Start

### Prerequisites

- Python 3.10 or higher
- pip package manager

### 1. Clone / Download the project

```bash
cd "AQI Prediction"
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv venv
source venv/bin/activate          # macOS / Linux
# OR
venv\Scripts\activate             # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Ensure model artifacts are present

The following files must exist at the project root (they are generated by the Jupyter Notebook):

```
aqi_model.pkl
scaler.pkl
feature_names.pkl
```

If they are missing, run all cells in `AQI_Prediction.ipynb` first:

```bash
jupyter notebook AQI_Prediction.ipynb
# Run All Cells (Kernel → Restart & Run All)
```

### 5. Start the Flask server

```bash
python app.py
```

```
 * Running on http://127.0.0.1:5001
 * [startup] Model loaded. Features: ['PM2.5', 'PM10', ...]
```

### 6. Open in your browser

| Page | URL |
|------|-----|
| Dashboard | http://127.0.0.1:5001/ |
| Manual Prediction | http://127.0.0.1:5001/predict |
| About | http://127.0.0.1:5001/about |

---

## ⚙️ Configuration

All key settings live at the top of `app.py`:

```python
# ── API ─────────────────────────────────────────
WAQI_TOKEN   = "97926bde88d74ac8e9c433dc0381a9ccad65aa73"
WAQI_URL     = "https://api.waqi.info/feed/{city}/?token={token}"
DEFAULT_CITY = "Bangalore"

# ── Imputation defaults (μg/m³) ─────────────────
CITY_DEFAULTS = {
    "PM2.5": 30.0, "PM10": 60.0, "NO": 8.0,
    "NO2": 25.0,   "NOx":  33.0, "NH3": 10.0,
    "CO":   0.9,   "SO2":   8.0, "O3":  35.0,
    "Benzene": 2.0, "Toluene": 6.0, "Xylene": 1.5,
}
```

To use a different WAQI API token, replace `WAQI_TOKEN`.
To change the default city on page load, change `DEFAULT_CITY` to any supported city name.

---

## 🖥️ Pages

### `/` — Live Dashboard

The main monitoring interface. Automatically fetches live data for the selected city on page load and on every city change.

**Sections:**
- **Header** — animated brand dot, navigation, city dropdown
- **Current AQI** — animated SVG ring gauge with category + dominant pollutant
- **Pollutant Breakdown** — 6 cards with animated values and level bars
- **Tomorrow's AQI Forecast** — ML prediction with category badge + recommendations
- **AQI Scale** — reference bar with position markers

---

### `/predict` — Manual Prediction

Enter any combination of pollutant readings to get a next-day AQI prediction without relying on the WAQI API.

**Use cases:**
- Testing with your own sensor data
- Offline / API-unavailable scenarios
- Educational exploration of how pollutants affect AQI
- Data validation and model sanity checks

**Input groups:**

| Group | Fields |
|-------|--------|
| Particulate Matter | PM₂.₅ (0–500 μg/m³), PM₁₀ (0–600 μg/m³) |
| Nitrogen Compounds | NO, NO₂, NOx (0–150 μg/m³), NH₃ (0–100 μg/m³) |
| Other Gases | CO (0–20 mg/m³), SO₂, O₃ (0–100/200 μg/m³), Benzene, Toluene, Xylene |
| Temporal | Month (1–12), Day of Week (Mon–Sun) |

---

### `/about` — Documentation

Full project documentation including: how-it-works pipeline, dataset details, model hyperparameters, AQI reference table, and technology stack.

---

## 📡 API Reference

### `GET /api/aqi?city={city_name}`

Fetches real-time AQI data from WAQI, runs prediction, returns combined JSON.

**Parameters:**

| Param | Type | Required | Default | Example |
|-------|------|----------|---------|---------|
| `city` | string | No | `Bangalore` | `Delhi` |

**Response:**

```json
{
  "success": true,
  "city": "Bangalore",
  "current": {
    "aqi": 85,
    "category": "Satisfactory",
    "color": "#84CC16",
    "health_advice": "Air quality is acceptable...",
    "dominant_pollutant": "pm25",
    "pollutants": {
      "pm25": 45.2,
      "pm10": 78.5,
      "co": 0.8,
      "so2": 5.2,
      "no2": 22.1,
      "o3": 35.0
    },
    "timestamp": "2026-03-15 21:00:00"
  },
  "prediction": {
    "aqi": 92.4,
    "category": "Satisfactory",
    "color": "#84CC16",
    "health_advice": "Air quality is acceptable...",
    "recommendations": [
      "Sensitive groups should limit prolonged outdoor exertion",
      "Keep windows closed during peak traffic hours",
      "Consider using an air purifier indoors"
    ]
  }
}
```

**Error response:**

```json
{
  "success": false,
  "error": "City not found or API error"
}
```

---

### `POST /api/predict`

Runs the ML model on manually provided pollutant values.

**Request body (JSON):**

```json
{
  "PM2.5":   85.4,
  "PM10":   142.7,
  "NO":       8.3,
  "NO2":     32.1,
  "NOx":     40.6,
  "NH3":     15.2,
  "CO":       1.1,
  "SO2":     12.5,
  "O3":      38.9,
  "Benzene":  2.4,
  "Toluene":  8.7,
  "Xylene":   1.9,
  "Month":   11,
  "DayOfWeek": 2
}
```

> All fields are optional. Missing fields fall back to `CITY_DEFAULTS`.

**Response:**

```json
{
  "success": true,
  "predicted_aqi": 187.3,
  "category": "Moderate",
  "color": "#F59E0B",
  "health_advice": "May cause breathing discomfort to people with lung disease...",
  "recommendations": [
    "People with respiratory conditions should avoid strenuous outdoor activity",
    "Wear a mask if spending extended time outdoors",
    "Keep indoor air clean with purifiers and ventilation filters"
  ],
  "inputs": {
    "PM2.5": 85.4,
    "PM10": 142.7,
    ...
  }
}
```

---

### `GET /api/cities`

Returns the list of supported Indian cities.

**Response:**

```json
{
  "cities": [
    "Bangalore", "Delhi", "Mumbai", "Chennai", "Kolkata",
    "Hyderabad", "Pune", "Ahmedabad", "Jaipur", "Lucknow",
    "Surat", "Kanpur", "Nagpur", "Visakhapatnam", "Bhopal",
    "Patna", "Vadodara", "Ludhiana", "Agra", "Nashik"
  ]
}
```

---

## 🌈 AQI Reference

| Category | AQI Range | Color | Health Impact |
|----------|-----------|-------|---------------|
| **Good** | 0 – 50 | 🟢 `#22C55E` | Minimal or no impact |
| **Satisfactory** | 51 – 100 | 🟡 `#84CC16` | Minor breathing discomfort to sensitive people |
| **Moderate** | 101 – 200 | 🟠 `#F59E0B` | Discomfort to people with lung / heart disease |
| **Poor** | 201 – 300 | 🔶 `#F97316` | Respiratory discomfort on prolonged exposure |
| **Very Poor** | 301 – 400 | 🔴 `#EF4444` | Respiratory illness on prolonged exposure |
| **Severe** | 401 – 500 | 🟤 `#991B1B` | Serious health effects for everyone |
| **Hazardous** | 500+ | 🟣 `#581C87` | Health emergency — all populations affected |

---

## 📓 Notebook Walkthrough

`AQI_Prediction.ipynb` contains 10 cells that form the complete ML pipeline:

| Cell | Title | What It Does |
|------|-------|-------------|
| **1** | Imports & Setup | Loads all libraries, sets global matplotlib style (teal/amber/slate palette) |
| **2** | Data Loading & Exploration | Loads `city_day.csv`, prints shape/info/describe, shows missing value table |
| **3** | Data Cleaning | Drops null AQI rows → city-median imputation → date parsing → creates `AQI_Tomorrow` target |
| **4** | Exploratory Data Analysis | Generates 5-panel EDA figure → saves `eda_plots.png` |
| **5** | Feature Engineering & Split | Defines 14 features, 80/20 split, fits StandardScaler → saves `scaler.pkl` + `feature_names.pkl` |
| **6** | Model Training | Trains XGBRegressor (500 trees) with evaluation set, prints training time |
| **7** | Evaluation & Visualisations | Prints MAE/RMSE/R²/MAPE, generates 4-panel evaluation figure → saves `model_evaluation.png` |
| **8** | AQI Category Function | Defines `get_aqi_category(aqi_value)` → returns category, color, health advice |
| **9** | Save Model & Artifacts | Saves `aqi_model.pkl`, prints file sizes for all 3 artifacts |
| **10** | Test Prediction Pipeline | Loads artifacts, builds sample WAQI-style input, runs end-to-end inference, shows visual badge |

### Running the Notebook

```bash
# Install Jupyter if needed
pip install jupyter

# Launch
jupyter notebook AQI_Prediction.ipynb

# Run all cells in order
# Kernel → Restart & Run All
```

> The notebook must be run from the project root so that relative paths
> (`dataset/city_day.csv`, `aqi_model.pkl`, etc.) resolve correctly.

---

## 🔧 Troubleshooting

### `FileNotFoundError: aqi_model.pkl`
The model artifacts were not found. Run all cells in `AQI_Prediction.ipynb` first to generate them.

### `WAQI fetch failed: HTTPSConnectionPool...`
No internet connection or the WAQI API is temporarily down. The app falls back gracefully — predicted AQI is estimated as 105% of the PM2.5-derived value.

### `City not found or API error`
The city name was not recognised by the WAQI API. Check the spelling or try a different city. Cities with WAQI coverage include all 20 in the dropdown.

### Slider and number input out of sync
This is a JavaScript issue — try a hard browser refresh (`Cmd/Ctrl + Shift + R`) to clear the JS cache.

### Port 5001 already in use
```bash
# Find the process using port 5001
lsof -i :5001
# Kill it, then restart
kill -9 <PID>
python app.py
```

### `ModuleNotFoundError`
Make sure you've activated your virtual environment before running `pip install`:
```bash
source venv/bin/activate
pip install -r requirements.txt
```

---

## 📌 Key Design Decisions

| Decision | Rationale |
|----------|-----------|
| **`AQI_Tomorrow = shift(-1)` within city groups** | Prevents data leakage across cities — ensures the last row of City A is not the "tomorrow" of City B |
| **Shuffle in train/test split** | The WAQI dataset does not have strong temporal autocorrelation at daily granularity; shuffling gives a more representative test set |
| **StandardScaler over MinMaxScaler** | XGBoost is not sensitive to scale, but StandardScaler handles outliers better than MinMaxScaler for this dataset |
| **City-level median imputation** | City-specific medians preserve local pollution patterns; falling back to global median only when a city has 100% NaN for a pollutant |
| **Graceful degradation without model** | If `.pkl` files are missing, the API returns `AQI × 1.05` as the prediction rather than crashing |
| **SVG gauge vs Canvas** | SVG `stroke-dashoffset` animation is GPU-friendly and requires no external libraries |

---

## 📄 License

This project is released under the **MIT License**.
Dataset courtesy of the **Central Pollution Control Board (CPCB)** via [Kaggle](https://www.kaggle.com/datasets/rohanrao/air-quality-data-in-india).
Real-time data powered by the **[World Air Quality Index (WAQI)](https://waqi.info)** project.

---

<div align="center">

**🌐 AeroSense** — Built with Flask · XGBoost · Vanilla JS

*Predictions are estimates based on historical data.
Always follow official CPCB and local government advisories.*

</div>
