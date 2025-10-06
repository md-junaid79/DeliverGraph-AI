# src/nodes/notification_node.py
from ..utils.state import DeliveryState
from ..api.notifications import NotificationService
from ..database.crud import get_user
from ..database.models import SessionLocal

def notification_node(state: DeliveryState) -> DeliveryState:
    """
    Sends price notification via email (optional)
    Primary notification is via web UI
    """
    ticket_id = state['ticket_id']
    total_price = state['total_price']
    user_id = state['user_id']
    
    # Get user email
    user_email = state.get('user_email')
    
    if not user_email:
        db = SessionLocal()
        try:
            user = get_user(db, user_id)
            if user:
                user_email = user.email
        finally:
            db.close()
    
    # Send email notification (optional)
    if user_email:
        notifier = NotificationService()
        breakdown = {
            'base_price': state.get('base_price', 0),
            'urgency_multiplier': state.get('urgency_multiplier', 1.0),
            'weight_surcharge': state.get('weight_surcharge', 0),
            'location_adjustment': state.get('location_adjustment', 0)
        }
        
        result = notifier.send_price_quote_email(
            email=user_email,
            ticket_id=ticket_id,
            total_price=total_price,
            breakdown=breakdown
        )
        
        if result['status'] == 'success':
            state['action_log'].append(f"📧 Email sent to {user_email}")
        elif result['status'] == 'skipped':
            state['action_log'].append("ℹ️ Email notification skipped (not configured)")
        else:
            state['action_log'].append(f"⚠️ Email failed: {result['message']}")
    else:
        state['action_log'].append("ℹ️ No email provided for notification")
    
    # Primary notification is via web UI
    state['action_log'].append("✅ Notification ready for display")
    
    return state