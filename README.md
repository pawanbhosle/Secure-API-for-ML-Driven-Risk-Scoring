
# Risk Scoring API

This project provides a basic REST API that calculates a risk score based on input metadata. The system uses token-based authentication and can process risk computations asynchronously using Celery and Redis.

## Features

- Accepts metadata like purpose, region, processor, and data sensitivity.
- Calculates a mock risk score (0–100) based on simple rules.
- Protects endpoints using an API key.
- Includes Swagger docs for easy testing.
- Optional Celery support for async task processing.

## Setup Instructions
1. Install required packages:
   ```
   pip install -r requirements.txt
   ```

2. Run the Flask server:
   ```
   python app.py
   ```

3. Access Swagger UI at:
   ```
   http://127.0.0.1:5000/api/v1/
   api endpoint:
   http://127.0.0.1:5000/api/v1/api/v1/risk-score/
   ```

