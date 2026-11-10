# syntax=docker/dockerfile:1
FROM golang:1.27.3-alpine AS builder

RUN addgroup -g 1000 -S appgroup && \
  adduser -u 1000 -S appuser -G appgroup && \
  mkdir -p /app/environments && \
  apk --no-cache add ca-certificates

WORKDIR /app

COPY . ./

RUN go mod download && \
  CGO_ENABLED=0 go build -o /app/main . && \
  chown -R appuser:appgroup /app && \
  chmod -R 755 /app

# second stage to obtain a very small image
FROM scratch
# copy the ca-certificate.crt from the build stage
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/

# copy user permissions from builder
COPY --from=builder /etc/passwd /etc/passwd

COPY --from=builder /app /app

USER 1000

EXPOSE 3000

ENTRYPOINT [ "/app/main" ]
