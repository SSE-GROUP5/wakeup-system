from flask import Flask
from constants import PORT, HOSTNAME
from blueprints.triggers.triggers import triggers_blueprint
from blueprints.signals.signals import signals_blueprint
from blueprints.target_devices.target_devices import target_devices_blueprint
from blueprints.users.users import users_blueprint
from homeassistant_client import homeassistant_client
from db import db

def create_app(url="sqlite:///wakeup.sqlite"):
    app = Flask(__name__)
    app.config['DEBUG'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = url
    
    app.register_blueprint(triggers_blueprint)
    app.register_blueprint(signals_blueprint)
    app.register_blueprint(target_devices_blueprint)
    app.register_blueprint(users_blueprint)
    @app.route('/health')
    def health_check():
        is_HA_running = homeassistant_client.health_check()
        # return json response
        return { 
          'message': 'Hello, World!', 
          'HA_status': 'ALIVE' if is_HA_running else 'DEAD'
        }
        
    @app.route('/')
    def index():
        return "OK"
    
        
    
    db.init_app(app)
    with app.app_context():
        db.create_all()
    return app



if __name__ == "__main__":
    
    app = create_app()
    app.run(port=PORT, host=HOSTNAME)