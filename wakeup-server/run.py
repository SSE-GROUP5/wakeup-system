from flask import Flask
from constants import PORT, HOSTNAME
from blueprints.interactive_devices.interactive_devices import interactive_devices_blueprint
from blueprints.signals.signals import signals_blueprint
from blueprints.target_devices.target_devices import target_devices_blueprint
from homeassistant_client import homeassistant_client
from db import db

if __name__ == "__main__":
    app = Flask(__name__)
    app.config['DEBUG'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///wakeup.sqlite"
    
    app.register_blueprint(interactive_devices_blueprint)
    app.register_blueprint(signals_blueprint)
    app.register_blueprint(target_devices_blueprint)
    
    @app.route('/')
    def hello_world():
        is_HA_running = homeassistant_client.health_check()
        # return json response
        return { 
          'message': 'Hello, World!', 
          'HA_status': 'ALIVE' if is_HA_running else 'DEAD'
        }
       
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run(port=PORT, host=HOSTNAME)