FROM python:3.12-slim AS base
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .

# Étape "test" : flake8 + pytest. Si un test échoue, le build s'arrête ici.
FROM base AS test
COPY requirements-dev.txt test_app.py ./
RUN pip install --no-cache-dir -r requirements-dev.txt
RUN flake8 app.py test_app.py --max-line-length=100 && pytest -q

# Image finale (dernière étape = cible par défaut)
FROM base AS final
ARG APP_VERSION=dev
ENV APP_VERSION=${APP_VERSION}
EXPOSE 5000
CMD ["python", "app.py"]
