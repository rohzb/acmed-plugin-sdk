FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /opt/plugin

COPY . /opt/src/acmed-plugin-sdk
RUN pip install --no-cache-dir /opt/src/acmed-plugin-sdk[server] \
    && pip install --no-cache-dir /opt/src/acmed-plugin-sdk/examples/minimal-python-plugin

EXPOSE 8081
CMD ["python", "-m", "uvicorn", "--app-dir", "/opt/src/acmed-plugin-sdk/examples/minimal-python-plugin", "plugin_service.main:app", "--host", "0.0.0.0", "--port", "8081"]
