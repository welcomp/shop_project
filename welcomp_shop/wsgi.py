import os
import sys
import logging

from django.core.wsgi import get_wsgi_application

logging.basicConfig(level=logging.INFO, stream=sys.stdout, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'welcomp_shop.settings')

application = get_wsgi_application()

# Middleware simple para loggear encabezados de la solicitud
def log_request_headers_middleware(wsgi_app):
    def middleware(environ, start_response):
        logger.info("--- INICIO ENCABEZADOS DE SOLICITUD ---")
        for key, value in environ.items():
            # Los encabezados HTTP se pasan en el diccionario environ con el prefijo 'HTTP_'
            # También nos interesa 'SERVER_PORT' y 'SERVER_NAME'
            if key.startswith('HTTP_') or key in ['SERVER_PORT', 'SERVER_NAME', 'REQUEST_METHOD', 'PATH_INFO', 'SERVER_PROTOCOL', 'wsgi.url_scheme']:
                logger.info(f"  {key}: {value}")
        logger.info("--- FIN ENCABEZADOS DE SOLICITUD ---")
        return wsgi_app(environ, start_response)
    return middleware

# Aplica el middleware a tu aplicación WSGI
application = log_request_headers_middleware(application)
