FROM python:3.9.10-slim

WORKDIR /app

COPY requirements.txt .

RUN pip3 install -r /app/requirements.txt

COPY . .

EXPOSE 8000

ENTRYPOINT ["/app/django.sh"] 