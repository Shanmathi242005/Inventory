    from datetime import datetime
import re

def generate_id(prefix, length=6):
    """Generate a unique ID with given prefix"""
    import uuid
    return f"{prefix}{str(uuid.uuid4())[:length].upper()}"

def format_timestamp(timestamp):
    """Format timestamp to readable format"""
    if isinstance(timestamp, str):
        return timestamp
    return timestamp.strftime('%Y-%m-%d %H:%M:%S')

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def format_currency(amount):
    """Format amount as currency"""
    return f"${amount:,.2f}"

def get_current_datetime():
    """Get current datetime in ISO format"""
    return datetime.now().isoformat()

def calculate_age(birth_date):
    """Calculate age from birth date"""
    from datetime import date
    today = date.today()
    return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))