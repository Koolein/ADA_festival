FROM python:3.9-slim
WORKDIR /app
COPY requirements_pod.txt ./
RUN pip install --no-cache-dir -r requirements_pod.txt
COPY . .
CMD ["python", "app.py"]