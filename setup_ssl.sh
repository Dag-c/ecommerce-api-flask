#!/bin/bash

set -a
source .env
set +a

echo "🔁 Paso 1: Usando configuración HTTP para obtener certificado..."
export NGINX_CONF=nginx.http.conf
docker-compose down
docker-compose up -d nginx

echo "🌐 Esperando a que Nginx (HTTP) esté listo..."
sleep 5  # Opcional: espera para estabilidad

echo "🔐 Ejecutando Certbot para obtener certificados..."
docker-compose run --rm certbot

echo "🛑 Apagando Nginx (modo HTTP)..."
docker-compose stop nginx

echo "🔁 Paso 2: Cambiando a configuración HTTPS..."
export NGINX_CONF=nginx.https.conf

# Sustituye en .env la línea de NGINX_CONF
sed -i 's/NGINX_CONF=.*/NGINX_CONF=nginx.https.conf/' .env

echo "🚀 Levantando Nginx con configuración HTTPS..."
docker-compose up -d nginx

echo "✅ Nginx ya sirve con HTTPS."
