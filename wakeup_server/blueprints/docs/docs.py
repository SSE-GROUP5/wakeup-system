import os
import json
base_dir = os.path.dirname(os.path.realpath(__file__))
docs_dir = os.path.join(base_dir, '..', '..', 'static')

# Base Swagger configuration
swagger_config = {
    'swagger': '2.0',
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

# Set Swagger configuration

# Define the titles for each JSON file here
titles = {
    f'{docs_dir}/postman_api.json': 'Postman API Documentation',
    f'{docs_dir}/media_player_api.json': 'Media Player API Documentation',
    f'{docs_dir}/signals_api.json': 'Signals API Documentation',
    f'{docs_dir}/target_devices_api.json': 'Target Devices API Documentation',
    f'{docs_dir}/interactive_devices_api.json': 'Interactive Devices API Documentation',
    f'{docs_dir}/switch_api.json': 'Switch API Documentation',
    f'{docs_dir}/homeassistant_client_api.json': 'Home Assistant API Documentation',
    f'{docs_dir}/device_target_map_api.json': 'Interactive Target Association API Documentation'  # New entry for Interactive Target Association API
}

def get_swagger_config():
    """
    Endpoint to serve the combined Swagger documentation
    """
    # Initialize combined spec with the base config
    combined_spec = swagger_config.copy()  # Copy the base swagger config
    combined_spec['definitions'] = {}  # Ensure the definitions key is present
    # Load each JSON file and add it to the combined spec
    for file_path, title in titles.items():
        try:
            with open(file_path) as json_file:
                spec = json.load(json_file)

            # Add tag for the JSON file if not already present
            if not any(tag['name'] == title for tag in combined_spec['tags']):
                combined_spec['tags'].append({'name': title})

            # Update paths with the tag from individual specs
            for path, path_item in spec.get('paths', {}).items():
                for method, method_spec in path_item.items():
                    # Ensure the method spec has a 'tags' key
                    if 'tags' not in method_spec:
                        method_spec['tags'] = [title]
                    combined_spec['paths'].setdefault(path, {})[method] = method_spec

            # Update definitions from individual specs
            combined_spec['definitions'].update(spec.get('definitions', {}))

        except FileNotFoundError as e:
            print(f"Error: {e}")  # Log the error
            continue

    with open(f'{docs_dir}/combined_api.json', 'w') as f:
        json.dump(combined_spec, f, indent=4)
        
    swagger_config['API_URL'] = '/static/combined_api.json'
    return swagger_config
        
    