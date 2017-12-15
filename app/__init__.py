from flask_mail import Mail
from app.util import Flask, make_celery, AlchemyEncoder


app = Flask(
    __name__,
    instance_relative_config=True,
    instance_path='/var/www/tmp/',
    template_folder='templates',
    static_folder='static',
    static_url_path='/static'
)

# Settings
app.config.from_object('app.celeryconfig.Config')
app.config.from_object('app.default_config.DevelopmentConfig')


# Services
mail = Mail(app)


# Set the json encoder
app.json_encoder = AlchemyEncoder


# Init tasks
celery = make_celery(app)
from app.tasks import test


# Import views
from .view import *
