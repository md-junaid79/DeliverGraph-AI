# src/nodes/material_node.py
from ..utils.state import DeliveryState
from ..utils.pricing_config import PRICING_CONFIG

def material_pricing_node(state: DeliveryState) -> DeliveryState:
    """
    Calculates base price based on material type and distance
    """
    material_type = state.get('material_type', 'standard')
    distance = state.get('distance', 0)
    
    # Get base price for material
    base = PRICING_CONFIG['material_base_prices'].get(material_type, 100.0)
    
    # Add distance cost
    distance_cost = distance * PRICING_CONFIG['distance_rate_per_km']
    
    state['base_price'] = base + distance_cost
    state['action_log'].append(
        f"💰 Material pricing: {material_type.upper()} "
        f"(base: ₹{base} + distance: {distance}km × ₹{PRICING_CONFIG['distance_rate_per_km']}/km) "
        f"= ₹{state['base_price']}"
    )
    
    return state