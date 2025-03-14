"""
Minimal Flask app to test admin dashboard
"""
from flask import Flask, render_template
from database.db_config import SessionLocal, Business, BusinessIntent
from admin.models import AdminUser, ChatbotLog

app = Flask(__name__)


@app.route('/')
def dashboard():
    """Minimal dashboard view for testing"""
    try:
        db = SessionLocal()

        # Get counts for dashboard stats
        business_count = db.query(Business).count()
        intent_count = db.query(BusinessIntent).count()
        user_count = db.query(AdminUser).count()

        # Get recent logs
        logs = db.query(ChatbotLog).order_by(ChatbotLog.id.desc()).limit(10).all()

        db.close()

        # Just return some basic HTML instead of a template
        return f"""
        <html>
        <head><title>Dashboard Test</title></head>
        <body>
            <h1>Dashboard Test</h1>
            <p>Business count: {business_count}</p>
            <p>Intent count: {intent_count}</p>
            <p>User count: {user_count}</p>
            <p>Recent logs: {len(logs)} items</p>
        </body>
        </html>
        """
    except Exception as e:
        return f"Error: {str(e)}"


if __name__ == '__main__':
    app.run(debug=True, port=5001)