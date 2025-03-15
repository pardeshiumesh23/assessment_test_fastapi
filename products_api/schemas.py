from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from enum import Enum

class ProductCategory(str, Enum):
    finished = 'finished'
    semi_finished = 'semi-finished'
    raw = 'raw'

class UnitOfMeasure(str, Enum):
    mtr = 'mtr'
    mm = 'mm'
    ltr = 'ltr'
    ml = 'ml'
    cm = 'cm'
    mg = 'mg'
    gm = 'gm'
    unit = 'unit'
    pack = 'pack'

class ProductBase(BaseModel):
    name: str
    category: ProductCategory
    description: str
    product_image: str
    sku: str
    unit_of_measure: UnitOfMeasure
    lead_time: int

class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    pass

class Product(ProductBase):
    product_id: int
    created_date: datetime
    updated_date: datetime

    class Config:
        from_attributes = True

class ProductList(BaseModel):
    products : list[Product]
    total_pages : int
    current_page : int