import re

def validate_product_id(product_id):
    """Validate product ID format"""
    pattern = r'^[A-Z0-9]{3,20}$'
    return re.match(pattern, product_id) is not None

def validate_location_id(location_id):
    """Validate location ID format"""
    pattern = r'^[A-Z0-9]{3,20}$'
    return re.match(pattern, location_id) is not None

def validate_movement_id(movement_id):
    """Validate movement ID format"""
    pattern = r'^MOV[A-Z0-9]{3,10}$'
    return re.match(pattern, movement_id) is not None

def validate_quantity(quantity):
    """Validate quantity is positive integer"""
    try:
        qty = int(quantity)
        return qty > 0
    except (ValueError, TypeError):
        return False

def validate_capacity(capacity):
    """Validate capacity is positive integer"""
    try:
        cap = int(capacity)
        return cap > 0
    except (ValueError, TypeError):
        return False

def validate_text_input(text, min_length=1, max_length=255):
    """Validate text input length"""
    if not text or not isinstance(text, str):
        return False
    return min_length <= len(text.strip()) <= max_length

def validate_phone_number(phone):
    """Validate phone number format"""
    pattern = r'^\+?1?\d{9,15}$'
    return re.match(pattern, phone) is not None