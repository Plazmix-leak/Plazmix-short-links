import os

from dotenv import load_dotenv
from flask_redis import FlaskRedis

load_dotenv()

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from .utilits import RetryingQuery

db = SQLAlchemy(query_class=RetryingQuery)
redis_client = FlaskRedis()

# https://habr.com/ru/post/346344/
migrate = Migrate()
basedir = os.getcwdb().decode("utf-8")
app = Flask(__name__, static_folder=os.path.join(basedir, "static"),
            template_folder=os.path.join(basedir, "templates"))

app.config.from_object(os.getenv('FLASK_ENV') or 'config.Development')

db.init_app(app)
migrate.init_app(app, db)
redis_client.init_app(app)

# from .core.models import UserAuthSession
# from .blueprints import auth_blueprint, api_blueprint, main_blueprint
from .blueprints import api, main
from .core.modules import Link

# app.register_blueprint(auth_blueprint, url_prefix='/auth')
app.register_blueprint(api, url_prefix='/api')
app.register_blueprint(main)


@app.errorhandler(404)
def not_found_error(error):
    return render_template('error.html', error_comment="Страница не найдена"), 404


@app.errorhandler(500)
def not_found_error(error):
    return render_template('error.html', error_comment="Упс, ошибка на стороне сервера, если через некоторое время "
                                                       "она повторится, то сообщите о ней нам"), 500

