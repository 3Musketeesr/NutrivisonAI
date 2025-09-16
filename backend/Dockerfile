FROM python:3.13.7-slim

WORKDIR /app

COPY ../requirements.txt /tmp/requirements.txt

RUN python3.13 -m venv /opt/.venv && \
    /opt/.venv/bin/pip install --upgrade pip && \
    /opt/.venv/bin/pip install -r /tmp/requirements.txt

COPY . /app

CMD ["/opt/.venv/bin/uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
