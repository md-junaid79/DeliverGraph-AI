# src/api/main.py
from fastapi import FastAPI, HTTPException, status, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
from ..workflow import app as workflow_app
from ..database.models import init_db, SessionLocal
from ..database.crud import get_delivery, get_all_deliveries, create_user
import uvicorn
import os

# Initialize FastAPI
api = FastAPI(
    title="🚚 DeliverGraph AI",
    version="1.0.0",
    description="Real-time Delivery Pricing Engine with Web UI"
)

# Mount static files
api.mount("/static", StaticFiles(directory="static"), name="static")

# Setup templates
templates = Jinja2Templates(directory="templates")

# CORS middleware
api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic Models
class DeliveryRequest(BaseModel):
    user_id: str
    user_email: Optional[str] = None
    material_type: str
    distance: float
    urgency: str
    weight: float
    location_type: str

class DeliveryResponse(BaseModel):
    ticket_id: str
    total_price: float
    status: str
    action_log: List[str]
    breakdown: dict

# Initialize database on application startup
async def startup():
    # Run blocking DB initialization in a thread to avoid blocking the event loop
    import asyncio
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, init_db)
    print("✅ Database initialized")
    print("🚀 DeliverGraph AI is ready!")
    print("📊 Web UI: http://localhost:8000")
    print("📖 API Docs: http://localhost:8000/docs")

# ============ WEB UI ROUTES ============

@api.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Main web interface"""
    return templates.TemplateResponse("index.html", {"request": request})

@api.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    """Dashboard showing all deliveries"""
    return templates.TemplateResponse("dashboard.html", {"request": request})

@api.get("/delivery/{ticket_id}", response_class=HTMLResponse)
async def delivery_details_page(request: Request, ticket_id: str):
    """Delivery details page"""
    return templates.TemplateResponse("details.html", {
        "request": request,
        "ticket_id": ticket_id
    })

# ============ API ROUTES ============

@api.post("/api/calculate-price", response_model=DeliveryResponse)
async def calculate_price(delivery_request: DeliveryRequest):
    """Calculate delivery price via API"""
    try:
        # Pass a Python dict to the workflow (not a JSON string). Using
        # Pydantic v2's `model_dump()` returns a dict suitable for the
        # workflow.invoke() call.
        payload = delivery_request.model_dump()
        result = workflow_app.invoke(payload)
        
        if result.get('error_message'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "error": "Validation Error",
                    "message": result['error_message'],
                    "ticket_id": result.get('ticket_id')
                }
            )
        
        breakdown = {
            "base_price": result.get('base_price', 0),
            "urgency_multiplier": result.get('urgency_multiplier', 1.0),
            "weight_surcharge": result.get('weight_surcharge', 0),
            "location_adjustment": result.get('location_adjustment', 0),
        }
        
        return DeliveryResponse(
            ticket_id=result['ticket_id'],
            total_price=result['total_price'],
            status='completed',
            action_log=result['action_log'],
            breakdown=breakdown
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "Internal Server Error", "message": str(e)}
        )

@api.get("/api/delivery/{ticket_id}")
async def get_delivery_details(ticket_id: str):
    """Get delivery details by ticket ID"""
    db = SessionLocal()
    try:
        delivery = get_delivery(db, ticket_id)
        
        if not delivery:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Delivery with ticket {ticket_id} not found"
            )
        
        return {
            "ticket_id": delivery.ticket_id,
            "user_id": delivery.user_id,
            "material_type": delivery.material_type,
            "distance": delivery.distance,
            "urgency": delivery.urgency,
            "weight": delivery.weight,
            "location_type": delivery.location_type,
            "total_price": delivery.total_price,
            "status": delivery.status,
            "action_log": delivery.action_log,
            "created_at": delivery.created_at.isoformat()
        }
    finally:
        db.close()

@api.get("/api/deliveries")
async def get_deliveries(limit: int = 50):
    """Get all deliveries"""
    db = SessionLocal()
    try:
        deliveries = get_all_deliveries(db, limit)
        return [{
            "ticket_id": d.ticket_id,
            "user_id": d.user_id,
            "material_type": d.material_type,
            "distance": d.distance,
            "total_price": d.total_price,
            "status": d.status,
            "created_at": d.created_at.isoformat()
        } for d in deliveries]
    finally:
        db.close()

@api.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "DeliverGraph AI",
        "version": "1.0.0"
    }

if __name__ == "__main__":
    uvicorn.run(api, host="0.0.0.0", port=8000)