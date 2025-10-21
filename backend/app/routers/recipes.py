from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import json
from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/recipes", tags=["recipes"])

@router.get("/", response_model=List[schemas.Recipe])
def get_recipes(healthy_only: bool = False, db: Session = Depends(get_db)):
    """Get all recipes, optionally filtered by healthy recipes"""
    query = db.query(models.Recipe)
    if healthy_only:
        query = query.filter(models.Recipe.is_healthy == True)
    return query.all()

@router.get("/{recipe_id}", response_model=schemas.Recipe)
def get_recipe(recipe_id: int, db: Session = Depends(get_db)):
    """Get a specific recipe by ID"""
    recipe = db.query(models.Recipe).filter(models.Recipe.id == recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe

@router.post("/", response_model=schemas.Recipe)
def create_recipe(recipe: schemas.RecipeCreate, db: Session = Depends(get_db)):
    """Create a new recipe"""
    db_recipe = models.Recipe(**recipe.model_dump())
    db.add(db_recipe)
    db.commit()
    db.refresh(db_recipe)
    return db_recipe

@router.delete("/{recipe_id}")
def delete_recipe(recipe_id: int, db: Session = Depends(get_db)):
    """Delete a recipe"""
    db_recipe = db.query(models.Recipe).filter(models.Recipe.id == recipe_id).first()
    if not db_recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    
    db.delete(db_recipe)
    db.commit()
    return {"message": "Recipe deleted successfully"}

@router.get("/match/ingredients", response_model=List[schemas.Recipe])
def find_matching_recipes(db: Session = Depends(get_db)):
    """Find recipes that can be made with available ingredients"""
    # Get all available ingredients
    available_ingredients = db.query(models.Ingredient).filter(
        models.Ingredient.quantity > 0
    ).all()
    
    available_names = {ing.name.lower() for ing in available_ingredients}
    
    # Get all recipes
    all_recipes = db.query(models.Recipe).all()
    matching_recipes = []
    
    for recipe in all_recipes:
        try:
            recipe_ingredients = json.loads(recipe.ingredients)
            # Check if all recipe ingredients are available
            required_ingredients = {ing.lower() for ing in recipe_ingredients}
            
            # Calculate match percentage
            if required_ingredients.issubset(available_names):
                matching_recipes.append(recipe)
        except json.JSONDecodeError:
            continue
    
    return matching_recipes

@router.post("/seed-sample")
def seed_sample_recipes(db: Session = Depends(get_db)):
    """Seed database with sample healthy recipes"""
    sample_recipes = [
        {
            "name": "Grilled Chicken Salad",
            "description": "Healthy protein-packed salad with fresh vegetables",
            "ingredients": json.dumps(["chicken", "lettuce", "tomato", "cucumber", "olive oil"]),
            "instructions": "1. Grill chicken breast\n2. Chop vegetables\n3. Mix with olive oil\n4. Season to taste",
            "prep_time": 20,
            "servings": 2,
            "calories": 350,
            "is_healthy": True
        },
        {
            "name": "Vegetable Stir Fry",
            "description": "Quick and nutritious vegetable dish",
            "ingredients": json.dumps(["broccoli", "carrot", "bell pepper", "soy sauce", "garlic"]),
            "instructions": "1. Heat pan with oil\n2. Add garlic\n3. Stir fry vegetables\n4. Add soy sauce",
            "prep_time": 15,
            "servings": 3,
            "calories": 180,
            "is_healthy": True
        },
        {
            "name": "Fruit Smoothie",
            "description": "Refreshing and vitamin-rich smoothie",
            "ingredients": json.dumps(["banana", "strawberry", "yogurt", "honey"]),
            "instructions": "1. Add all ingredients to blender\n2. Blend until smooth\n3. Serve cold",
            "prep_time": 5,
            "servings": 1,
            "calories": 220,
            "is_healthy": True
        }
    ]
    
    for recipe_data in sample_recipes:
        # Check if recipe already exists
        existing = db.query(models.Recipe).filter(models.Recipe.name == recipe_data["name"]).first()
        if not existing:
            db_recipe = models.Recipe(**recipe_data)
            db.add(db_recipe)
    
    db.commit()
    return {"message": "Sample recipes seeded successfully"}
