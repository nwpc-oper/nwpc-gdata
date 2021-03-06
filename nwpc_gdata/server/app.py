from pathlib import Path
from datetime import datetime, time, timedelta, date

from flask import Flask
from flask.json import JSONEncoder

from .config import Config


class ServerJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime("%Y-%m-%dT%H:%M:%S")
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        elif isinstance(obj, time):
            return obj.strftime('%H:%M:%S')
        elif isinstance(obj, timedelta):
            return {'day': obj.days, 'seconds': obj.seconds}
        return JSONEncoder.default(self, obj)


def create_app(config_file_path=None):

    static_folder = str(Path(Path(__file__).parent, "static"))
    template_folder = str(Path(Path(__file__).parent, "templates"))
    app = Flask(__name__,
                static_folder=static_folder,
                template_folder=template_folder)

    app.config.from_object(Config.load_config(config_file_path))
    app.config['server_config'] = app.config['SERVER_CONFIG']
    app.json_encoder = ServerJSONEncoder

    with app.app_context():
        from .main import main_app
        app.register_blueprint(main_app)

        from .api import api_app
        app.register_blueprint(api_app, url_prefix="/api/v1")

    return app
