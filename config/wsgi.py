import os
from django.core.wsgi import get_wsgi_application

from config.settings.app_setting import DSM


os.environ.setdefault("DJANGO_SETTINGS_MODULE", DSM)

application = get_wsgi_application()
