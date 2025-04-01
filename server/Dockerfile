FROM python:3.11-alpine

WORKDIR /app

RUN pip install flask
COPY server.py .

EXPOSE 8000
CMD ["python3", "server.py"]