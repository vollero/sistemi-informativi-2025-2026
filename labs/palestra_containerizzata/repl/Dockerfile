FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY labs/palestra_repl/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY labs/palestra_repl /app/labs/palestra_repl

CMD ["python", "labs/palestra_repl/main.py"]
