#!/bin/bash

set -a
source .env
set +a

echo "Stop old containers and their volumes..."
docker-compose down -v
sleep 5
echo "Starting Postgres and Redis containers..."
docker-compose up -d postgres redis

echo "Starting API..."
docker-compose up -d api

echo "Starting Nginx HTTP Config..."
sed -i 's/^NGINX_CONF=.*/NGINX_CONF=nginx.http.conf/' .env
docker-compose up -d nginx

echo "Waiting for Nginx..."
sleep 5

echo "Run Certbot (renovación no interactiva)..."
docker-compose run --rm certbot renew -v

echo "🛑 Apagando Nginx (modo HTTP)..."
docker-compose stop nginx

echo "🔁 Paso 2: Cambiando a configuración HTTPS..."
sed -i 's/^NGINX_CONF=.*/NGINX_CONF=nginx.https.conf/' .env

echo "🚀 Levantando Nginx con configuración HTTPS..."
docker-compose up -d nginx

echo "✅ Todo listo. Nginx está sirviendo por HTTPS."
