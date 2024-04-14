from nvidia/cuda:12.0.1-cudnn8-runtime-ubuntu20.04

# Install Python
RUN apt-get update && apt-get install -y python3 python3-pip

WORKDIR /app
COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
