# MotoSense AI
**AI-Powered Predictive Motorcycle Maintenance — educational prototype**

MotoSense AI is a Flask web application for recording motorcycle service/condition data, estimating maintenance risk using transparent demo rules, viewing a dashboard, and exporting records to CSV.

> **Important limitation:** This project is a portfolio prototype. It is not an approved Royal Enfield system, does not use Royal Enfield internal data, and is not a validated mechanical diagnostic tool. Risk estimates are based on illustrative thresholds. The optional ML script uses synthetic labels generated from those same rules, so its metrics do not demonstrate real-world predictive accuracy.

## Features
- Dashboard summary with Low / Medium / High demo risk flags
- Add motorcycle records: model, odometer, days since service, temperature, vibration, notes
- SQLite database (works locally without MySQL server setup)
- Explainable reasons for risk flags
- CSV export
- Optional synthetic dataset + scikit-learn Random Forest training demonstration
- Responsive interface

## Requirements
- Python 3.10 or newer
- pip

## Run on Windows
1. Extract the ZIP.
2. Open the extracted `MotoSense_AI` folder in VS Code.
3. Open Terminal in that folder.
4. Create a virtual environment:
   ```powershell
   py -m venv .venv
   .venv\Scripts\activate
   ```
5. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```
6. Start the app:
   ```powershell
   python app.py
   ```
7. Open `http://127.0.0.1:5000` in your browser.

The database is created automatically at `data/motosense.db` after the app starts.

## Optional ML demonstration
Run:
```powershell
python train_demo_model.py
```
This creates `data/synthetic_motorcycle_data.csv`, prints evaluation metrics, and saves `data/motosense_demo_model.joblib`. The web app currently uses the transparent rule estimator in `predictor.py`; the saved model is an optional learning exercise and is not wired into production predictions.

## Suggested next improvements
1. Replace synthetic/demo rules with a reputable, documented real dataset if available.
2. Define labels based on verified service/failure outcomes, not arbitrary thresholds.
3. Evaluate on a separate test set and report class-wise precision, recall, F1, and confusion matrix.
4. Add authentication and role-based access before deploying.
5. Add automated tests and deployment configuration.
6. Consult qualified mechanics before using thresholds for safety-related decisions.

## Project structure
```text
MotoSense_AI/
├── app.py
├── predictor.py
├── train_demo_model.py
├── requirements.txt
├── README.md
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── add.html
│   └── about.html
├── static/
│   └── style.css
└── data/
    └── .gitkeep
```

## Resume bullet (use after implementation)
**MotoSense AI — Predictive Motorcycle Maintenance Prototype** | Python, Flask, SQLite, scikit-learn
- Built a web application to record motorcycle condition and service history, surface explainable demo maintenance-risk flags, and export records for analysis.
- Created an optional scikit-learn workflow to demonstrate model training and evaluation on synthetic data, documenting the limitations of simulated labels.
