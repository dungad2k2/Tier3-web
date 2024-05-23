from flask import Flask
from config import Config
from db.models import db
from api.routes import api
from web import web

app = Flask(__name__)
app.config.from_object(Config)
app.config['TEMPLATES_AUTO_RELOAD'] = True
db.init_app(app)

app.register_blueprint(api, url_prefix='/api')
app.register_blueprint(web)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)
