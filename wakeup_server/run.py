from flask import Flask
from constants import PORT, HOSTNAME, DEV_MODE, HOMEASSISTANT_OFFLINE_MODE
from blueprints.triggers.triggers import triggers_blueprint
from blueprints.signals.signals import signals_blueprint
from blueprints.target_devices.target_devices import target_devices_blueprint
from blueprints.users.users import users_blueprint
from blueprints.docs.docs import get_swagger_config
from blueprints.statistics.statistics import statistics_blueprint
from homeassistant_client import homeassistant_client
from db import db
from log_scheduler import LogScheduler
from flask_swagger_ui import get_swaggerui_blueprint
import os

SWAGGER_URL = '/docs'
dir_path = os.path.dirname(os.path.realpath(__file__))


def create_app(url="sqlite:///wakeup.sqlite"):
    app = Flask(__name__, static_url_path='/static')
    app.config['DEBUG'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = url

    app.register_blueprint(triggers_blueprint)
    app.register_blueprint(signals_blueprint)
    app.register_blueprint(target_devices_blueprint)
    app.register_blueprint(users_blueprint)
    config = get_swagger_config()
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        config['API_URL'],
        config=config
    )
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)
    
    app.register_blueprint(statistics_blueprint)
    @app.route('/health')
    def health_check():
        is_HA_running = homeassistant_client.health_check()

        return { 
          'message': 'Hello, World!', 
          'HA_status': 'ALIVE' if is_HA_running else 'HA_OFFLINE_MODE' if HOMEASSISTANT_OFFLINE_MODE else 'DEAD', 
          'DEV_MODE': DEV_MODE
        }
        
    @app.route('/')
    def index():
        return "OK"
    
        
    
    db.init_app(app)
    with app.app_context():
        db.create_all()
        
    logging_scheduler = LogScheduler(app)
    logging_scheduler.start_logging()
    logging_scheduler.start()
    
    return app



if __name__ == "__main__":
    app = create_app()
    print(f"Swagger UI available at http://{HOSTNAME}:{PORT}/docs")
    app.run(port=PORT, host=HOSTNAME)

