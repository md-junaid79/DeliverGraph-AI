# test_database.py
from src.database.models import SessionLocal
from src.database.crud import create_user, create_delivery, get_all_users, get_all_deliveries

def test_database():
    """Test database operations"""
    db = SessionLocal()
    
    try:
        # Test 1: Create a user
        print("\n📝 Test 1: Creating user...")
        user = create_user(db, name="John Doe", email="john@example.com", phone="+919876543210")
        print(f"   User ID: {user.user_id}")
        
        # Test 2: Create a delivery
        print("\n📝 Test 2: Creating delivery...")
        delivery_data = {
            'material_type': 'fragile',
            'distance': 15.0,
            'urgency': 'express',
            'weight': 5.0,
            'location_type': 'urban'
        }
        delivery = create_delivery(db, user.user_id, delivery_data)
        print(f"   Ticket ID: {delivery.ticket_id}")
        
        # Test 3: Retrieve all users
        print("\n📝 Test 3: Retrieving all users...")
        users = get_all_users(db)
        print(f"   Total users: {len(users)}")
        
        # Test 4: Retrieve all deliveries
        print("\n📝 Test 4: Retrieving all deliveries...")
        deliveries = get_all_deliveries(db)
        print(f"   Total deliveries: {len(deliveries)}")
        
        print("\n✅ All database tests passed!")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    test_database()