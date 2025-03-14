"""
Test script to verify admin dashboard functionality
"""
from database.db_config import SessionLocal, Business, BusinessIntent, BotConfig
from admin.models import AdminUser, ChatbotLog


def test_dashboard_data():
    """Simulate the dashboard function from admin/routes.py"""
    db = SessionLocal()

    try:
        # Get counts for dashboard stats
        business_count = db.query(Business).count()
        intent_count = db.query(BusinessIntent).count()
        user_count = db.query(AdminUser).count()

        # Get recent logs
        logs = db.query(ChatbotLog).order_by(ChatbotLog.id.desc()).limit(10).all()

        print(f"Business count: {business_count}")
        print(f"Intent count: {intent_count}")
        print(f"User count: {user_count}")
        print(f"Recent logs: {len(logs)} items")

        # Try to access properties that might be causing the error
        print("\nTesting access to business data:")
        businesses = db.query(Business).all()
        for business in businesses:
            print(f"Business: {business.name}, Type: {business.business_type}")

        print("\nTesting access to intent data:")
        intents = db.query(BusinessIntent).all()
        for intent in intents:
            print(f"Intent: {intent.intent_name}, Business Type: {intent.business_type}")

    except Exception as e:
        print(f"Error accessing dashboard data: {str(e)}")
    finally:
        db.close()


if __name__ == "__main__":
    test_dashboard_data()