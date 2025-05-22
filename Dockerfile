FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_APP=app
# CMD ["flask", "run", "--host=127.0.0.1"]
CMD ["flask", "run", "--host=127.0.0.1", "--port=5001"]
