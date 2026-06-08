#!/usr/bin/env bash
# Script de build executado pelo Render antes de iniciar o servidor
 
set -o errexit   # Para o script se qualquer comando falhar
 
pip install -r requirements.txt
 
python manage.py collectstatic --no-input
python manage.py migrate
 