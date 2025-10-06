# src/nodes/error_handler.py
from ..utils.state import DeliveryState
from ..database.crud import log_error, update_delivery
from ..database.models import SessionLocal

def error_handler_node(state: DeliveryState) -> DeliveryState:
    """
    Handles errors and logs escalation
    """
    error_message = state.get('error_message', 'Unknown error')
    ticket_id = state['ticket_id']
    
    # Log to database
    db = SessionLocal()
    try:
        log_error(
            db,
            ticket_id=ticket_id,
            error_type="workflow_error",
            error_message=error_message,
            node_name="error_handler"
        )
        
        update_delivery(db, ticket_id, {
            'status': 'failed',
            'action_log': state['action_log']
        })
        
        state['action_log'].append(f"🚨 Error logged: {error_message}")
    except Exception as e:
        state['action_log'].append(f"⚠️ Error logging failed: {str(e)}")
    finally:
        db.close()
    
    return state