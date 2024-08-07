from datetime import date, datetime
from decimal import Decimal
from sqlalchemy import Column, String, TIMESTAMP, text
from sqlalchemy.dialects.mysql import INTEGER, TINYINT
from sqlalchemy.ext.declarative import declarative_base

class Base(declarative_base()):
    __abstract__ = True

    def as_dict(self):
        result = {}
        for c in self.__table__.columns:
            value = getattr(self, c.name)
            if not value:
                continue

            if isinstance(value, (date, datetime)):
                result[c.name] = value.isoformat()
            elif isinstance(value, Decimal):
                result[c.name] = str(value)
            else:
                result[c.name] = value
        return result

metadata = Base.metadata


class Client(Base):
    __tablename__ = 'client'

    id = Column(String(36), primary_key=True, comment='UUIDV4')
    name = Column(INTEGER(11), nullable=False, unique=True)
    email = Column(String(100), nullable=False, unique=True)
    phone = Column(String(48), nullable=False)
    address = Column(String(504))
    created_at = Column(TIMESTAMP, nullable=False, server_default=text("current_timestamp()"))
    updated_at = Column(TIMESTAMP, nullable=False, server_default=text("current_timestamp()"))


class User(Base):
    __tablename__ = 'users'

    id = Column(String(36), primary_key=True, comment='UUID')
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    password = Column(String(255), nullable=False, comment='Hashed password')
    admin = Column(TINYINT(1), nullable=False, server_default=text("0"))
    created_at = Column(TIMESTAMP, nullable=False, server_default=text("current_timestamp()"))
    updated_at = Column(TIMESTAMP, nullable=False, server_default=text("current_timestamp()"))
