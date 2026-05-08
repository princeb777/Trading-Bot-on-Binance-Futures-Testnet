from typing import Dict, Any, Optional
from binance.exceptions import BinanceAPIException, BinanceRequestException, BinanceOrderException
from .client import get_client
from .logging_config import logger

def place_order(
    symbol: str, 
    side: str, 
    order_type: str, 
    quantity: float, 
    price: Optional[float] = None,
    stop_price: Optional[float] = None
) -> Dict[str, Any]:
    """Places an order on Binance Futures Testnet."""
    client = get_client()
    
    order_params = {
        "symbol": symbol,
        "side": side,
        "type": order_type,
        "quantity": quantity,
    }
    
    if order_type == "LIMIT":
        if not price:
            raise ValueError("Price is required for LIMIT orders.")
        order_params["price"] = price
        order_params["timeInForce"] = "GTC"
    
    elif order_type == "STOP_MARKET":
        if not stop_price:
            raise ValueError("Stop price is required for STOP_MARKET orders.")
        order_params["stopPrice"] = stop_price

    logger.info(f"Placing {order_type} order: {order_params}")
    
    try:
        response = client.futures_create_order(**order_params)
        logger.info(f"Order placed successfully. Response: {response}")
        return response
    
    except BinanceAPIException as e:
        logger.error(f"Binance API Exception: Status Code {e.status_code}, Message: {e.message}")
        raise
    except BinanceOrderException as e:
        logger.error(f"Binance Order Exception: {e}")
        raise
    except BinanceRequestException as e:
        logger.error(f"Binance Request Exception: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error while placing order: {e}")
        raise
