# data/tasks.py
from celery.schedules import crontab
from flask import g
from sqlalchemy.sql import and_
from sqlalchemy.dialects import postgresql


from app import celery
from app.util.tasks import query_to_frame, get_pk
from .models import CallTable, EventTable


_mmap = {
    'c_call': CallTable,
    'c_event': EventTable
}


def add_scheduled_tasks(app):
    # app.config['CELERYBEAT_SCHEDULE']['test'] = {
    #     'task': 'app.data.tasks.load_data',
    #     'schedule': crontab(minute='*/15'),
    #     'args': ('date1', 'date2')
    # }
    pass


def get_data_interval(session, table_name, start_time, end_time):
    table = _mmap.get(table_name)
    print(table)
    return session.query(table).filter(
        and_(
            table.start_time >= start_time,
            table.end_time <= end_time,
        )
    )


class SqlAlchemyTask(celery.Task):
    """An abstract Celery Task that ensures that the connection the the
    database is closed on task completion"""
    abstract = True

    def __call__(self, *args, **kwargs):
        # try:
        #     return super().__call__(*args, **kwargs)
        # except DatabaseError:
        #     loc_data_session.rollback()
        # finally:
        #     loc_data_session.commit()
        pass

    def after_return(self, status, retval, task_id, args, kwargs, einfo):
        # loc_data_session.remove()
        # ext_data_session.remove()
        # print(task_id, ' closed sessions: ', loc_data_session, ext_data_session)
        pass


@celery.task(base=SqlAlchemyTask, max_retries=10, default_retry_delay=60)
def load_data(start_time=None, end_time=None, event_id=None):
    # success = True
    # results = CallTable.query.filter(
    #     and_(
    #         CallTable.start_time >= start_time,
    #         CallTable.end_time <= end_time,
    #     )
    # )
    # print(results)
    # print(str(results.statement.compile(dialect=postgresql.dialect())))
    #
    # for r in results.all():
    #     exists = LocalCallTable.query.get_or(r.call_id) is not None
    #     if exists:
    #         print('record already exists')
    #     else:
    #         print('adding ', r.__dict__)
    #         LocalCallTable(**r.__dict__).save()
    #
    # return success
    pass


@celery.task(base=SqlAlchemyTask, max_retries=10, default_retry_delay=60)
def get_data(start_time=None, end_time=None, event_id=None):
    return CallTable.query.filter(
        and_(
            CallTable.start_time >= start_time,
            CallTable.end_time <= end_time,
        )
    )


def load_test(table_name, start_time, end_time):
    table = _mmap.get(table_name)
    print('load_test ', table)
    if table is not None:
        results = get_data_interval(g.ext_session, table_name, start_time, end_time)
        for r in results.all():
            record = g.local_session.query(table).get(r.call_id)
            if record is None:
                new_record = table(**r.__dict__)
                g.local_session.add(new_record)
                # print('added record', new_record)
                # print('added to ', g.local_session)
            else:
                print('record already exists')

    return True


def data_task(task_name, start_time=None, end_time=None, id=None):
    if start_time and end_time:
        if task_name == 'get':
            query = get_data_interval(g.local_session, 'c_call', start_time, end_time)
            result = query_to_frame(query)
            status = 200
            tb = 'Success'
        elif task_name == 'load_test':
            result = load_test('c_call', start_time, end_time)
            status = 204 if result else 302
            tb = 'Success'
        else:
            result = 'Nothing'
            status = 200
            tb = 'Success'
    else:
        result = 'Nothing'
        status = 200
        tb = 'Success'
    # if task_name == 'load_test':
    #     result = load_test(start_time, end_time)
    #     status = 'Test'
    #     tb = 'Okay'
    # elif task_name == 'get_test':
    #     result = get_test(start_time, end_time)
    #     status = 'Test'
    #     tb = 'Okay'
    # else:
    #     if task == 'load':
    #         async_result = load_data.delay(start_time, end_time)
    #     else:
    #         async_result = get_data.delay(start_time, end_time)
    #     try:
    #         result = async_result.get(timeout=5, propagate=False)
    #     except TimeoutError:
    #         result = None
    #     status = async_result.status
    #     tb = async_result.traceback

    return result, status, tb