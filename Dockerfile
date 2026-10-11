FROM ghcr.io/astral-sh/uv:python3.12-trixie-slim

# Создаём пользователя
RUN addgroup --system --gid 1000 appuser && \
    adduser --system --uid 1000 --ingroup appuser appuser

WORKDIR /app

# Копируем метаданные зависимостей
COPY --chown=appuser:appuser pyproject.toml uv.lock ./

# Синхронизируем зависимости (пока ещё от root — так безопаснее для прав)
RUN uv sync --frozen --no-install-project --no-dev

# Копируем весь код проекта
COPY --chown=appuser:appuser . .

# ВАЖНО: явно делаем /app принадлежащим appuser (и рекурсивно всё внутри)
RUN chown -R appuser:appuser /app

# Переключаемся на непривилегированного пользователя
USER appuser

# Абсолютный путь к кэшу внутри /app — у appuser теперь точно есть права
ENV UV_CACHE_DIR=/app/.cache/uv
ENV PATH="/app/.venv/bin:$PATH"

CMD ["uv", "run", "dev"]
