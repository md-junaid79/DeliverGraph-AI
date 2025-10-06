# src/nodes/weight_node.py
from ..utils.state import DeliveryState
from ..utils.pricing_config import PRICING_CONFIG

def weight_volume_node(state: DeliveryState) -> DeliveryState:
    """
    Adds surcharge for excess weight
    """
    weight = state.get('weight', 0)
    threshold = PRICING_CONFIG['weight_thresholds']['threshold_kg']
    surcharge_rate = PRICING_CONFIG['weight_thresholds']['surcharge_per_kg']
    
    if weight > threshold:
        excess = weight - threshold
        surcharge = excess * surcharge_rate
    else:
        surcharge = 0.0
    
    state['weight_surcharge'] = surcharge
    
    if surcharge > 0:
        state['action_log'].append(
            f"⚖️ Weight: {weight}kg (excess: {excess}kg × ₹{surcharge_rate}/kg) = +₹{surcharge}"
        )
    else:
        state['action_log'].append(f"⚖️ Weight: {weight}kg (within threshold)")
    
    return state