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

echo "Run Certbot (Non-interactive renew)..."
docker-compose run --rm certbot renew -v

echo "Turn off Nginx (mode HTTP)..."
docker-compose stop nginx

echo " Change to setup for HTTPS..."
sed -i 's/^NGINX_CONF=.*/NGINX_CONF=nginx.https.conf/' .env

echo "Run Nginx with setup HTTPS..."
docker-compose up -d nginx

echo "All ready. Nginx is working with HTTPS."
