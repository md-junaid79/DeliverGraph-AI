# src/workflow.py
from langgraph.graph import StateGraph, END
from .utils.state import DeliveryState
from .nodes.input_node import input_node
from .nodes.distance_node import distance_node
from .nodes.material_node import material_pricing_node
from .nodes.urgency_node import urgency_node
from .nodes.weight_node import weight_volume_node
from .nodes.location_node import location_node
from .nodes.final_price_node import final_price_node
from .nodes.notification_node import notification_node
from .nodes.error_handler import error_handler_node

def create_workflow():
    """
    Creates the LangGraph workflow
    """
    workflow = StateGraph(DeliveryState)
    
    # Add nodes
    workflow.add_node("input", input_node)
    workflow.add_node("distance_node", distance_node)
    workflow.add_node("material", material_pricing_node)
    workflow.add_node("urgency_node", urgency_node)
    workflow.add_node("weight_volume_node", weight_volume_node)
    workflow.add_node("location_node", location_node)
    workflow.add_node("final_price_node", final_price_node)
    workflow.add_node("notification_node", notification_node)
    workflow.add_node("error_handler_node", error_handler_node)
    
    # Define conditional routing
    def check_for_errors(state: DeliveryState):
        if state.get('error_message'):
            return "error_handler_node"
        return "continue"
    
    # Set entry point
    workflow.set_entry_point("input")
    
    # Add edges with error handling
    workflow.add_conditional_edges(
        "input",
        check_for_errors,
        {
            "continue": "distance_node",
            "error_handler_node": "error_handler_node"
        }
    )
    
    workflow.add_conditional_edges(
        "distance_node",
        check_for_errors,
        {
            "continue": "material",
            "error_handler_node": "error_handler_node"
        }
    )
    
    workflow.add_edge("material", "urgency_node")
    workflow.add_edge("urgency_node", "weight_volume_node")
    workflow.add_edge("weight_volume_node", "location_node")
    workflow.add_edge("location_node", "final_price_node")
    workflow.add_edge("final_price_node", "notification_node")
    workflow.add_edge("notification_node", END)
    workflow.add_edge("error_handler_node", END)
    
    return workflow.compile()

# Create compiled workflow
app = create_workflow()