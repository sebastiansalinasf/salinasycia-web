#!/bin/bash
# Reconstruye el sitio (HTML + CSS). Luego commit y push.
set -e
cd "$(dirname "$0")"
[ -d node_modules ] || npm install --silent
python3 build.py
npx tailwindcss -c tailwind.config.js -i in.css -o ../site/assets/styles.css --minify
echo "Sitio reconstruido en site/"
