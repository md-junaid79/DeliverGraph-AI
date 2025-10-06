# src/utils/state.py
from typing import TypedDict, List, Optional

class DeliveryState(TypedDict):
    """
    State is a dictionary that flows through the LangGraph workflow
    Contains all information about a delivery request
    """
    
    # ============ IDENTIFIERS ============
    ticket_id: str                          # Unique delivery ticket ID
    user_id: str                            # User identifier
    user_email: Optional[str]               # User email for notifications
    
    # ============ INPUT PARAMETERS ============
    material_type: Optional[str]            # Type of material: standard, fragile, perishable, heavy
    distance: Optional[float]               # Distance in kilometers (manual input)
    urgency: Optional[str]                  # Urgency: standard, express, same_day
    weight: Optional[float]                 # Weight in kilograms
    location_type: Optional[str]            # Location: urban, suburban, rural
    
    # ============ INTERMEDIATE CALCULATIONS ============
    base_price: Optional[float]             # Base price (material + distance)
    urgency_multiplier: Optional[float]     # Urgency multiplier (1.0, 1.5, 2.0)
    weight_surcharge: Optional[float]       # Extra charge for excess weight
    location_adjustment: Optional[float]    # Location-based adjustment
    
    # ============ FINAL OUTPUT ============
    total_price: Optional[float]            # Final calculated price
    
    # ============ METADATA ============
    action_log: List[str]                   # Log of all processing steps
    error_message: Optional[str]            # Error message if any
    retry_count: int                        # Number of retry attempts