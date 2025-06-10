# FastAPI Backend Application

This is a FastAPI-based backend application that provides RESTful API endpoints.

## Setup

1. Create a virtual environment (recommended):
```bash
python3 -m venv venv
source venv/bin/activate  # On Unix/macOS
# or
.\venv\Scripts\activate  # On Windows
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

To run the application:

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the application is running, you can access:
- Interactive API documentation (Swagger UI) at `http://localhost:8000/docs`
- Alternative API documentation (ReDoc) at `http://localhost:8000/redoc` 