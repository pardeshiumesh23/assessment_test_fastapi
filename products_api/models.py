from sqlalchemy import create_engine, Column, Integer, String, Enum, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import enum

Base = declarative_base()

class ProductCategory(enum.Enum):
    finished = 'finished'
    semi_finished = 'semi-finished'
    raw = 'raw'

class UnitOfMeasure(enum.Enum):
    mtr = 'mtr'
    mm = 'mm'
    ltr = 'ltr'
    ml = 'ml'
    cm = 'cm'
    mg = 'mg'
    gm = 'gm'
    unit = 'unit'
    pack = 'pack'

class Product(Base):
    __tablename__ = 'products'

    product_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100))
    category = Column(Enum(ProductCategory))
    description = Column(String(250))
    product_image = Column(String(2048)) # Increased length for URL
    sku = Column(String(100))
    unit_of_measure = Column(Enum(UnitOfMeasure))
    lead_time = Column(Integer)
    created_date = Column(DateTime, default=func.now())
    updated_date = Column(DateTime, default=func.now(), onupdate=func.now())

# Database connection
engine = create_engine('mysql+mysqldb://root:root@localhost/product_db') #replace with your database credentials
Base.metadata.create_all(engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()