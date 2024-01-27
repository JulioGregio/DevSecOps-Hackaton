FROM python:3.11.7-alpine

WORKDIR /app

COPY . .

RUN python3 -m venv ./venv

RUN . venv/bin/activate && \
    pip install --upgrade pip && \
    pip install -r requirements.txt && \
    pip install bandit

RUN apk --no-cache add curl && \
    curl -sfL https://github.com/aquasecurity/trivy/releases/latest/download/trivy_0.19.2_Linux-64bit.tar.gz | tar -xz -C /usr/local/bin trivy

CMD ["flask", "--app", "app", "run", "--host=0.0.0.0"]
