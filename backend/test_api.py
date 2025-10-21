"""
Simple API test script
Run: python test_api.py
"""
import requests
import json
from datetime import date, timedelta

BASE_URL = "http://localhost:8778"

def test_health():
    """Test health endpoint"""
    print("Testing health endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    if response.status_code == 200:
        print("✅ Health check passed")
        return True
    else:
        print(f"❌ Health check failed: {response.status_code}")
        return False

def test_ingredients():
    """Test ingredients endpoints"""
    print("\nTesting ingredients endpoints...")
    
    # Create ingredient
    ingredient_data = {
        "name": "test_tomato",
        "category": "Vegetables",
        "location": "Fridge",
        "quantity": 5,
        "unit": "pieces",
        "expiry_date": str(date.today() + timedelta(days=7))
    }
    
    response = requests.post(f"{BASE_URL}/ingredients/", json=ingredient_data)
    if response.status_code == 200:
        print("✅ Create ingredient passed")
        ingredient_id = response.json()["id"]
        
        # Get ingredient
        response = requests.get(f"{BASE_URL}/ingredients/{ingredient_id}")
        if response.status_code == 200:
            print("✅ Get ingredient passed")
        
        # Delete ingredient
        response = requests.delete(f"{BASE_URL}/ingredients/{ingredient_id}")
        if response.status_code == 200:
            print("✅ Delete ingredient passed")
        
        return True
    else:
        print(f"❌ Create ingredient failed: {response.status_code}")
        print(response.text)
        return False

def test_shopping_lists():
    """Test shopping list endpoints"""
    print("\nTesting shopping list endpoints...")
    
    # Create shopping list
    list_data = {"name": "Test Shopping List"}
    response = requests.post(f"{BASE_URL}/shopping-lists/", json=list_data)
    
    if response.status_code == 200:
        print("✅ Create shopping list passed")
        list_id = response.json()["id"]
        
        # Add item to list
        item_data = {
            "item_name": "test_item",
            "quantity": 2,
            "unit": "kg",
            "is_purchased": False
        }
        response = requests.post(f"{BASE_URL}/shopping-lists/{list_id}/items", json=item_data)
        if response.status_code == 200:
            print("✅ Add item to list passed")
        
        # Delete shopping list
        response = requests.delete(f"{BASE_URL}/shopping-lists/{list_id}")
        if response.status_code == 200:
            print("✅ Delete shopping list passed")
        
        return True
    else:
        print(f"❌ Create shopping list failed: {response.status_code}")
        return False

def test_recipes():
    """Test recipe endpoints"""
    print("\nTesting recipe endpoints...")
    
    # Get all recipes
    response = requests.get(f"{BASE_URL}/recipes/")
    if response.status_code == 200:
        print(f"✅ Get recipes passed ({len(response.json())} recipes found)")
        return True
    else:
        print(f"❌ Get recipes failed: {response.status_code}")
        return False

def run_all_tests():
    """Run all API tests"""
    print("=" * 50)
    print("🧪 GroceryMate API Test Suite")
    print("=" * 50)
    
    try:
        tests = [
            ("Health Check", test_health),
            ("Ingredients API", test_ingredients),
            ("Shopping Lists API", test_shopping_lists),
            ("Recipes API", test_recipes)
        ]
        
        results = []
        for test_name, test_func in tests:
            try:
                result = test_func()
                results.append((test_name, result))
            except Exception as e:
                print(f"❌ {test_name} error: {str(e)}")
                results.append((test_name, False))
        
        print("\n" + "=" * 50)
        print("Test Results Summary:")
        print("=" * 50)
        
        passed = sum(1 for _, result in results if result)
        total = len(results)
        
        for test_name, result in results:
            status = "✅ PASSED" if result else "❌ FAILED"
            print(f"{test_name}: {status}")
        
        print(f"\nTotal: {passed}/{total} tests passed")
        
        if passed == total:
            print("\n🎉 All tests passed!")
        else:
            print(f"\n⚠️  {total - passed} test(s) failed")
            
    except requests.exceptions.ConnectionError:
        print("\n❌ Cannot connect to API!")
        print("Make sure the backend server is running on http://localhost:8000")
        print("Start it with: uvicorn app.main:app --reload")

if __name__ == "__main__":
    run_all_tests()
