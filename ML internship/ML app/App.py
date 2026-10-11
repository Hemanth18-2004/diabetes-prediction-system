
import os
import math
from pathlib import Path

import joblib
import pandas as pd

from flask import (
    Flask, render_template, request, redirect,
    url_for, flash, session
)
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from werkzeug.utils import secure_filename

from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score


# ==================================================
# APPLICATION CONFIGURATION
# ==================================================
app = Flask(__name__)

app.secret_key = os.environ.get(
    "FLASK_SECRET_KEY",
    "dev-only-change-this-secret-key"
)

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL",
    "mysql+pymysql://root:root@localhost/ml_app"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)


# ==================================================
# PATHS AND MODEL CONFIGURATION
# ==================================================
BASE_DIR = Path(__file__).resolve().parent
UPLOAD_FOLDER = BASE_DIR / "uploads"
MODEL_DIR = BASE_DIR / "models"
MODEL_PATH = MODEL_DIR / "diabetes_model.joblib"

UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)
MODEL_DIR.mkdir(parents=True, exist_ok=True)

app.config["UPLOAD_FOLDER"] = str(UPLOAD_FOLDER)

ALLOWED_EXTENSIONS = {"csv"}

FEATURES = [
    "Pregnancies",
    "Glucose",
    "BloodPressure",
    "SkinThickness",
    "Insulin",
    "BMI",
    "DiabetesPedigreeFunction",
    "Age",
]

TARGET = "Outcome"


# ==================================================
# DATABASE MODEL
# ==================================================
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(
        db.String(100), unique=True, nullable=False
    )

    email = db.Column(
        db.String(100), unique=True, nullable=False
    )

    password = db.Column(
        db.String(255), nullable=False
    )


# ==================================================
# HOME
# ==================================================
@app.route("/")
def index():
    return render_template("index.html")


# ==================================================
# REGISTER
# ==================================================
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get(
            "username", ""
        ).strip()

        email = request.form.get(
            "email", ""
        ).strip().lower()

        password = request.form.get("password", "")

        if not username or not email or not password:
            flash("Please fill in all fields.", "danger")
            return render_template("register.html")

        try:
            existing_user = User.query.filter(
                (User.username == username)
                | (func.lower(User.email) == email)
            ).first()

            if existing_user:
                flash(
                    "Username or email already exists. "
                    "Please log in or use different details.",
                    "warning"
                )
                return render_template("register.html")

            password_hash = bcrypt.generate_password_hash(
                password
            ).decode("utf-8")

            user = User(
                username=username,
                email=email,
                password=password_hash
            )

            db.session.add(user)
            db.session.commit()

            flash(
                "Registration successful! Please log in.",
                "success"
            )
            return redirect(url_for("login"))

        except IntegrityError:
            db.session.rollback()
            app.logger.exception("Duplicate registration")

            flash(
                "That username or email may already exist.",
                "danger"
            )

        except Exception:
            db.session.rollback()
            app.logger.exception("Registration failed")

            flash(
                "Registration failed. Check the terminal.",
                "danger"
            )

    return render_template("register.html")


# ==================================================
# LOGIN
# ==================================================
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get(
            "email", ""
        ).strip().lower()

        password = request.form.get("password", "")

        if not email or not password:
            flash("Enter your email and password.", "danger")
            return render_template("login.html")

        try:
            user = User.query.filter(
                func.lower(User.email) == email
            ).first()

            if user and bcrypt.check_password_hash(
                user.password, password
            ):
                session.clear()
                session["user_id"] = user.id
                session["username"] = user.username

                flash("Login successful!", "success")
                return redirect(url_for("dashboard"))

            flash(
                "Invalid email or password. Please try again.",
                "danger"
            )

        except Exception:
            app.logger.exception("Login failed")
            flash(
                "Login error. Check the terminal.",
                "danger"
            )

    return render_template("login.html")


# ==================================================
# DASHBOARD
# ==================================================
@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        flash(
            "Please log in to access the dashboard.",
            "warning"
        )
        return redirect(url_for("login"))

    return render_template(
        "dashboard.html",
        username=session.get("username", "")
    )


# ==================================================
# LOGOUT
# ==================================================
@app.route("/logout", methods=["GET", "POST"])
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("login"))


# ==================================================
# CSV UPLOAD
# ==================================================
def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower()
        in ALLOWED_EXTENSIONS
    )


@app.route("/upload", methods=["GET", "POST"])
def upload():
    if "user_id" not in session:
        flash("Please log in first.", "warning")
        return redirect(url_for("login"))

    file_uploaded = False
    columns = []
    data = []

    if request.method == "POST":
        file = request.files.get("file")

        if file is None or not file.filename:
            flash("Please select a CSV file.", "warning")
            return redirect(url_for("upload"))

        if not allowed_file(file.filename):
            flash("Please upload a CSV file.", "danger")
            return redirect(url_for("upload"))

        filename = secure_filename(file.filename)

        if not filename:
            flash("Invalid filename.", "danger")
            return redirect(url_for("upload"))

        file_path = UPLOAD_FOLDER / filename

        try:
            file.save(str(file_path))

            dataset = pd.read_csv(file_path)

            if dataset.empty:
                raise ValueError("The uploaded CSV is empty.")

            file_uploaded = True
            columns = dataset.columns.tolist()
            data = dataset.head(10).values.tolist()

            flash("Dataset uploaded successfully!", "success")

        except Exception:
            app.logger.exception("Dataset upload failed")
            flash(
                "Unable to read the dataset. Check the terminal.",
                "danger"
            )

    return render_template(
        "upload.html",
        file_uploaded=file_uploaded,
        columns=columns,
        data=data
    )


