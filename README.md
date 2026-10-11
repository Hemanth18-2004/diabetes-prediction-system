\# Diabetes Prediction System Using Machine Learning



A web-based machine learning application that predicts the likelihood of diabetes based on patient health parameters. Built using Python, Flask, MySQL, and Scikit-learn.



\## Features



\- User registration and login

\- CSV dataset upload and validation

\- Data preprocessing using Pandas

\- Machine learning model training using Logistic Regression

\- Model evaluation using test data

\- Diabetes prediction based on health parameters

\- Estimated prediction probability

\- MySQL database integration



\## Technologies Used



\- Python

\- Flask

\- MySQL

\- Flask-SQLAlchemy

\- Flask-Bcrypt

\- Pandas

\- Scikit-learn

\- Joblib

\- HTML, CSS, and Jinja2



\## Project Structure



```text

ML internship/

├── README.md

├── requirements.txt

├── .gitignore

└── ML internship/

&#x20;   └── ML app/

&#x20;       ├── App.py

&#x20;       ├── models/

&#x20;       ├── static/

&#x20;       ├── templates/

&#x20;       └── uploads/

```



\## Installation



\### 1. Clone the repository



```bash

git clone <YOUR\_GITHUB\_REPOSITORY\_URL>

cd <YOUR\_PROJECT\_FOLDER>

```



\### 2. Create a virtual environment



```bash

python -m venv .venv

```



Activate it on Windows PowerShell:



```powershell

.\\.venv\\Scripts\\Activate.ps1

```



\### 3. Install dependencies



```bash

python -m pip install -r requirements.txt

```



\### 4. Configure MySQL



Make sure MySQL is running and create the database:



```sql

CREATE DATABASE ml\_app;

```



Configure your database connection and Flask secret key using environment variables or another secure configuration method. Do not publish passwords or secret keys in the repository.



\### 5. Run the application



Navigate to the folder containing `App.py`:



```powershell

cd ".\\ML internship\\ML app"

python App.py

```



Open your browser and visit:



http://127.0.0.1:5000



\## Dataset



The dataset should contain the following input features:



\- Pregnancies

\- Glucose

\- BloodPressure

\- SkinThickness

\- Insulin

\- BMI

\- DiabetesPedigreeFunction

\- Age



The target column is `Outcome`, where `0` represents a negative diabetes label and `1` represents a positive diabetes label in the dataset.



Use a compatible CSV dataset with the required column names.



\## Machine Learning Workflow



1\. Load and validate the dataset.

2\. Preprocess the medical attributes.

3\. Split the data into training and testing sets.

4\. Scale features using StandardScaler.

5\. Train a Logistic Regression classifier.

6\. Evaluate the model on test data.

7\. Save the trained model using Joblib.

8\. Generate predictions from user-provided inputs.



\## Future Enhancements



\- Compare multiple machine learning algorithms.

\- Display precision, recall, F1-score, and confusion matrix.

\- Improve the user interface and responsiveness.

\- Store prediction history securely.

\- Deploy the application to a cloud platform.



\## Disclaimer



This project is intended for educational purposes only. Its predictions are not medical diagnoses and should not be used as the sole basis for medical decisions. Consult a qualified healthcare professional for medical advice.



\## Author



\*\*Hemanth18-2004\*\*



GitHub: https://github.com/Hemanth18-2004



