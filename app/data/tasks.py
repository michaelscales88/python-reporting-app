from celery.schedules import crontab
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.sql import func, and_
from sqlalchemy.dialects import postgresql

from app import celery
from app.database import data_session


def add_scheduled_tasks(app):
    app.config['CELERYBEAT_SCHEDULE']['test'] = {
        'task': 'app.data.tasks.load_data',
        'schedule': crontab(minute='*/15'),
        'args': ('date1', 'date2')
    }


def data_task(task, start_date, end_date, id=None):
    if task == 'load':
        async_result = load_data.delay(start_date, end_date)
    else:
        async_result = get_data.delay(start_date, end_date)
    try:
        result = async_result.get(timeout=5, propagate=False)
    except TimeoutError:
        result = None
    return result, async_result.status, async_result.traceback


class SqlAlchemyTask(celery.Task):
    """An abstract Celery Task that ensures that the connection the the
    database is closed on task completion"""
    abstract = True

    def after_return(self, status, retval, task_id, args, kwargs, einfo):
        data_session.remove()
        print('closed sessions.', data_session)


@celery.task(base=SqlAlchemyTask, max_retries=10, default_retry_delay=60)
def load_data(start_date, end_date, event_id=None):
    # event_id can be call_id or event_id from models.py
    from .models import CallTable, EventTable
    from datetime import datetime, timedelta
    start_time = end_time = datetime.today()
    start_time -= timedelta(hours=12)
    end_time -= timedelta(hours=2)
    try:
        print(start_time, end_time, event_id)
        results = data_session.query(CallTable).filter(
            and_(
                CallTable.start_time >= start_time,
                CallTable.end_time <= end_time,
            )
        )
        print(results)
        print(str(results.statement.compile(dialect=postgresql.dialect())))
    except NoResultFound as exc:
        print('No Result Found')
        raise load_data.retry(exc=exc)
    # do something with the user
    print('load data in load_data')
    for r in results.all():
        print(r)
    print('loaded data into local db')


@celery.task(base=SqlAlchemyTask, max_retries=10, default_retry_delay=60)
def get_data(start_date=None, end_date=None, event_id=None):
    # event_id can be call_id or event_id from models.py
    from .models import CallTable, EventTable
    from datetime import datetime, timedelta
    start_time = end_time = datetime.today()
    start_time -= timedelta(hours=12)
    end_time -= timedelta(hours=2)
    try:
        print(start_time, end_time, event_id)
        results = data_session.query(CallTable).filter(
            and_(
                CallTable.start_time >= start_time,
                CallTable.end_time <= end_time,
            )
        )
        print(results)
        print(str(results.statement.compile(dialect=postgresql.dialect())))
    except NoResultFound as exc:
        print('No Result Found')
        raise load_data.retry(exc=exc)
    # do something with the user
    print('fetched data in get_data')
    for r in results.all():
        print(r)
