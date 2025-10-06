# src/nodes/urgency_node.py
from ..utils.state import DeliveryState
from ..utils.pricing_config import PRICING_CONFIG

def urgency_node(state: DeliveryState) -> DeliveryState:
    """
    Applies urgency multiplier
    """
    urgency = state.get('urgency', 'standard')
    multiplier = PRICING_CONFIG['urgency_multipliers'].get(urgency, 1.0)
    
    state['urgency_multiplier'] = multiplier
    state['action_log'].append(
        f"⚡ Urgency: {urgency.upper()} (multiplier: {multiplier}x)"
    )
    
    return state