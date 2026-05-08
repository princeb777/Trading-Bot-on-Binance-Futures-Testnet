import os
from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceRequestException, BinanceOrderException
from dotenv import load_dotenv
from .logging_config import logger

load_dotenv()

API_KEY = os.getenv("BINANCE_API_KEY")
API_SECRET = os.getenv("BINANCE_API_SECRET")

_client_instance = None

def get_client() -> Client:
    global _client_instance
    if _client_instance is None:
        if not API_KEY or not API_SECRET:
            logger.error("API keys are not set in the environment variables.")
            raise ValueError("BINANCE_API_KEY and BINANCE_API_SECRET must be set.")
        
        try:
            logger.info("Initializing Binance testnet client...")
            _client_instance = Client(API_KEY, API_SECRET, testnet=True)
            # A simple ping to check if connection is successful
            _client_instance.ping()
            logger.info("Binance client initialized successfully.")
        except Exception as e:
            logger.error(f"Failed to initialize Binance client: {e}")
            raise
    return _client_instance
