from sqlalchemy import Column, Boolean, CHAR, DateTime, \
    Integer, Interval, String
from sqlalchemy import text
from sqlalchemy.ext.declarative import declarative_base

ORMBase = declarative_base()

def __ORMBase__repr__(self):
    return "<{}({})>".format(self.__class__.__name__,
                             ", ".join("{}={!r}".format(\
                                col.name, getattr(self, col.name)) \
                                for col in self.__table__.columns))
ORMBase.__repr__ = __ORMBase__repr__

class Trashmail(ORMBase):
    __tablename__ = 'trashmail'

    fake_recipient = Column(CHAR(4), primary_key=True)
    recipient = Column(String(200), nullable=False)
    creation_date = Column(DateTime(timezone=False),
                           server_default=text('now()'))
    period = Column(Interval, nullable=False)
    active = Column(Boolean, default=True, server_default=text('true'))
