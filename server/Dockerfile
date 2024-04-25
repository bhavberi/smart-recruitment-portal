# cache dependencies
FROM python:3.12 as python_cache
ENV VIRTUAL_ENV=/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
WORKDIR /cache/
COPY requirements.txt .
RUN python -m venv /venv
RUN pip install -r requirements.txt
ENV HUGGINGFACE_HUB_CACHE=/app/.cache/huggingface
RUN mkdir -p $HUGGINGFACE_HUB_CACHE && \
    chmod -R a+rwX $HUGGINGFACE_HUB_CACHE
# build and start
FROM python:3.12-slim as build
EXPOSE 8000
WORKDIR /app/
ENV VIRTUAL_ENV=/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
COPY --from=python_cache /venv /venv
COPY . .
ENV HUGGINGFACE_HUB_CACHE=/app/.cache/huggingface
RUN mkdir -p $HUGGINGFACE_HUB_CACHE && \
    chmod -R a+rwX $HUGGINGFACE_HUB_CACHE
ENTRYPOINT ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
