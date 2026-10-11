FROM python:3.12-slim

RUN addgroup --system --gid 1000 appuser && \
    adduser --system --uid 1000 --ingroup appuser appuser

WORKDIR /app

COPY --chown=appuser:appuser requirements.txt .
RUN pip install -r requirements.txt
COPY --chown=appuser:appuser . .

USER appuser

ENV PYTHONPATH=/app/src

CMD ["python", "src/app/main.py"]
