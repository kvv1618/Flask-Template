FROM alpine:latest 
RUN apk add --no-cache python3-dev \
    && python3-pip install --upgrade pip