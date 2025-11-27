FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app
RUN apt update \
    && apt install gcc libpq-dev -y \
    && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install -r requirements.txt


COPY . .
COPY startup.sh /app/startup.sh 
RUN chmod +x /app/startup.sh
ENTRYPOINT ["/bin/sh",  "/app/startup.sh" ]

CMD ["gunicorn", "ecommerce_app.wsgi:application", "--bind", "0.0.0.0:8000"]
