FROM python:3.11.7-bookworm

WORKDIR /app

COPY . .

RUN python3 -m venv ./venv && \
    . venv/bin/activate && \
    pip install --upgrade pip && \
    pip install -r requirements.txt

CMD ["flask", "--app", "app", "run", "--host=0.0.0.0"]
