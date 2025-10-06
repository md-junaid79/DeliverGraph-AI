# src/nodes/final_price_node.py
from ..utils.state import DeliveryState
from ..database.crud import update_delivery
from ..database.models import SessionLocal

def final_price_node(state: DeliveryState) -> DeliveryState:
    """
    Calculates final delivery price
    """
    base = state.get('base_price', 0)
    multiplier = state.get('urgency_multiplier', 1.0)
    weight_surcharge = state.get('weight_surcharge', 0)
    location_adj = state.get('location_adjustment', 0)
    
    total = (base * multiplier) + weight_surcharge + location_adj
    state['total_price'] = round(total, 2)
    
    state['action_log'].append(
        f"💳 Final Calculation: "
        f"(₹{base} × {multiplier}) + ₹{weight_surcharge} + ₹{location_adj} = ₹{state['total_price']}"
    )
    
    # Update database
    db = SessionLocal()
    try:
        update_delivery(db, state['ticket_id'], {
            'total_price': state['total_price'],
            'action_log': state['action_log'],
            'status': 'completed'
        })
        state['action_log'].append("✅ Price saved to database")
    except Exception as e:
        state['action_log'].append(f"⚠️ Database update warning: {str(e)}")
    finally:
        db.close()
    
    return state