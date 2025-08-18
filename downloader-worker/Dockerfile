FROM python:3.10-slim
USER root

WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

EXPOSE 5000
EXPOSE 6881

CMD ["python", "app.py"]