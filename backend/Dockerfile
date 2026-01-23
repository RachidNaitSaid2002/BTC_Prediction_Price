FROM python:3.10-slim

USER root

RUN apt-get update \
    && apt-get install -y openjdk-21-jdk procps \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

ENV JAVA_HOME=/usr/lib/jvm/java-21-openjdk-amd64
ENV PATH=$JAVA_HOME/bin:$PATH

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/app/ .
COPY ml/ ./ml/

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
