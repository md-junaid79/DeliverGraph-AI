# src/database/crud.py
from sqlalchemy.orm import Session
from .models import User, Delivery, ErrorLog
import uuid
from datetime import datetime

# ============ USER OPERATIONS ============

def create_user(db: Session, name: str, email: str = None, phone: str = None):
    """Create a new user"""
    user_id = str(uuid.uuid4())[:8]
    user = User(
        user_id=user_id,
        name=name,
        email=email,
        phone=phone,
        created_at=datetime.utcnow()
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    print(f"✅ User created: {user_id}")
    return user

def get_user(db: Session, user_id: str):
    """Get user by user_id"""
    return db.query(User).filter(User.user_id == user_id).first()

def get_all_users(db: Session, limit: int = 100):
    """Get all users"""
    return db.query(User).limit(limit).all()

# ============ DELIVERY OPERATIONS ============

def create_delivery(db: Session, user_id: str, inputs: dict):
    """Create a new delivery request"""
    ticket_id = f"DEL-{uuid.uuid4().hex[:8].upper()}"
    
    delivery = Delivery(
        ticket_id=ticket_id,
        user_id=user_id,
        material_type=inputs.get('material_type'),
        distance=inputs.get('distance'),
        urgency=inputs.get('urgency'),
        weight=inputs.get('weight'),
        location_type=inputs.get('location_type'),
        total_price=None,
        status='pending',
        action_log=[],
        created_at=datetime.utcnow()
    )
    
    db.add(delivery)
    db.commit()
    db.refresh(delivery)
    print(f"✅ Delivery created: {ticket_id}")
    return delivery

def update_delivery(db: Session, ticket_id: str, updates: dict):
    """Update an existing delivery"""
    delivery = db.query(Delivery).filter(Delivery.ticket_id == ticket_id).first()
    
    if not delivery:
        print(f"❌ Delivery not found: {ticket_id}")
        return None
    
    # Update fields
    for key, value in updates.items():
        if hasattr(delivery, key):
            setattr(delivery, key, value)
    
    db.commit()
    db.refresh(delivery)
    print(f"✅ Delivery updated: {ticket_id}")
    return delivery

def get_delivery(db: Session, ticket_id: str):
    """Get delivery by ticket_id"""
    return db.query(Delivery).filter(Delivery.ticket_id == ticket_id).first()

def get_all_deliveries(db: Session, limit: int = 100):
    """Get all deliveries, sorted by created_at descending"""
    return db.query(Delivery).order_by(Delivery.created_at.desc()).limit(limit).all()

def get_user_deliveries(db: Session, user_id: str, limit: int = 50):
    """Get all deliveries for a specific user"""
    return db.query(Delivery).filter(
        Delivery.user_id == user_id
    ).order_by(Delivery.created_at.desc()).limit(limit).all()

# ============ ERROR LOG OPERATIONS ============

def log_error(db: Session, ticket_id: str, error_type: str, 
              error_message: str, node_name: str):
    """Log an error to the database"""
    error = ErrorLog(
        ticket_id=ticket_id,
        error_type=error_type,
        error_message=error_message,
        node_name=node_name,
        timestamp=datetime.utcnow()
    )
    
    db.add(error)
    db.commit()
    print(f"🚨 Error logged: {error_type} for {ticket_id}")
    return error

def get_errors_by_ticket(db: Session, ticket_id: str):
    """Get all errors for a specific ticket"""
    return db.query(ErrorLog).filter(ErrorLog.ticket_id == ticket_id).all()

def get_all_errors(db: Session, limit: int = 100):
    """Get all errors"""
    return db.query(ErrorLog).order_by(ErrorLog.timestamp.desc()).limit(limit).all()

# ============ STATISTICS ============

def get_delivery_stats(db: Session):
    """Get delivery statistics"""
    total = db.query(Delivery).count()
    completed = db.query(Delivery).filter(Delivery.status == 'completed').count()
    failed = db.query(Delivery).filter(Delivery.status == 'failed').count()
    pending = db.query(Delivery).filter(Delivery.status == 'pending').count()
    
    # Calculate total revenue
    deliveries = db.query(Delivery).filter(Delivery.total_price.isnot(None)).all()
    total_revenue = sum(d.total_price for d in deliveries)
    avg_price = total_revenue / completed if completed > 0 else 0
    
    return {
        "total_deliveries": total,
        "completed": completed,
        "failed": failed,
        "pending": pending,
        "total_revenue": total_revenue,
        "average_price": avg_price
    }