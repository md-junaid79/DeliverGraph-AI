# src/api/notifications.py
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os

class NotificationService:
    def __init__(self):
        # SendGrid Email setup
        self.sendgrid_client = None
        if os.getenv('SENDGRID_API_KEY'):
            try:
                self.sendgrid_client = SendGridAPIClient(os.getenv('SENDGRID_API_KEY'))
                self.from_email = os.getenv('SENDGRID_FROM_EMAIL', 'noreply@delivergraph.ai')
            except Exception as e:
                print(f"⚠️ SendGrid initialization failed: {e}")
    
    def send_email(self, to_email: str, subject: str, content: str) -> dict:
        """
        Send Email via SendGrid
        Returns: {"status": "success"/"error", "message": str}
        """
        if not self.sendgrid_client:
            return {
                "status": "skipped", 
                "message": "SendGrid not configured"
            }
        
        try:
            message = Mail(
                from_email=self.from_email,
                to_emails=to_email,
                subject=subject,
                html_content=content
            )
            response = self.sendgrid_client.send(message)
            return {
                "status": "success", 
                "status_code": response.status_code,
                "message": "Email sent successfully"
            }
        except Exception as e:
            return {
                "status": "error", 
                "message": f"Email failed: {str(e)}"
            }
    
    def send_price_quote_email(self, email: str, ticket_id: str, total_price: float, 
                               breakdown: dict) -> dict:
        """
        Send detailed price quote email
        """
        subject = f"Delivery Quote #{ticket_id}"
        
        content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                           color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
                .price {{ font-size: 36px; font-weight: bold; color: #667eea; text-align: center; margin: 20px 0; }}
                .breakdown {{ background: white; padding: 20px; border-radius: 8px; margin: 20px 0; }}
                .breakdown-item {{ display: flex; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid #eee; }}
                .footer {{ text-align: center; color: #999; margin-top: 30px; font-size: 14px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🚚 DeliverGraph AI</h1>
                    <p>Your Delivery Quote is Ready!</p>
                </div>
                <div class="content">
                    <p><strong>Ticket ID:</strong> {ticket_id}</p>
                    <div class="price">₹{total_price:.2f}</div>
                    
                    <div class="breakdown">
                        <h3>Price Breakdown</h3>
                        <div class="breakdown-item">
                            <span>Base Price:</span>
                            <span>₹{breakdown.get('base_price', 0):.2f}</span>
                        </div>
                        <div class="breakdown-item">
                            <span>Urgency Multiplier:</span>
                            <span>{breakdown.get('urgency_multiplier', 1.0)}x</span>
                        </div>
                        <div class="breakdown-item">
                            <span>Weight Surcharge:</span>
                            <span>₹{breakdown.get('weight_surcharge', 0):.2f}</span>
                        </div>
                        <div class="breakdown-item">
                            <span>Location Adjustment:</span>
                            <span>₹{breakdown.get('location_adjustment', 0):.2f}</span>
                        </div>
                    </div>
                    
                    <p style="text-align: center; margin-top: 30px;">
                        <a href="http://localhost:8000/delivery/{ticket_id}" 
                           style="background: #667eea; color: white; padding: 12px 30px; 
                                  text-decoration: none; border-radius: 5px; display: inline-block;">
                            View Details
                        </a>
                    </p>
                </div>
                <div class="footer">
                    <p>Thank you for using DeliverGraph AI!</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return self.send_email(email, subject, content)