FROM python:3.11

EXPOSE 8002

ENV PYTHONUNBUFFERED=1

WORKDIR /trip_assistant

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .
