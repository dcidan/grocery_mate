"""
Seed script to populate database with sample data
Run: python seed_data.py
"""
from datetime import date, timedelta
import json
from app.database import SessionLocal, engine
from app.models import Base, Ingredient, Recipe

# Create tables
Base.metadata.create_all(bind=engine)

def seed_ingredients():
    """Add sample ingredients"""
    db = SessionLocal()
    
    sample_ingredients = [
        # Vegetables
        {
            "name": "carrot",
            "category": "Vegetables",
            "location": "Fridge",
            "quantity": 1.0,
            "unit": "kg",
            "expiry_date": date.today() + timedelta(days=10)
        },
        {
            "name": "broccoli",
            "category": "Vegetables",
            "location": "Fridge",
            "quantity": 0.5,
            "unit": "kg",
            "expiry_date": date.today() + timedelta(days=5)
        },
        {
            "name": "bell pepper",
            "category": "Vegetables",
            "location": "Fridge",
            "quantity": 3,
            "unit": "pieces",
            "expiry_date": date.today() + timedelta(days=7)
        },
        # Fruits
        {
            "name": "banana",
            "category": "Fruits",
            "location": "Pantry",
            "quantity": 6,
            "unit": "pieces",
            "expiry_date": date.today() + timedelta(days=4)
        },
        {
            "name": "strawberry",
            "category": "Fruits",
            "location": "Fridge",
            "quantity": 0.5,
            "unit": "kg",
            "expiry_date": date.today() + timedelta(days=3)
        },
        # Dairy
        {
            "name": "yogurt",
            "category": "Dairy",
            "location": "Fridge",
            "quantity": 500,
            "unit": "ml",
            "expiry_date": date.today() + timedelta(days=14)
        },
        {
            "name": "milk",
            "category": "Dairy",
            "location": "Fridge",
            "quantity": 1,
            "unit": "L",
            "expiry_date": date.today() + timedelta(days=7)
        },
        # Meat
        {
            "name": "chicken",
            "category": "Meat",
            "location": "Fridge",
            "quantity": 1,
            "unit": "kg",
            "expiry_date": date.today() + timedelta(days=2)
        },
        # Pantry items
        {
            "name": "rice",
            "category": "Grains",
            "location": "Pantry",
            "quantity": 2,
            "unit": "kg",
            "expiry_date": None
        },
        {
            "name": "olive oil",
            "category": "Condiments",
            "location": "Pantry",
            "quantity": 500,
            "unit": "ml",
            "expiry_date": None
        },
        {
            "name": "soy sauce",
            "category": "Condiments",
            "location": "Pantry",
            "quantity": 250,
            "unit": "ml",
            "expiry_date": None
        },
        {
            "name": "garlic",
            "category": "Vegetables",
            "location": "Pantry",
            "quantity": 10,
            "unit": "pieces",
            "expiry_date": date.today() + timedelta(days=30)
        },
        {
            "name": "lettuce",
            "category": "Vegetables",
            "location": "Fridge",
            "quantity": 1,
            "unit": "pieces",
            "expiry_date": date.today() + timedelta(days=5)
        },
        {
            "name": "tomato",
            "category": "Vegetables",
            "location": "Fridge",
            "quantity": 4,
            "unit": "pieces",
            "expiry_date": date.today() + timedelta(days=6)
        },
        {
            "name": "cucumber",
            "category": "Vegetables",
            "location": "Fridge",
            "quantity": 2,
            "unit": "pieces",
            "expiry_date": date.today() + timedelta(days=8)
        },
        {
            "name": "honey",
            "category": "Condiments",
            "location": "Pantry",
            "quantity": 250,
            "unit": "ml",
            "expiry_date": None
        }
    ]
    
    added = 0
    for ing_data in sample_ingredients:
        # Check if already exists
        existing = db.query(Ingredient).filter(Ingredient.name == ing_data["name"]).first()
        if not existing:
            ingredient = Ingredient(**ing_data)
            db.add(ingredient)
            added += 1
    
    db.commit()
    db.close()
    print(f"✅ Added {added} sample ingredients")

def seed_recipes():
    """Add sample healthy recipes"""
    db = SessionLocal()
    
    sample_recipes = [
        {
            "name": "Grilled Chicken Salad",
            "description": "Healthy protein-packed salad with fresh vegetables",
            "ingredients": json.dumps(["chicken", "lettuce", "tomato", "cucumber", "olive oil"]),
            "instructions": "1. Grill chicken breast until fully cooked\n2. Chop lettuce, tomatoes, and cucumber\n3. Slice grilled chicken\n4. Mix all ingredients in a bowl\n5. Drizzle with olive oil\n6. Season with salt and pepper to taste",
            "prep_time": 20,
            "servings": 2,
            "calories": 350,
            "is_healthy": True
        },
        {
            "name": "Vegetable Stir Fry",
            "description": "Quick and nutritious vegetable dish",
            "ingredients": json.dumps(["broccoli", "carrot", "bell pepper", "soy sauce", "garlic"]),
            "instructions": "1. Heat pan with small amount of oil\n2. Mince garlic and add to pan\n3. Add chopped vegetables\n4. Stir fry for 5-7 minutes\n5. Add soy sauce\n6. Cook for 2 more minutes\n7. Serve hot with rice",
            "prep_time": 15,
            "servings": 3,
            "calories": 180,
            "is_healthy": True
        },
        {
            "name": "Fruit Smoothie",
            "description": "Refreshing and vitamin-rich smoothie",
            "ingredients": json.dumps(["banana", "strawberry", "yogurt", "honey"]),
            "instructions": "1. Peel and slice bananas\n2. Wash strawberries\n3. Add all fruits to blender\n4. Add yogurt\n5. Add 1 tablespoon of honey\n6. Blend until smooth\n7. Serve immediately",
            "prep_time": 5,
            "servings": 1,
            "calories": 220,
            "is_healthy": True
        },
        {
            "name": "Chicken Fried Rice",
            "description": "Delicious one-pan meal with vegetables",
            "ingredients": json.dumps(["chicken", "rice", "carrot", "garlic", "soy sauce"]),
            "instructions": "1. Cook rice and let it cool\n2. Cut chicken into small pieces\n3. Dice carrots and mince garlic\n4. Heat oil in large pan or wok\n5. Cook chicken until done, remove\n6. Stir fry vegetables\n7. Add rice and soy sauce\n8. Add chicken back\n9. Mix well and serve hot",
            "prep_time": 30,
            "servings": 4,
            "calories": 420,
            "is_healthy": True
        },
        {
            "name": "Garlic Roasted Vegetables",
            "description": "Simple and healthy roasted veggie medley",
            "ingredients": json.dumps(["broccoli", "carrot", "bell pepper", "garlic", "olive oil"]),
            "instructions": "1. Preheat oven to 200°C (400°F)\n2. Cut vegetables into similar-sized pieces\n3. Mince garlic\n4. Toss vegetables with olive oil and garlic\n5. Season with salt and pepper\n6. Spread on baking sheet\n7. Roast for 20-25 minutes\n8. Serve as side dish",
            "prep_time": 25,
            "servings": 4,
            "calories": 120,
            "is_healthy": True
        }
    ]
    
    added = 0
    for recipe_data in sample_recipes:
        # Check if already exists
        existing = db.query(Recipe).filter(Recipe.name == recipe_data["name"]).first()
        if not existing:
            recipe = Recipe(**recipe_data)
            db.add(recipe)
            added += 1
    
    db.commit()
    db.close()
    print(f"✅ Added {added} sample recipes")

if __name__ == "__main__":
    print("🌱 Seeding database with sample data...")
    print()
    seed_ingredients()
    seed_recipes()
    print()
    print("✅ Database seeding complete!")
    print("You can now start the application and see sample data.")