# ==================================================
# LOAD AND VALIDATE DATASET
# ==================================================
def get_training_data():
    uploaded_files = sorted(
        UPLOAD_FOLDER.glob("*.csv"),
        key=lambda path: path.stat().st_mtime,
        reverse=True
    )

    if not uploaded_files:
        raise FileNotFoundError(
            "Upload diabetes.csv before training."
        )

    dataset = pd.read_csv(uploaded_files[0])

    required_columns = FEATURES + [TARGET]
    missing = set(required_columns) - set(dataset.columns)

    if missing:
        raise ValueError(
            f"Missing dataset columns: {sorted(missing)}"
        )

    dataset = dataset[required_columns].copy()

    for column in required_columns:
        dataset[column] = pd.to_numeric(
            dataset[column], errors="coerce"
        )

    dataset = dataset.replace(
        [float("inf"), float("-inf")], float("nan")
    ).dropna()

    if len(dataset) < 10:
        raise ValueError(
            "The dataset must contain at least 10 valid rows."
        )

    if not dataset[TARGET].isin([0, 1]).all():
        raise ValueError(
            "Outcome must contain only 0 and 1."
        )

    if dataset[TARGET].nunique() != 2:
        raise ValueError(
            "The dataset must contain both Outcome classes."
        )

    return dataset


# ==================================================
# TRAIN MODEL
# ==================================================
@app.route("/train", methods=["POST"])
def train():
    if "user_id" not in session:
        flash("Please log in first.", "warning")
        return redirect(url_for("login"))

    try:
        dataset = get_training_data()

        X = dataset[FEATURES]
        y = dataset[TARGET].astype(int)

        if y.value_counts().min() < 2:
            raise ValueError(
                "Not enough examples of each outcome class."
            )

        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            test_size=0.2,
            random_state=42,
            stratify=y
        )

        model = make_pipeline(
            StandardScaler(),
            LogisticRegression(max_iter=1000)
        )

        model.fit(X_train, y_train)

        predictions = model.predict(X_test)
        accuracy = accuracy_score(y_test, predictions)

        joblib.dump(
            {
                "model": model,
                "features": FEATURES
            },
            MODEL_PATH
        )

        flash(
            f"Model trained successfully. "
            f"Holdout accuracy: {accuracy:.1%}.",
            "success"
        )

    except Exception:
        app.logger.exception("Model training failed")
        flash(
            "Model training failed. Check the terminal.",
            "danger"
        )

    return redirect(url_for("upload"))


# ==================================================
# PREDICT
# ==================================================
@app.route("/predict", methods=["GET", "POST"])
def predict():
    if "user_id" not in session:
        flash("Please log in first.", "warning")
        return redirect(url_for("login"))

    if request.method == "GET":
        if not MODEL_PATH.exists():
            flash(
                "Train the model before making predictions.",
                "warning"
            )
            return redirect(url_for("upload"))

        return render_template("predict.html", result=None)

    if not MODEL_PATH.exists():
        flash(
            "Train the model before making predictions.",
            "warning"
        )
        return redirect(url_for("upload"))

    try:
        values = []

        for feature in FEATURES:
            raw_value = request.form.get(feature, "").strip()

            if not raw_value:
                raise ValueError(
                    f"Missing value for {feature}."
                )

            value = float(raw_value)

            if not math.isfinite(value):
                raise ValueError(
                    f"Invalid value for {feature}."
                )

            values.append(value)

        saved_model = joblib.load(MODEL_PATH)

        if saved_model.get("features") != FEATURES:
            raise ValueError(
                "The saved model features do not match."
            )

        model = saved_model["model"]

        input_data = pd.DataFrame(
            [values], columns=FEATURES
        )

        prediction = int(model.predict(input_data)[0])

        probability = float(
            model.predict_proba(input_data)[0][1]
        )

        result = {
            "prediction": prediction,
            "probability": round(probability * 100, 2)
        }

        return render_template(
            "predict.html",
            result=result
        )

    except (ValueError, TypeError):
        flash(
            "Please enter valid numbers for all eight fields.",
            "danger"
        )
        return render_template("predict.html", result=None)

    except Exception:
        app.logger.exception("Prediction failed")
        flash(
            "Prediction failed. Check the terminal.",
            "danger"
        )
        return render_template("predict.html", result=None)


# ==================================================
# START SERVER
# ==================================================
if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(
        debug=False,
        host="127.0.0.1",
        port=5000
    )
