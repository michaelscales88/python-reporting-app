# data/models.py
import datetime

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.hybrid import hybrid_property

from modules.extensions import BaseModel


class EventTableModel(BaseModel):
    __tablename__ = 'c_event'
    __repr_attrs__ = [
        'event_id', 'event_type', 'calling_party', 'receiving_party',
        'is_conference', 'start_time', 'end_time', 'call_id'
    ]

    event_id = Column(Integer, primary_key=True)
    event_type = Column(Integer, nullable=False)
    calling_party = Column(String(100))
    receiving_party = Column(String(100))
    hunt_group = Column(String(100))
    is_conference = Column(String(100))
    start_time = Column(DateTime(timezone=True))
    end_time = Column(DateTime(timezone=True))
    tag = Column(String(100))
    recording_rule = Column(Integer)
    call_id = Column(Integer)

    @hybrid_property
    def length(self):
        delta = self.end_time - self.start_time
        return delta - datetime.timedelta(microseconds=delta.microseconds)

    @classmethod
    def set_empty(cls, model):
        model.data = {}
        return model

    @classmethod
    def worker_find(cls, session, raw_id):
        return session.query(cls).filter(cls.event_id == int(raw_id)).first()
