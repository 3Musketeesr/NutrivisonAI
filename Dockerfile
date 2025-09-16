FROM python:3.13.7-slim

WORKDIR /app

# Install build dependencies for pip packages
RUN apt-get update && apt-get install -y build-essential gcc libffi-dev && rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt /tmp/requirements.txt

RUN python3.13 -m venv /opt/.venv && \
    /opt/.venv/bin/pip install --upgrade pip && \
    /opt/.venv/bin/pip install -r /tmp/requirements.txt

COPY . /app 

CMD ["/opt/.venv/bin/uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
