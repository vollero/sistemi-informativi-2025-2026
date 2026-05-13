FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY labs/palestra_web/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY labs/palestra_web /app/labs/palestra_web

EXPOSE 5000

CMD ["python", "labs/palestra_web/app.py"]
