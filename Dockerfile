# Use official lightweight Python image
FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y     build-essential     libpoppler-cpp-dev     pkg-config     python3-dev     gcc     && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
