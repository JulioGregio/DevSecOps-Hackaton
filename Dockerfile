FROM python:3.11.7

WORKDIR /app

COPY . .

RUN python3 -m venv ./venv

RUN . venv/bin/activate && \
    pip install --upgrade pip && \
    pip install -r requirements.txt && \
    pip install bandit

RUN apt-get update && apt-get install -y curl && \
    curl -sfL https://github.com/aquasecurity/trivy/releases/latest/download/trivy_0.18.3_Linux-64bit.tar.gz | tar -xz -C /usr/local/bin trivy

CMD ["flask", "--app", "app", "run", "--host=0.0.0.0"]
