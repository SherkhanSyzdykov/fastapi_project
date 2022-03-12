from sqlalchemy import Column, BigInteger, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship


Base = declarative_base()


class AbstractBaseModel(Base):
    __abstract__ = True

    id = Column(BigInteger, primary_key=True, autoincrement=True)


class Url(AbstractBaseModel):
    __tablename__ = 'url'

    url = Column(String, nullable=False, unique=True)

    requests = relationship('Request', back_populates='url')


class Request(AbstractBaseModel):
    __tablename__ = 'request'

    body = Column(String, nullable=False)

    url_id = Column(BigInteger, ForeignKey(f'{Url.__tablename__}.id'), nullable=False)
    url = relationship('Url', back_populates='requests')
