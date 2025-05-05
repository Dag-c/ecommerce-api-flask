#!/bin/bash

# Cargar variables del archivo .env
set -a
source .env
set +a

# Paso 1: Crear volúmenes de certificados para Certbot
echo "Creando volúmenes necesarios para Certbot..."
docker volume create certbot-etc
docker volume create certbot-var

# Paso 2: Crear carpeta temporal para validación (webroot)
mkdir -p ./certbot/www

# Paso 3: Levantar contenedores con nginx y certbot en modo inicial
echo "Levantando servicios con nginx y certbot para obtener el primer certificado..."
docker-compose up -d nginx certbot

# Paso 4: Verificar si Nginx está listo
echo "Esperando a que Nginx esté listo..."
until docker-compose logs nginx 2>&1 | grep -m 1 "ready to handle connections"; do
  echo "Esperando a que Nginx esté listo..."
  sleep 2
done

# Paso 5: Ejecutar la obtención del certificado
echo "Solicitando certificado SSL con certbot..."
docker-compose run --rm certbot

# Paso 6: Recargar nginx para que use el nuevo certificado
echo "Recargando Nginx con los certificados SSL..."
docker-compose exec nginx nginx -s reload

# Paso 7: Crear cron job para renovar el certificado automáticamente cada semana
CRON_CMD="0 3 * * 1 docker-compose run --rm certbot renew && docker-compose exec nginx nginx -s reload"
CRON_JOB="0 3 * * 1 docker-compose run --rm certbot renew && docker-compose exec nginx nginx -s reload"

# Verificar si ya existe en crontab
(crontab -l 2>/dev/null | grep -Fv "$CRON_CMD" ; echo "$CRON_JOB") | crontab -

echo "✅ Certificado creado y renovación automática configurada."
