# src/nodes/location_node.py
from ..utils.state import DeliveryState
from ..utils.pricing_config import PRICING_CONFIG

def location_node(state: DeliveryState) -> DeliveryState:
    """
    Adjusts price based on location type
    """
    location_type = state.get('location_type', 'urban')
    adjustment = PRICING_CONFIG['location_adjustments'].get(location_type, 0.0)
    
    state['location_adjustment'] = adjustment
    
    if adjustment > 0:
        state['action_log'].append(
            f"📍 Location: {location_type.upper()} (+₹{adjustment})"
        )
    else:
        state['action_log'].append(f"📍 Location: {location_type.upper()}")
    
    return state