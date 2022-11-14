FROM python:3.10-slim

WORKDIR /app

RUN pip install --upgrade pip==22.3.1

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

#RUN python test.py
