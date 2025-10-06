# src/utils/pricing_config.py

# ============ PRICING CONFIGURATION ============
PRICING_CONFIG = {
    # Base prices for different material types
    "material_base_prices": {
        "standard": 100.0,      # Regular items
        "fragile": 150.0,       # Fragile items (glass, electronics)
        "perishable": 180.0,    # Perishable goods (food, medicine)
        "heavy": 200.0          # Heavy items (furniture, machinery)
    },
    
    # Urgency multipliers
    "urgency_multipliers": {
        "standard": 1.0,        # Regular delivery (3-5 days)
        "express": 1.5,         # Express delivery (1-2 days)
        "same_day": 2.0         # Same day delivery
    },
    
    # Weight thresholds and surcharges
    "weight_thresholds": {
        "threshold_kg": 10,            # Weight limit before surcharge
        "surcharge_per_kg": 5.0        # Additional cost per kg over threshold
    },
    
    # Location adjustments
    "location_adjustments": {
        "urban": 0.0,           # City areas - no extra charge
        "suburban": 25.0,       # Suburban areas - moderate charge
        "rural": 50.0           # Rural areas - higher charge
    },
    
    # Distance pricing
    "distance_rate_per_km": 4.0     # Cost per kilometer
}

# ============ VALIDATION FUNCTIONS ============

def validate_material_type(material_type: str) -> bool:
    """Check if material type is valid"""
    return material_type in PRICING_CONFIG["material_base_prices"]

def validate_urgency(urgency: str) -> bool:
    """Check if urgency level is valid"""
    return urgency in PRICING_CONFIG["urgency_multipliers"]

def validate_location_type(location_type: str) -> bool:
    """Check if location type is valid"""
    return location_type in PRICING_CONFIG["location_adjustments"]

def get_valid_options():
    """Get all valid options for form dropdowns"""
    return {
        "material_types": list(PRICING_CONFIG["material_base_prices"].keys()),
        "urgencies": list(PRICING_CONFIG["urgency_multipliers"].keys()),
        "location_types": list(PRICING_CONFIG["location_adjustments"].keys())
    }

# ============ PRICING HELPERS ============

def calculate_base_price(material_type: str, distance: float) -> float:
    """Calculate base price before modifiers"""
    base = PRICING_CONFIG["material_base_prices"].get(material_type, 100.0)
    distance_cost = distance * PRICING_CONFIG["distance_rate_per_km"]
    return base + distance_cost

def calculate_urgency_cost(base_price: float, urgency: str) -> float:
    """Calculate price after urgency multiplier"""
    multiplier = PRICING_CONFIG["urgency_multipliers"].get(urgency, 1.0)
    return base_price * multiplier

def calculate_weight_surcharge(weight: float) -> float:
    """Calculate weight surcharge"""
    threshold = PRICING_CONFIG["weight_thresholds"]["threshold_kg"]
    rate = PRICING_CONFIG["weight_thresholds"]["surcharge_per_kg"]
    
    if weight > threshold:
        excess = weight - threshold
        return excess * rate
    return 0.0

def calculate_location_adjustment(location_type: str) -> float:
    """Get location adjustment cost"""
    return PRICING_CONFIG["location_adjustments"].get(location_type, 0.0)