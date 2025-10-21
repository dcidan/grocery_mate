from sqlalchemy import Column, Integer, String, Float, Date, Boolean, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

# USER 

class User(Base):
    __tablename__ ="users"
    id= Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    # Relationships
    ingredients = relationship("Ingredient", back_populates="owner")
    shopping_lists = relationship("ShoppingList", back_populates="owner")
    recipes = relationship("Recipe", back_populates="owner")


# APP

class Ingredient(Base):
    __tablename__ = "ingredients"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    category = Column(String, nullable=False)  # Dairy, Vegetables, Fruits, Meat, etc.
    location = Column(String, nullable=False)  # Fridge or Pantry
    quantity = Column(Float, default=0)
    unit = Column(String, nullable=False)  # kg, liters, pieces, etc.
    expiry_date = Column(Date, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    owner = relationship("User", back_populates="ingredients")

class ShoppingList(Base):
    __tablename__ = "shopping_lists"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    items = relationship("ShoppingItem", back_populates="shopping_list", cascade="all, delete-orphan")
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    owner = relationship("User", back_populates="shopping_lists")

class ShoppingItem(Base):
    __tablename__ = "shopping_items"
    
    id = Column(Integer, primary_key=True, index=True)
    shopping_list_id = Column(Integer, ForeignKey("shopping_lists.id"))
    item_name = Column(String, nullable=False)
    quantity = Column(Float, default=1)
    unit = Column(String, nullable=False)
    is_purchased = Column(Boolean, default=False)
    shopping_list = relationship("ShoppingList", back_populates="items")

class Recipe(Base):
    __tablename__ = "recipes"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    description = Column(Text)
    ingredients = Column(Text, nullable=False)  # JSON string of ingredients
    instructions = Column(Text, nullable=False)
    prep_time = Column(Integer)  # in minutes
    servings = Column(Integer, default=2)
    calories = Column(Integer, nullable=True)
    is_healthy = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    owner = relationship("User", back_populates="recipes")
