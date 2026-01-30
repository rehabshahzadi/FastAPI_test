# FastAPI + Streamlit Prediction App

This project uses **FastAPI** as a backend API for predictions and **Streamlit** as a frontend user interface.

---

## Requirements
- Python 3.9+
- pip


## Setup

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```


---

## Prepare Prediction model
run the code to save the model 

fastapi-demo-api-main/fastapi_ml_model.ipynb

---

## Run FastAPI (Backend)

Open **Terminal 1**:

```bash
uvicorn app:app --reload --port 8000
```

Check API docs:
- http://127.0.0.1:8000/docs

---

## Run Streamlit (Frontend)

Open **Terminal 2**:

```bash
streamlit run frontend.py
```

Streamlit opens at:
- http://localhost:8501

---

## API URL Configuration

Make sure `frontend.py` contains the correct API URL:

```python
API_URL = "http://127.0.0.1:8000/predict"
```

---

## Notes
- FastAPI handles prediction logic and ML model
- Streamlit only sends input and displays results
- Restart FastAPI after backend code changes


## Typical Workflow

- Activate virtual environment
- Run FastAPI backend
- Run Streamlit frontend
- Open Streamlit in browser