# Best as of 2026: Use official Python image for simplicity and security
FROM python:3.12-windowsservercore-ltsc2022

WORKDIR C:/app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "app.py"]