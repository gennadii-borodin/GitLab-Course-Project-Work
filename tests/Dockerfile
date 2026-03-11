FROM python:3.11-slim

WORKDIR /app

COPY tests/requirements-test.txt .
RUN pip install --no-cache-dir -r requirements-test.txt

# Установка PostgreSQL клиента, Java и Allure CLI
RUN apt-get update && apt-get install -y libpq-dev gcc wget openjdk-21-jre-headless && rm -rf /var/lib/apt/lists/* \
    && wget -q https://repo.maven.apache.org/maven2/io/qameta/allure/allure-commandline/2.29.0/allure-commandline-2.29.0.tgz -O /tmp/allure.tgz \
    && tar -xzf /tmp/allure.tgz -C /opt/ \
    && ln -s /opt/allure-2.29.0/bin/allure /usr/local/bin/allure \
    && rm /tmp/allure.tgz

COPY . .

CMD ["sh", "-c", "pytest -v --cov=api --cov-report=term-missing --cov-report=html:coverage-report --alluredir=allure-results; allure generate allure-results -o allure-report --clean || true"]