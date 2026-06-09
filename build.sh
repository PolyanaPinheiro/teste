#!/usr/bin/env bash
set -o errexit

echo "Instalando dependências..."
pip install -r requirements.txt

echo "Coletando arquivos estáticos..."
python manage.py collectstatic --no-input

echo "Rodando migrações..."
python manage.py migrate --no-input

# Opcional: Se você estiver usando o django-allauth, 
# às vezes é bom garantir que os sites estejam configurados
python manage.py shell -c "from django.contrib.sites.models import Site; Site.objects.get_or_create(id=1, defaults={'domain': 'cliqueseguro.onrender.com', 'name': 'Clique Seguro'})"