from sqlalchemy.ext.declarative import DeclarativeMeta
from datetime import datetime
from dateutil import parser
from flask import json


CONVERTERS = {
    '__datetime__': parser.parse
}


class AlchemyEncoder(json.JSONEncoder):

    def default(self, o):
        # ORM models
        if isinstance(o.__class__, DeclarativeMeta):
            data = {}
            fields = o.__json__() if hasattr(o, '__json__') else dir(o)
            for field in [f for f in fields if not f.startswith('_') and f not in ['metadata', 'query', 'query_class']]:
                value = o.__getattribute__(field)
                try:
                    json.dumps(value)
                    data[field] = value
                except TypeError:
                    data[field] = None
            return data
        # Datetime
        if isinstance(o, datetime):
            return {"val": o.isoformat(), "_spec_type": "__datetime__"}
        print('encoder', type(o))
        return json.JSONEncoder.default(self, o)


def object_hook(o):
    """Convert json data from its serialized value"""
    _spec_type = o.get('_spec_type')
    if not _spec_type:
        return o
    print('decoder', type(o))
    if _spec_type in CONVERTERS:
        return CONVERTERS[_spec_type](o['val'])
    else:
        raise Exception('Unknown {}'.format(_spec_type))


# Encoder function
def my_dumps(obj):
    return json.dumps(obj, cls=AlchemyEncoder)


# Decoder function
def my_loads(obj):
    return json.loads(obj, object_hook=object_hook)

