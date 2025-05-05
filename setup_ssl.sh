#!/bin/bash

set -a
source .env
set +a

echo "🔁 Paso 1: Configuración HTTP temporal para obtener certificados..."
export NGINX_CONF=nginx.http.conf
sed -i 's/^NGINX_CONF=.*/NGINX_CONF=nginx.http.conf/' .env

echo "🧹 Apagando servicios antiguos si existen..."
docker-compose down

echo "🐘 Levantando base de datos (postgres) y Redis..."
docker-compose up -d postgres redis

echo "🚀 Levantando API..."
docker-compose up -d api

echo "🌐 Levantando Nginx con configuración HTTP..."
docker-compose up -d nginx

echo "⌛ Esperando 5 segundos para que Nginx esté listo..."
sleep 5

echo "🔐 Ejecutando Certbot (renovación no interactiva)..."
docker-compose run --rm certbot renew -v

echo "🛑 Apagando Nginx (modo HTTP)..."
docker-compose stop nginx

echo "🔁 Paso 2: Cambiando a configuración HTTPS..."
export NGINX_CONF=nginx.https.conf
sed -i 's/^NGINX_CONF=.*/NGINX_CONF=nginx.https.conf/' .env

echo "🚀 Levantando Nginx con configuración HTTPS..."
docker-compose up -d nginx

echo "✅ Todo listo. Nginx está sirviendo por HTTPS."
