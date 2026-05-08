class ValidationError(Exception):
    pass

def validate_symbol(symbol: str) -> str:
    symbol = symbol.upper().strip()
    if not symbol.isalnum():
        raise ValidationError(f"Invalid symbol format: {symbol}. Must be alphanumeric.")
    return symbol

def validate_side(side: str) -> str:
    side = side.upper().strip()
    if side not in ["BUY", "SELL"]:
        raise ValidationError(f"Invalid side: {side}. Must be BUY or SELL.")
    return side

def validate_order_type(order_type: str) -> str:
    order_type = order_type.upper().strip()
    if order_type not in ["MARKET", "LIMIT", "STOP_MARKET"]:
        raise ValidationError(f"Invalid order type: {order_type}. Must be MARKET, LIMIT, or STOP_MARKET.")
    return order_type

def validate_quantity(quantity: float) -> float:
    try:
        quantity = float(quantity)
    except ValueError:
        raise ValidationError(f"Invalid quantity: {quantity}. Must be a valid number.")
    if quantity <= 0:
        raise ValidationError("Quantity must be greater than zero.")
    return quantity

def validate_price(price: float) -> float:
    try:
        price = float(price)
    except ValueError:
        raise ValidationError(f"Invalid price: {price}. Must be a valid number.")
    if price <= 0:
        raise ValidationError("Price must be greater than zero.")
    return price
