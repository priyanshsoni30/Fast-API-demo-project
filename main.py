from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from models import Product
from database import session, engine
import database_models
from sqlalchemy.orm import Session

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["http://localhost:3000"],
    allow_methods = ["*"]
)

database_models.Base.metadata.create_all(bind=engine)

@app.get("/")
def greet():
    return "Hello world"

products = [
    Product(id=1, name="Phone", description="Apple", price=100, quantity=5),
    Product(id=2, name="Charger", description="Samsung", price=10, quantity=50),
    Product(id=5, name="Goggles", description="Tommy Hillfiger", price=20, quantity=100),
    Product(id=7, name="Laptop", description="Macbook", price=150, quantity=4)
]

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()

def init_db():
    db = session()
    
    count = db.query(database_models.Product).count
    
    if count == 0:
        for product in products:
            db.add(database_models.Product(**product.model_dump()))
        db.commit()
    
init_db()

@app.get("/products")
def get_all_products(db: Session = Depends(get_db)):
    
    db_products = db.query(database_models.Product).all()
    return db_products

@app.get("/products/{id}")
def get_product_by_id(id:int, db: Session = Depends(get_db)):
    
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if db_product:
        return db_product
    return "product not found"

@app.post("/products")
def add_product(product: Product, db: Session = Depends(get_db)):
    db.add(database_models.Product(**product.model_dump()))
    db.commit()
    return product

@app.put("/products/{id}")
def update_product(id:int, product: Product, db: Session = Depends(get_db)):

    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if db_product:
        db_product.name = product.name
        db_product.description = product.description
        db_product.price = product.price
        db_product.quantity = product.quantity
        db.commit()
        return "Product added Successfully..."
    
    else:
        return "No Product found!!!"

@app.delete("/products/{id}")
def delete_product(id:int, db: Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    
    if db_product:
        db.delete(db_product)
        db.commit()
        return "Product deleted Successfully..."
    else:
        return "No Product found!!!"