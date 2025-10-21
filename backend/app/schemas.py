from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import date, datetime

# Ingredient Schemas
class IngredientBase(BaseModel):
    name: str
    category: str
    location: str
    quantity: float
    unit: str
    expiry_date: Optional[date] = None

class IngredientCreate(IngredientBase):
    pass

class IngredientUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    location: Optional[str] = None
    quantity: Optional[float] = None
    unit: Optional[str] = None
    expiry_date: Optional[date] = None

class Ingredient(IngredientBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Shopping List Schemas
class ShoppingItemBase(BaseModel):
    item_name: str
    quantity: float
    unit: str
    is_purchased: bool = False

class ShoppingItemCreate(ShoppingItemBase):
    pass

class ShoppingItem(ShoppingItemBase):
    id: int
    shopping_list_id: int

    class Config:
        from_attributes = True

class ShoppingListBase(BaseModel):
    name: str

class ShoppingListCreate(ShoppingListBase):
    pass

class ShoppingList(ShoppingListBase):
    id: int
    created_at: datetime
    items: List[ShoppingItem] = []

    class Config:
        from_attributes = True

# Recipe Schemas
class RecipeBase(BaseModel):
    name: str
    description: Optional[str] = None
    ingredients: str  # JSON string
    instructions: str
    prep_time: Optional[int] = None
    servings: int = 2
    calories: Optional[int] = None
    is_healthy: bool = True

class RecipeCreate(RecipeBase):
    pass

class Recipe(RecipeBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class UserBase(BaseModel):
    email: EmailStr
    username:str

class UserCreate(UserBase):
    password:str
class UserLogin(BaseModel):
    email: EmailStr
    password:str

class User(UserBase):
    id:int
    created_at: datetime

class Config:
    from_attributes =True

class Token(BaseModel):
    access_token:str
    token_type:str

class TokenData(BaseModel):
    email: Optional[str]=None
