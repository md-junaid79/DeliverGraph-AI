# src/nodes/input_node.py
from ..utils.state import DeliveryState
from ..utils.pricing_config import validate_material_type, validate_urgency, validate_location_type
from ..database.crud import create_delivery
from ..database.models import SessionLocal
import uuid

def input_node(state: DeliveryState) -> DeliveryState:
    """
    NODE 1: Input Validation
    - Validates all input parameters
    - Creates delivery record in database
    - Initializes the state
    """
    print("\n🔵 NODE 1: Input Validation")
    
    # Generate ticket ID if not exists
    if not state.get('ticket_id'):
        state['ticket_id'] = f"DEL-{uuid.uuid4().hex[:8].upper()}"
        print(f"   Generated Ticket ID: {state['ticket_id']}")
    
    # Initialize action log and retry count. If action_log exists but is None
    # or not a list (e.g., deserialized from DB or provided as null), replace
    # it with an empty list so `.append()` calls are safe.
    if 'action_log' not in state or not isinstance(state.get('action_log'), list):
        state['action_log'] = []

    # Ensure retry_count is an integer
    try:
        if 'retry_count' not in state or not isinstance(state.get('retry_count'), int):
            state['retry_count'] = 0
    except Exception:
        state['retry_count'] = 0
    
    # ============ VALIDATE REQUIRED FIELDS ============
    required_fields = {
        'material_type': state.get('material_type'),
        'distance': state.get('distance'),
        'urgency': state.get('urgency'),
        'weight': state.get('weight'),
        'location_type': state.get('location_type')
    }
    
    missing = [f for f, v in required_fields.items() if not v]
    
    if missing:
        state['error_message'] = f"Missing required fields: {', '.join(missing)}"
        state['action_log'].append(f"❌ Validation failed: {state['error_message']}")
        print(f"   ❌ {state['error_message']}")
        return state
    
    # ============ VALIDATE FIELD VALUES ============
    
    # Validate material type
    if not validate_material_type(state['material_type']):
        state['error_message'] = (
            f"Invalid material_type: {state['material_type']}. "
            f"Must be: standard, fragile, perishable, heavy"
        )
        state['action_log'].append(f"❌ {state['error_message']}")
        print(f"   ❌ {state['error_message']}")
        return state
    
    # Validate urgency
    if not validate_urgency(state['urgency']):
        state['error_message'] = (
            f"Invalid urgency: {state['urgency']}. "
            f"Must be: standard, express, same_day"
        )
        state['action_log'].append(f"❌ {state['error_message']}")
        print(f"   ❌ {state['error_message']}")
        return state
    
    # Validate location type
    if not validate_location_type(state['location_type']):
        state['error_message'] = (
            f"Invalid location_type: {state['location_type']}. "
            f"Must be: urban, suburban, rural"
        )
        state['action_log'].append(f"❌ {state['error_message']}")
        print(f"   ❌ {state['error_message']}")
        return state
    
    # Validate numeric fields
    if state['distance'] <= 0:
        state['error_message'] = "Distance must be greater than 0 km"
        state['action_log'].append(f"❌ {state['error_message']}")
        print(f"   ❌ {state['error_message']}")
        return state
    
    if state['weight'] <= 0:
        state['error_message'] = "Weight must be greater than 0 kg"
        state['action_log'].append(f"❌ {state['error_message']}")
        print(f"   ❌ {state['error_message']}")
        return state
    
    # ============ SAVE TO DATABASE ============
    db = SessionLocal()
    try:
        create_delivery(db, state['user_id'], {
            'material_type': state['material_type'],
            'distance': state['distance'],
            'urgency': state['urgency'],
            'weight': state['weight'],
            'location_type': state['location_type']
        })
        state['action_log'].append("✅ Input validated and ticket created")
        print("   ✅ Validation successful")
    except Exception as e:
        state['error_message'] = f"Database error: {str(e)}"
        state['action_log'].append(f"❌ {state['error_message']}")
        print(f"   ❌ Database error: {e}")
    finally:
        db.close()
    
    return state