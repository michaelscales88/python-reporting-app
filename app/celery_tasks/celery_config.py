# app/config.py
import os

TASKS_MODULE_ROUTES = {

}

"""
Get Broker Information
"""
AMQP_USERNAME = os.getenv('AMQP_USERNAME', 'user')
AMQP_PASSWORD = os.getenv('AMQP_PASSWORD', 'password')
AMQP_HOST = os.getenv('AMQP_HOST', 'localhost')
AMQP_PORT = int(os.getenv('AMQP_PORT', '5672'))
BROKER_API_PORT = int(os.getenv('BROKER_API_PORT', '15672'))
DISCOVER_RABBITMQ = bool(os.getenv("DISCOVER_RABBITMQ", True))

"""
RabbitMQ Broker Management
"""
# RabbitMQ task broker
DEFAULT_BROKER_URL = 'amqp://{user}:{pw}@{host}:{port}'.format(
    user=AMQP_USERNAME,
    pw=AMQP_PASSWORD,
    host=AMQP_HOST,
    port=AMQP_PORT
)

# RabbitMQ management api
broker_api = 'amqp://{user}:{pw}@{host}:{port}/api/'.format(
    user=AMQP_USERNAME,
    pw=AMQP_PASSWORD,
    host=AMQP_HOST,
    port=BROKER_API_PORT
)

# Enable debug logging
logging = os.getenv('FLOWER_LOG_LEVEL', 'INFO')
CELERYD_LOG_FILE = os.getenv('CELERY_LOGFILE', 'instance/celery-logs')

"""
Celery Task Queue Management
"""
DEFAULT_CELERY_BACKEND = 'rpc://{user}:{pw}@{host}:{port}'.format(
    user=AMQP_USERNAME,
    pw=AMQP_PASSWORD,
    host=AMQP_HOST,
    port=AMQP_PORT
)

CELERY_BROKER_URL = os.getenv('BROKER_URL', DEFAULT_BROKER_URL)
CELERY_RESULT_BACKEND = os.getenv('BACKEND_URL', DEFAULT_CELERY_BACKEND)

CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'


"""
Celery Beat Persistent Task Scheduler
"""
CELERYBEAT_SCHEDULE_FILENAME = os.getenv(
    'CELERYBEAT_SCHEDULE_FILENAME', 'instance/celerybeat-schedule'
)
CELERYBEAT_SCHEDULE = {}
BEAT_PERIOD = os.getenv('BEAT_PERIOD', 'minute')
BEAT_RATE = os.getenv('BEAT_RATE', '*/1')
