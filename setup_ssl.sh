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
until docker-compose logs nginx 2>&1 | grep -m 1 "start worker processes"; do
  sleep 2
done

# Paso 6: Solicitar certificado SSL con certbot
echo "🔐 Solicitando certificado SSL..."
docker-compose run --rm certbot

# Paso 7: Detener nginx
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

# Evitar duplicados en crontab
(crontab -l 2>/dev/null | grep -Fv "$CRON_CMD" ; echo "$CRON_JOB") | crontab -

echo "✅ Certificado creado y renovación automática configurada."
