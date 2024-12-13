import sys
import os
import pygame
import random
import traceback
from rich.console import Console
from rich.table import Table

# Add the project root to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from src.universe import UniverseGenerator
from src.player import Player
from src.economy import EconomySimulator
from src.events import EventGenerator
from src.technologies import TechnologyTree

class CargoHauler:
    def __init__(self, difficulty=2):
        pygame.init()
        self.console = Console()
        self.difficulty = difficulty
        
        # Initialize game systems
        self.universe = UniverseGenerator(difficulty)
        self.player = Player()
        self.economy = EconomySimulator(self.universe.planets)
        self.event_generator = EventGenerator()
        self.tech_tree = TechnologyTree()
        
        # Game state
        self.current_planet = None
        self.game_over = False
        
    def start_game(self):
        self.console.print("[bold green]Welcome to Cargo Hauler![/bold green]")
        self.current_planet = random.choice(self.universe.planets)
        try:
            self.main_game_loop()
        except Exception as e:
            self.console.print("[bold red]An error occurred:[/bold red]")
            self.console.print(f"[red]{traceback.format_exc()}[/red]")
    
    def main_game_loop(self):
        while not self.game_over:
            try:
                self.display_status()
                self.player_turn()
            except KeyboardInterrupt:
                self.console.print("\n[yellow]Game interrupted. Exiting...[/yellow]")
                break
            except Exception as e:
                self.console.print(f"[red]Error in game loop: {e}[/red]")
                break
        
        self.console.print("[bold yellow]Thanks for playing Cargo Hauler![/bold yellow]")
    
    def display_status(self):
        try:
            table = Table(title="Current Status")
            table.add_column("Attribute", style="cyan")
            table.add_column("Value", style="magenta")
            
            table.add_row("Current Planet", self.current_planet.name)
            table.add_row("Credits", str(self.player.credits))
            table.add_row("Cargo Space", f"{self.player.cargo_used}/{self.player.cargo_capacity}")
            
            self.console.print(table)
        except Exception as e:
            self.console.print(f"[red]Error displaying status: {e}[/red]")
    
    def player_turn(self):
        try:
            actions = [
                "Trade Goods",
                "Travel to New Planet",
                "Check Market Prices",
                "Upgrade Ship",
                "View Technologies",
                "Quit Game"
            ]
            
            self.console.print("\nChoose an action:")
            for i, action in enumerate(actions, 1):
                self.console.print(f"{i}. {action}")
            
            choice = self.console.input("[bold yellow]Enter your choice: [/bold yellow]")
            
            try:
                choice = int(choice)
                if choice == 1:
                    self.trade_goods()
                elif choice == 2:
                    self.travel_to_new_planet()
                elif choice == 3:
                    self.check_market_prices()
                elif choice == 4:
                    self.upgrade_ship()
                elif choice == 5:
                    self.view_technologies()
                elif choice == 6:
                    self.game_over = True
                else:
                    self.console.print("[bold red]Invalid choice![/bold red]")
            except ValueError:
                self.console.print("[bold red]Please enter a number![/bold red]")
        except Exception as e:
            self.console.print(f"[red]Error in player turn: {e}[/red]")
    
    def trade_goods(self):
        try:
            self.console.print(f"[bold]Trading at {self.current_planet.name}[/bold]")
            
            # Ensure commodities exist before trying to access them
            if not hasattr(self.economy, 'commodities') or not self.economy.commodities:
                self.console.print("[red]No commodities available for trading.[/red]")
                return
            
            # Get available commodities from the economy
            available_commodities = list(self.economy.commodities.keys())
            
            if not available_commodities:
                self.console.print("[red]No commodities available for trading.[/red]")
                return
            
            # Display available commodities and their prices
            self.console.print("\nAvailable Commodities:")
            commodity_prices = {}
            for i, commodity in enumerate(available_commodities, 1):
                try:
                    # Safely calculate price
                    price = self.economy.calculate_price(commodity, self.current_planet)
                    commodity_prices[i] = {
                        'name': commodity, 
                        'price': price
                    }
                    self.console.print(f"{i}. {commodity}: {price:.2f} credits")
                except Exception as price_error:
                    self.console.print(f"[red]Error calculating price for {commodity}: {price_error}[/red]")
            
            # Prompt for commodity selection
            commodity_choice = self.console.input("[yellow]Enter the number of the commodity to trade (or 0 to cancel): [/yellow]")
            
            try:
                commodity_index = int(commodity_choice)
                
                if commodity_index == 0:
                    return  # User chose to cancel
                
                if commodity_index not in commodity_prices:
                    self.console.print("[red]Invalid commodity selection.[/red]")
                    return
                
                # Get selected commodity details
                selected_commodity = commodity_prices[commodity_index]['name']
                price = commodity_prices[commodity_index]['price']
                
                # Buying or selling prompt
                trade_type = self.console.input("[yellow]Do you want to (B)uy or (S)ell? [/yellow]").lower()
                
                if trade_type in ['b', 'buy']:
                    # Buying logic
                    max_quantity = min(
                        self.player.cargo_capacity - self.player.cargo_used, 
                        int(self.player.credits / price)
                    )
                    
                    quantity_str = self.console.input(f"[yellow]How many {selected_commodity} do you want to buy? (Max: {max_quantity}): [/yellow]")
                    
                    try:
                        quantity = int(quantity_str)
                        
                        if 0 < quantity <= max_quantity:
                            total_cost = quantity * price
                            
                            # Perform the purchase
                            if self.player.add_cargo(selected_commodity, quantity, price):
                                self.console.print(f"[green]Bought {quantity} {selected_commodity} for {total_cost:.2f} credits[/green]")
                            else:
                                self.console.print("[red]Purchase failed. Check your cargo space or credits.[/red]")
                        else:
                            self.console.print("[red]Invalid quantity.[/red]")
                    
                    except ValueError:
                        self.console.print("[red]Please enter a valid number.[/red]")
                
                elif trade_type in ['s', 'sell']:
                    # Selling logic
                    if selected_commodity not in self.player.cargo:
                        self.console.print(f"[red]You don't have any {selected_commodity} to sell.[/red]")
                        return
                    
                    # Get available quantity safely
                    available_quantity = self.player.cargo.get(selected_commodity, {}).get('quantity', 0)
                    
                    quantity_str = self.console.input(f"[yellow]How many {selected_commodity} do you want to sell? (Max: {available_quantity}): [/yellow]")
                    
                    try:
                        quantity = int(quantity_str)
                        
                        if 0 < quantity <= available_quantity:
                            total_revenue = quantity * price
                            
                            # Perform the sale
                            if self.player.sell_cargo(selected_commodity, quantity, price):
                                self.console.print(f"[green]Sold {quantity} {selected_commodity} for {total_revenue:.2f} credits[/green]")
                            else:
                                self.console.print("[red]Sale failed.[/red]")
                        else:
                            self.console.print("[red]Invalid quantity.[/red]")
                    
                    except ValueError:
                        self.console.print("[red]Please enter a valid number.[/red]")
                
                else:
                    self.console.print("[red]Invalid trade type. Choose Buy or Sell.[/red]")
            
            except ValueError:
                self.console.print("[red]Please enter a valid number.[/red]")
        
        except Exception as e:
            self.console.print(f"[red]Error in trading: {e}[/red]")
            import traceback
            traceback.print_exc()

    def travel_to_new_planet(self):
        possible_planets = [p for p in self.universe.planets if p != self.current_planet]
        if possible_planets:
            new_planet = random.choice(possible_planets)
            self.current_planet = new_planet
            self.console.print(f"Traveled to {new_planet.name}")
        else:
            self.console.print("No other planets to travel to")
    
    def check_market_prices(self):
        market_overview = self.economy.get_market_overview()
        self.console.print(market_overview)
    
    def upgrade_ship(self):
        available_upgrades = self.tech_tree.get_available_upgrades()
        self.console.print("Available Upgrades:")
        for category, upgrades in available_upgrades.items():
            self.console.print(f"\n{category}:")
            for upgrade in upgrades:
                self.console.print(f"- {upgrade['name']} (Cost: {upgrade['cost']} credits)")
    
    def view_technologies(self):
        self.console.print("Current Technologies:")
        for category, techs in self.tech_tree.technologies.items():
            self.console.print(f"\n{category}:")
            for tech_name, tech_info in techs.items():
                self.console.print(f"- {tech_name} (Level {tech_info['level']})")

def main():
    try:
        game = CargoHauler(difficulty=2)
        game.start_game()
    except Exception as e:
        print(f"Error starting the game: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    main()