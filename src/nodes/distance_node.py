# src/nodes/distance_node.py
from ..utils.state import DeliveryState

def distance_node(state: DeliveryState) -> DeliveryState:
    """
    NODE 2: Distance Processing
    - Uses manual distance input (no API calls)
    - Validates distance value
    """
    print("\n🔵 NODE 2: Distance Processing")
    
    distance = state.get('distance')
    
    if not distance or distance <= 0:
        state['error_message'] = "Invalid distance provided"
        state['action_log'].append(f"❌ {state['error_message']}")
        print("   ❌ Invalid distance")
        return state
    
    state['action_log'].append(f"📍 Distance: {distance} km (manual input)")
    print(f"   ✅ Distance: {distance} km")
    
    return state