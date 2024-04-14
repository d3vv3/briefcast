from tiangolo/uvicorn-gunicorn-fastapi:python3.11

WORKDIR /app
COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .
