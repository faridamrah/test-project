FROM python:3.9-slim

WORKDIR /app

COPY python/requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt

COPY python/test_cases.py .

CMD ["python", "test_cases.py"]
