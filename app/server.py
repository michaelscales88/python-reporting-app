# app/server.py
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from healthcheck import HealthCheck


from .services import make_celery, get_nav, AppJSONEncoder, migration_meta, BaseModel


app = Flask(
    __name__,
    instance_relative_config=True,
    instance_path='/tmp',
    template_folder='../static/templates',
    static_folder='../static'
)

# Set JSON serializer for the application
app.json_encoder = AppJSONEncoder


# Settings
app.config.from_object('app.celery_config.Config')
app.config.from_object('app.default_config.DevelopmentConfig')


# Database manager
db = SQLAlchemy(
    app,
    metadata=migration_meta(),
    model_class=BaseModel
)


def init_db():
    # Create database and tables
    # Must import Models before calling create_all to ensure
    # tables and metadata are created

    from app.client.models import ClientModel
    from app.data.models import EventTableModel, CallTableModel
    from app.report.models import SlaReportModel

    db.create_all()


# Services
mail = Mail(app)
celery = make_celery(app)
Bootstrap(app)
nav = get_nav()
nav.init_app(app)
moment = Moment(app)
health = HealthCheck(app, "/healthcheck")


@celery.task
def send_async_email(msg):
    """Background task to send an email with Flask-Mail."""
    mail.send(msg)
