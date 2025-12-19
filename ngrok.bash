#!/bin/bash
# Script para instalar ngrok en Rocky Linux 8/9 de forma automática
# Testeado en Rocky Linux 9.4 - Diciembre 2025

set -e  # Sale si algo falla

echo "======================================"
echo "   Instalando ngrok en Rocky Linux"
echo "======================================"

# 1. Descargar la versión más reciente de ngrok para Linux AMD64
echo "Descargando ngrok..."
curl -s https://api.github.com/repos/ngrok/ngrok/releases/latest \
  | grep "browser_download_url.*ngrok-linux-amd64.zip" \
  | cut -d : -f 2,3 \
  | tr -d \" \
  | wget -qi -

# Si el comando anterior falla (arquitectura ARM), usa este de respaldo:
if [ ! -f ngrok-linux-amd64.zip ]; then
    echo "No se encontró versión AMD64, intentando versión genérica..."
    wget https://bin.equinox.io/c/bNyj1mQVY4/ngrok-v3-stable-linux-amd64.tgz -O ngrok.tgz
    tar xvzf ngrok.tgz
    mv ngrok /usr/local/bin/
else
    unzip -o ngrok-linux-amd64.zip
    sudo mv ngrok /usr/local/bin/
    rm ngrok-linux-amd64.zip
fi

# 2. Darle permisos de ejecución
sudo chmod +x /usr/local/bin/ngrok

# 3. Verificar instalación
echo "Versión instalada:"
ngrok version

# 4. (Opcional pero recomendado) Crear un enlace simbólico para que funcione sin ./ 
# (ya está en /usr/local/bin, que normalmente está en el PATH)

# 5. Preguntar por el authtoken y configurarlo automáticamente
echo
read -p "Pega aquí tu authtoken de ngrok (regístrate en https://dashboard.ngrok.com/get-started/your-authtoken): " NGROK_TOKEN

if [[ -n "$NGROK_TOKEN" ]]; then
    ngrok config add-authtoken "$NGROK_TOKEN"
    echo "¡Authtoken configurado correctamente!"
else
    echo "No se ingresó token. Puedes hacerlo después con: ngrok config add-authtoken TU_TOKEN"
fi

echo
echo "¡Listo! ngrok está instalado y configurado."
echo "Para abrir un túnel SSH solo ejecuta:"
echo "    ngrok tcp 22"
echo "¡Disfruta!"
