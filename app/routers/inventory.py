from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..schemas.inventory import Product, ProductCreate
from ..models.inventory_models import Product as DBProduct
from ..utils.security import get_current_user

router = APIRouter(
    prefix="/products",
    tags=["products"]
)

@router.get("/", response_model=List[Product]) #✅ GET todos
def read_products(
    skip: int = 0, 
    limit: int = 10, 
    db: Session = Depends(get_db)
):
    products = db.query(DBProduct).offset(skip).limit(limit).all()
    return products

@router.get("/{product_id}", response_model=Product)  #✅ GET por id
def read_product(
    product_id: int, 
    db: Session = Depends(get_db)
):
    product = db.query(DBProduct).filter(DBProduct.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.put("/{product_id}", response_model=Product)  #✅ PUT por id    
def update_product(
    product_id: int, 
    product: ProductCreate, 
    db: Session = Depends(get_db), 
    current_user: str = Depends(get_current_user)
):
    db_product = db.query(DBProduct).filter(DBProduct.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    for key, value in product.dict().items():
        setattr(db_product, key, value)
    
    db.commit()
    db.refresh(db_product)
    return db_product

@router.delete("/{product_id}") #✅ DELETE por id
def delete_product(
    product_id: int, 
    db: Session = Depends(get_db), 
    current_user: str = Depends(get_current_user)
):
    db_product = db.query(DBProduct).filter(DBProduct.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    db.delete(db_product)
    db.commit()
    return {"message": "Product deleted successfully"}

@router.post("/", response_model= Product) #✅ POST
def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    db_product = DBProduct(
        name=product.name,
        description=product.description,
        price=product.price,
        stock=product.stock,
        category=product.category
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    
    return db_product