import sys
import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from bot.validators import (
    validate_symbol, validate_side, validate_order_type, 
    validate_quantity, validate_price, ValidationError
)
from bot.orders import place_order
from bot.logging_config import logger

console = Console()

@click.group()
def cli():
    """Binance Futures Testnet Trading Bot CLI."""
    pass

@cli.command()
@click.option('--symbol', required=True, help='Trading pair symbol (e.g., BTCUSDT)')
@click.option('--side', required=True, type=click.Choice(['BUY', 'SELL'], case_sensitive=False), help='Order side: BUY or SELL')
@click.option('--type', 'order_type', required=True, type=click.Choice(['MARKET', 'LIMIT', 'STOP_MARKET'], case_sensitive=False), help='Order type')
@click.option('--quantity', required=True, type=float, help='Order quantity')
@click.option('--price', type=float, help='Order price (required for LIMIT orders)')
@click.option('--stop-price', type=float, help='Stop price (required for STOP_MARKET orders)')
def place(symbol: str, side: str, order_type: str, quantity: float, price: float = None, stop_price: float = None):
    """Place an order on Binance Futures Testnet."""
    try:
        # Validate inputs
        valid_symbol = validate_symbol(symbol)
        valid_side = validate_side(side)
        valid_order_type = validate_order_type(order_type)
        valid_quantity = validate_quantity(quantity)
        
        valid_price = validate_price(price) if price is not None else None
        valid_stop_price = validate_price(stop_price) if stop_price is not None else None

        if valid_order_type == "LIMIT" and valid_price is None:
            raise ValidationError("Price is required for LIMIT orders.")
        
        if valid_order_type == "STOP_MARKET" and valid_stop_price is None:
            raise ValidationError("Stop price is required for STOP_MARKET orders.")

        # Show order summary before placing
        summary_table = Table(title="Order Request Summary", show_header=True, header_style="bold magenta")
        summary_table.add_column("Parameter", style="cyan")
        summary_table.add_column("Value", style="green")
        
        summary_table.add_row("Symbol", valid_symbol)
        summary_table.add_row("Side", valid_side)
        summary_table.add_row("Type", valid_order_type)
        summary_table.add_row("Quantity", str(valid_quantity))
        
        if valid_price:
            summary_table.add_row("Price", str(valid_price))
        if valid_stop_price:
            summary_table.add_row("Stop Price", str(valid_stop_price))
            
        console.print(summary_table)
        console.print("[bold yellow]Placing order...[/bold yellow]")

        # Place the order
        response = place_order(
            symbol=valid_symbol,
            side=valid_side,
            order_type=valid_order_type,
            quantity=valid_quantity,
            price=valid_price,
            stop_price=valid_stop_price
        )

        # Show response details
        response_table = Table(title="Order Response Details", show_header=True, header_style="bold blue")
        response_table.add_column("Field", style="cyan")
        response_table.add_column("Value", style="green")
        
        fields_to_show = ["orderId", "status", "executedQty", "avgPrice", "clientOrderId"]
        for field in fields_to_show:
            if field in response:
                response_table.add_row(field, str(response[field]))
        
        console.print(response_table)
        console.print(Panel("[bold green]Order placed successfully![/bold green]", expand=False))

    except ValidationError as e:
        console.print(f"[bold red]Validation Error:[/bold red] {e}")
        logger.warning(f"Validation Error: {e}")
        sys.exit(1)
    except Exception as e:
        console.print(f"[bold red]Failed to place order:[/bold red] {e}")
        console.print("Check the logs for more details.")
        sys.exit(1)

if __name__ == '__main__':
    cli()
