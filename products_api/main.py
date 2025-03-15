from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Annotated
import models, schemas

app = FastAPI()

def get_db():
    db = models.SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@app.get("/product/list", response_model=schemas.ProductList)
def list_products(db: db_dependency, page: int = Query(1), page_size: int = Query(10)):
    skip = (page - 1) * page_size
    products = db.query(models.Product).offset(skip).limit(page_size).all()
    total_count = db.query(models.Product).count()
    total_pages = (total_count + page_size - 1) // page_size

    return schemas.ProductList(products=products, total_pages = total_pages, current_page = page)

@app.get("/product/{pid}/info", response_model=schemas.Product)
def get_product(pid: int, db: db_dependency):
    product = db.query(models.Product).filter(models.Product.product_id == pid).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.post("/product/add", response_model=schemas.Product)
def add_product(product: schemas.ProductCreate, db: db_dependency):
    db_product = models.Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@app.put("/product/{pid}/update", response_model=schemas.Product)
def update_product(pid: int, product: schemas.ProductUpdate, db: db_dependency):
    db_product = db.query(models.Product).filter(models.Product.product_id == pid).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")

    for key, value in product.model_dump().items():
        setattr(db_product, key, value)

    db.commit()
    db.refresh(db_product)
    return db_product