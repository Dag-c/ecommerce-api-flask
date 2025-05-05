#!/bin/bash

# Cargar variables del archivo .env
set -a
source .env
set +a

# Paso 1: Crear volúmenes de certificados para Certbot
echo "🔧 Creando volúmenes necesarios para Certbot..."
docker volume create certbot-etc
docker volume create certbot-var

# Paso 2: Crear carpeta temporal para validación (webroot)
mkdir -p ./certbot/www

# Paso 3: Usar configuración temporal HTTP
echo "🌐 Usando configuración temporal (HTTP)..."
export NGINX_CONF=nginx.http.conf

# Paso 4: Levantar nginx con configuración temporal + certbot
docker-compose up -d nginx certbot

# Paso 5: Esperar a que nginx esté listo
echo "⏳ Esperando a que Nginx esté listo..."
counter=1
until docker-compose logs nginx 2>&1 | grep -m 1 "start worker processes" || [ $counter -ge 10 ]; do
  echo "⏳ Esperando a que Nginx esté listo... ($counter)"
  sleep 1
  counter=$((counter+1))
done

if [ $counter -ge 10 ]; then
  echo "❌ Nginx no se inició correctamente. Verifica los logs de Nginx."
  exit 1
fi

# Paso 6: Solicitar certificado SSL con certbot
echo "🔐 Solicitando certificado SSL..."
docker-compose run --rm certbot

# Pausa corta para asegurarse de que los archivos estén disponibles
echo "⌛ Esperando 5 segundos para asegurar que los archivos SSL estén disponibles..."
sleep 5

# Paso 7: Detener nginx temporal (modo HTTP)
echo "🛑 Deteniendo nginx temporal..."
docker-compose stop nginx

# Paso 8: Cambiar a configuración HTTPS
echo "🔁 Cambiando a configuración HTTPS..."
export NGINX_CONF=nginx.https.conf

# Paso 9: Levantar nginx con certificados ya generados
docker-compose up -d nginx

# Paso 10: Crear cron job para renovar el certificado
CRON_CMD="docker-compose run --rm certbot renew && docker-compose exec nginx nginx -s reload"
CRON_JOB="0 3 * * 1 $CRON_CMD"
(crontab -l 2>/dev/null | grep -Fv "$CRON_CMD" ; echo "$CRON_JOB") | crontab -

# Paso 11: Levantar API, base de datos y Redis
echo "🚀 Levantando todos los servicios restantes..."
docker-compose up -d api redis db

echo "✅ Certificado creado, configuración HTTPS activa y servicios levantados."
