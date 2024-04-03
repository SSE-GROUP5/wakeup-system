import os
import json
import sys
base_dir = os.path.dirname(os.path.realpath(__file__))
def is_exe_file():
	# Determine if we are running in a bundled environment and set the base path
	return getattr(sys, 'frozen', False)

docs_dir = "static" if is_exe_file() else  os.path.join(base_dir, '..', '..', 'static')

# Base Swagger configuration
swagger_config = {
    'swagger': '3.0.3',
    'info': {
        'version': '1.0.0',
        'title': 'Matter API Documentation',
        'description': 'API endpoints for multiple services',
    },
    'basePath': '/',
    'schemes': ['http'],
    'consumes': ['application/json'],
    'produces': ['application/json'],
    'paths': {},
    'definitions': {},  # Ensure definitions key is present
    'tags': []
}


def get_swagger_config():
    swagger_config['API_URL'] = '/static/api.yml'
    return swagger_config
        
    