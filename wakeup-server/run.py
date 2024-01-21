from flask import Flask
from constants import MONGODB_URL
from blueprints.interactive_devices.interactive_devices import interactive_devices_blueprint
from blueprints.signals.signals import signals_blueprint
from blueprints.target_devices.target_devices import target_devices_blueprint
from db import init_app

if __name__ == "__main__":
    app = Flask(__name__)
    app.config['DEBUG'] = True
    app.config['MONGO_URI'] = MONGODB_URL
    
    app.register_blueprint(interactive_devices_blueprint)
    app.register_blueprint(signals_blueprint)
    app.register_blueprint(target_devices_blueprint)
       
       
    init_app(app)
    app.run(port=5001)