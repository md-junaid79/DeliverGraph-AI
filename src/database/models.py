from sqlalchemy import Column, Integer, String, Float, DateTime, JSON, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timezone
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create base class for declarative models
Base = declarative_base()

# ============ USER TABLE ============
class User(Base):
    """User table to store customer information"""
    __tablename__ = 'users'
    
    user_id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String)
    phone = Column(String)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    
    def __repr__(self):
        return f"<User(user_id='{self.user_id}', name='{self.name}')>"

# ============ DELIVERY TABLE ============
class Delivery(Base):
    """Delivery table to store all delivery requests and prices"""
    __tablename__ = 'deliveries'
    
    ticket_id = Column(String, primary_key=True)
    user_id = Column(String, nullable=False)
    material_type = Column(String)
    distance = Column(Float)
    urgency = Column(String)
    weight = Column(Float)
    location_type = Column(String)
    total_price = Column(Float)
    status = Column(String, default='pending')
    action_log = Column(JSON, default=[])
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    
    def __repr__(self):
        return f"<Delivery(ticket_id='{self.ticket_id}', status='{self.status}')>"

# ============ ERROR LOG TABLE ============
class ErrorLog(Base):
    """Error log table to track all errors in the system"""
    __tablename__ = 'error_logs'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    ticket_id = Column(String)
    error_type = Column(String)
    error_message = Column(String)
    node_name = Column(String)
    timestamp = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    
    def __repr__(self):
        return f"<ErrorLog(id={self.id}, ticket_id='{self.ticket_id}')>"

# ============ DATABASE CONNECTION ============
# Get database URL from environment or use default SQLite
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///delivergraph.db')

# Create database engine
engine = create_engine(
    DATABASE_URL,
    echo=False,  # Set to True to see SQL queries
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

# Create session factory
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False
)

# ============ DATABASE INITIALIZATION ============
def init_db():
    """
    Initialize database - creates all tables
    Run this once to set up the database
    """
    print("🔧 Creating database tables...")
    Base.metadata.create_all(engine)
    print("✅ Database initialized successfully!")
    print(f"📁 Database location: {DATABASE_URL}")
    
    # Print table names
    print("\n📊 Created tables:")
    for table in Base.metadata.sorted_tables:
        print(f"   - {table.name}")

def get_db():
    """
    Get database session
    Used in API endpoints
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ============ RUN DIRECTLY TO INITIALIZE ============
if __name__ == "__main__":
    init_db()