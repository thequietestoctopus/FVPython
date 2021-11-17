from rich import console
from rich.style import Style
from rich.console import Console


console = Console()
strike_text = Style(strike=True, color="blue", dim=True)
console.print("This text should be striked out", style=strike_text)
