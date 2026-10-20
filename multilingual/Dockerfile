FROM python:3.13-slim
WORKDIR /app
COPY multilingual/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY multilingual /app/multilingual
ENV PORT=8080
CMD ["uvicorn", "multilingual.communications:app", "--host", "0.0.0.0", "--port", "8080", "--proxy-headers"]
