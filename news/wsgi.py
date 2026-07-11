import os
from django.core.wsgi import get_wsgi_application
from a2wsgi import WSGIMiddleware  #  Correct uppercase 'M'
  # <-- Add this import

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'news.settings')

# Change the default variable name to raw_application
raw_application = get_wsgi_application()

# Expose the wrapped version as 'application' for Uvicorn
application = WSGIMiddleware(raw_application)
