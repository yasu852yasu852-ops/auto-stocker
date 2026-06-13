from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey, func
from sqlalchemy.orm import declarative_base, relationship
from flask_login import UserMixin
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
import config

Base = declarative_base()
engine = create_engine(config.DB_URL, future=True)
SessionLocal = scoped_session(sessionmaker(bind=engine))

class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    sku = Column(String(64), unique=True, nullable=False)
    name = Column(String(200), nullable=False)

class Shelf(Base):
    __tablename__ = 'shelves'
    id = Column(Integer, primary_key=True)
    slot = Column(Integer, unique=True, nullable=False)
    status = Column(Enum('EMPTY','OCCUPIED', name='shelf_status'), default='EMPTY')
    product_id = Column(Integer, ForeignKey('products.id'), nullable=True)
    stored_at = Column(DateTime, nullable=True)
    product = relationship('Product')

class StockHistory(Base):
    __tablename__ = 'stock_history'
    id = Column(Integer, primary_key=True)
    shelf_id = Column(Integer)
    product_id = Column(Integer)
    action = Column(Enum('IN','OUT', name='action_type'))
    timestamp = Column(DateTime, server_default=func.now())

class QueueJob(Base):
    __tablename__ = 'queue_jobs'
    id = Column(Integer, primary_key=True)
    job_type = Column(Enum('IN','OUT', name='job_type'))
    sku = Column(String(64), nullable=False)
    requested_by = Column(String(64), nullable=True)
    priority = Column(Integer, default=100)
    created_at = Column(DateTime, server_default=func.now())

class User(UserMixin, Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(64), unique=True, nullable=False)
    password_hash = Column(String(256), nullable=False)

def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    return SessionLocal()

if __name__ == '__main__':
    init_db()
    print('DB initialized')
