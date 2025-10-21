from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/shopping-lists", tags=["shopping-lists"])

@router.get("/", response_model=List[schemas.ShoppingList])
def get_shopping_lists(db: Session = Depends(get_db)):
    """Get all shopping lists"""
    return db.query(models.ShoppingList).all()

@router.get("/{list_id}", response_model=schemas.ShoppingList)
def get_shopping_list(list_id: int, db: Session = Depends(get_db)):
    """Get a specific shopping list by ID"""
    shopping_list = db.query(models.ShoppingList).filter(models.ShoppingList.id == list_id).first()
    if not shopping_list:
        raise HTTPException(status_code=404, detail="Shopping list not found")
    return shopping_list

@router.post("/", response_model=schemas.ShoppingList)
def create_shopping_list(shopping_list: schemas.ShoppingListCreate, db: Session = Depends(get_db)):
    """Create a new shopping list"""
    db_list = models.ShoppingList(**shopping_list.model_dump())
    db.add(db_list)
    db.commit()
    db.refresh(db_list)
    return db_list

@router.delete("/{list_id}")
def delete_shopping_list(list_id: int, db: Session = Depends(get_db)):
    """Delete a shopping list"""
    db_list = db.query(models.ShoppingList).filter(models.ShoppingList.id == list_id).first()
    if not db_list:
        raise HTTPException(status_code=404, detail="Shopping list not found")
    
    db.delete(db_list)
    db.commit()
    return {"message": "Shopping list deleted successfully"}

# Shopping Items
@router.post("/{list_id}/items", response_model=schemas.ShoppingItem)
def add_item_to_list(list_id: int, item: schemas.ShoppingItemCreate, db: Session = Depends(get_db)):
    """Add an item to a shopping list"""
    shopping_list = db.query(models.ShoppingList).filter(models.ShoppingList.id == list_id).first()
    if not shopping_list:
        raise HTTPException(status_code=404, detail="Shopping list not found")
    
    db_item = models.ShoppingItem(**item.model_dump(), shopping_list_id=list_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.put("/items/{item_id}", response_model=schemas.ShoppingItem)
def update_shopping_item(item_id: int, is_purchased: bool, db: Session = Depends(get_db)):
    """Update shopping item status"""
    db_item = db.query(models.ShoppingItem).filter(models.ShoppingItem.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Shopping item not found")
    
    db_item.is_purchased = is_purchased
    db.commit()
    db.refresh(db_item)
    return db_item

@router.delete("/items/{item_id}")
def delete_shopping_item(item_id: int, db: Session = Depends(get_db)):
    """Delete a shopping item"""
    db_item = db.query(models.ShoppingItem).filter(models.ShoppingItem.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Shopping item not found")
    
    db.delete(db_item)
    db.commit()
    return {"message": "Shopping item deleted successfully"}
