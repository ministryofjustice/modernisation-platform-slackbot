FROM python:3.12-alpine3.21

RUN addgroup -g 1001 -S appgroup && \
  adduser -u 1001 -S appuser -G appgroup

WORKDIR /usr/src/app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
COPY checks_config.json .

EXPOSE 3000

ENV HOST=0.0.0.0

RUN chown -R appuser:appgroup /usr/src/app

USER 1000

CMD ["python", "/usr/src/app/app.py"]
