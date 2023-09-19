import os
from django.core.asgi import get_asgi_application

from config.settings.app_setting import DSM


os.environ.setdefault("DJANGO_SETTINGS_MODULE", DSM)

application = get_asgi_application()
