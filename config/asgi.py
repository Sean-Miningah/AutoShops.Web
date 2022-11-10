"""
ASGI config for config project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os
import sys
from pathlib import Path 


from django.core.asgi import get_asgi_application

ROOT_DIR = Path(__file__).resolve(strict=True).parent.parent
sys.path.append(str(ROOT_DIR / "mazugumzo"))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

django_application = get_asgi_application()

# Import websocket application here, so apps from django_application are loaded first
from config import routing  

from channels.routing import ProtocolTypeRouter, URLRouter 


application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": URLRouter(routing.websocket_urlpatterns),
    }
)