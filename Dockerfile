FROM python:3.11.7

WORKDIR /app

COPY . .

RUN python3 -m venv ./venv

RUN . venv/bin/activate

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

RUN pip install bandit

RUN apk --no-cache add curl \
    && curl -sfL https://github.com/aquasecurity/trivy/releases/latest/download/trivy_0.18.3_Linux-64bit.tar.gz | tar -xz -C /usr/local/bin trivy

CMD [ "flask", "--app" , "app", "run", "--host=0.0.0.0"]