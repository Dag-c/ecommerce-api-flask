#!/bin/bash

echo "🔁 Paso 1: Usando configuración HTTP para obtener certificado..."

# Cambiar el archivo .env para usar nginx.http.conf
sed -i 's/^NGINX_CONF=.*/NGINX_CONF=nginx.http.conf/' .env

# Reiniciar Nginx con configuración HTTP
docker-compose down -v
docker-compose up -d nginx

echo "🌐 Esperando a que Nginx (HTTP) esté listo..."
sleep 5  # Puedes ajustar si nginx tarda más en levantar

echo "🔐 Ejecutando Certbot para obtener certificados..."
docker-compose run --rm certbot

echo "🛑 Apagando Nginx (modo HTTP)..."
docker-compose stop nginx

echo "🔁 Paso 2: Cambiando a configuración HTTPS..."

# Cambiar el archivo .env para usar nginx.https.conf
sed -i 's/^NGINX_CONF=.*/NGINX_CONF=nginx.https.conf/' .env

echo "🚀 Levantando Nginx con configuración HTTPS..."
docker-compose up

echo "✅ Nginx ya sirve con HTTPS."
