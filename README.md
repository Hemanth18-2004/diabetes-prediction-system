# Diabetes Prediction System Using Machine Learning

A full-stack, production-style web machine learning application that predicts the likelihood of diabetes based on patient diagnostic parameters. Built with Python, Flask, MySQL, and Scikit-learn.

---

## Features

- **User Authentication:** Secure registration and login using salted Blowfish password hashes (`Flask-Bcrypt`).
- **Interactive Dashboard:** Step-by-step navigation between dataset management, model training, and predictions.
- **CSV Dataset Ingestion:** Upload and preview clinical datasets with schema validation and sanitization.
- **Automated ML Pipeline:** Feature scaling with `StandardScaler` and classification via `LogisticRegression`.
- **Model Evaluation:** Holdout evaluation on 20% test data with accuracy reporting.
- **Real-Time Clinical Prediction:** Interactive patient parameter input form with calibrated probability percentage output.
- **One-Click Demos:** Pre-populated healthy vs. high-risk test simulations for fast demonstration.
- **Relational Persistence:** Backed by MySQL with automatic table migrations via SQLAlchemy.

---

## Technologies Used

- **Language:** Python
- **Backend:** Flask, Flask-SQLAlchemy, Flask-Bcrypt, PyMySQL
- **Machine Learning:** Scikit-learn, Pandas, NumPy, Joblib
- **Frontend:** HTML5, CSS3, Jinja2, Bootstrap 5
- **Database:** MySQL 8.0

---

## Project Structure

```text
ML internship/
├── README.md
├── requirements.txt
├── run.bat
├── .gitignore
└── ML internship/
    └── ML app/
        ├── App.py
        ├── models/
        │   └── diabetes_model.joblib
        ├── static/
        │   ├── css/
        │   │   └── style.css
        │   └── images/
        │       └── bg.jpg
        ├── templates/
        │   ├── base.html
        │   ├── dashboard.html
        │   ├── index.html
        │   ├── login.html
        │   ├── predict.html
        │   ├── register.html
        │   └── upload.html
        └── uploads/
            └── diabetes.csv
```

---

## Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/Hemanth18-2004/diabetes-prediction-system.git
cd diabetes-prediction-system
```

### 2. Create and activate a virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Configure MySQL

Ensure MySQL is running and create the database:

```sql
CREATE DATABASE ml_app;
```

*(By default, the application connects to `mysql+pymysql://root:root@localhost:3306/ml_app`. You can customize this by setting the `DATABASE_URL` environment variable.)*

---

## Running the Application

### Option A: One-Click Launcher (Windows)
Double-click `run.bat` in the project root.

### Option B: Terminal Command
```powershell
cd ".\ML internship\ML app"
python App.py
```

Then open your browser at:
**http://127.0.0.1:5000**

---

## Dataset Attributes

The model is trained on the Pima Indians Diabetes Dataset with the following 8 clinical features:

1. **Pregnancies:** Number of times pregnant
2. **Glucose:** Plasma glucose concentration at 2 hours in an oral glucose tolerance test
3. **BloodPressure:** Diastolic blood pressure (mm Hg)
4. **SkinThickness:** Triceps skin fold thickness (mm)
5. **Insulin:** 2-Hour serum insulin (mu U/ml)
6. **BMI:** Body Mass Index (weight in kg / (height in m)²)
7. **DiabetesPedigreeFunction:** Diabetes genetic pedigree score
8. **Age:** Age in years

**Target:** `Outcome` (`0` = Non-diabetic, `1` = Diabetic).

---

## Machine Learning Workflow

1. **Data Ingestion:** Load and validate uploaded clinical dataset.
2. **Data Cleaning:** Convert non-numeric values, strip infinite/null rows.
3. **Stratified Split:** Split into 80% train and 20% test partitions preserving class ratio.
4. **Feature Normalization:** Standardize features using `StandardScaler` to prevent feature dominance.
5. **Model Training:** Train `LogisticRegression` within a Scikit-Learn `Pipeline` to eliminate data leakage.
6. **Model Serialization:** Save the trained pipeline using `Joblib`.
7. **Real-time Inference:** Generate predictions and risk probabilities for live clinical inputs.

---

## Disclaimer

This application is developed for educational and portfolio demonstration purposes. Its outputs are not medical diagnoses. Consult a certified healthcare professional for medical advice.

---

## Author

**Hemanth DC**  
GitHub: [https://github.com/Hemanth18-2004](https://github.com/Hemanth18-2004)
