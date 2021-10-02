import os

from django.core.asgi import get_asgi_application

os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE', 'api_avito.settings.production'
)

application = get_asgi_application()
