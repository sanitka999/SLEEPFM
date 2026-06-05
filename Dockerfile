FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements-cpu.txt .
RUN pip install --upgrade pip && pip install -r requirements-cpu.txt

COPY . .

RUN chmod +x run_demo.sh

CMD ["./run_demo.sh", "check"]
