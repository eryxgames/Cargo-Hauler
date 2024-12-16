import sys
import os
import pygame
import random
import traceback
from rich.console import Console
from rich.table import Table
from rich.progress import Progress
import time
import json  # Ensure json is imported

# Add the project root to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from src.universe import UniverseGenerator, Planet  # Import Planet class
from src.player import Player
from src.economy import EconomySimulator
from src.events import EventGenerator
from src.technologies import TechnologyTree
from src.storyline import Storyline

class CargoHauler:
    def __init__(self, difficulty=2):
        pygame.init()
        self.console = Console()
        self.difficulty = difficulty

        # Initialize game systems
        self.universe = UniverseGenerator(difficulty)
        self.player = Player(self.console)
        self.economy = EconomySimulator(self.universe.planets)
        self.event_generator = EventGenerator()
        self.tech_tree = TechnologyTree()
        self.storyline = Storyline()

        # Game state
        self.current_planet = None
        self.game_over = False
        self.status_changed = True

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
                self.generate_random_quest()  # Ensure quests are generated at the start of each turn
                self.player_turn()
            except KeyboardInterrupt:
                self.console.print("\n[yellow]Game interrupted. Exiting...[/yellow]")
                break
            except Exception as e:
                self.console.print(f"[red]Error in game loop: {e}[/red]")
                break

        self.console.print("[bold yellow]Thanks for playing Cargo Hauler![/bold yellow]")

    def display_status(self):
        if self.status_changed:
            try:
                table = Table(title="Current Status")
                table.add_column("Attribute", style="cyan")
                table.add_column("Value", style="magenta")

                table.add_row("Current Planet", self.current_planet.name)
                table.add_row("Credits", f"{self.player.credits:.1f}")
                table.add_row("Cargo Space", f"{self.player.cargo_used}/{self.player.cargo_capacity}")
                table.add_row("Fuel Level", f"{self.player.fuel_level:.1f}/{self.player.fuel_tank_capacity}")

                self.console.print(table)
                self.status_changed = False
            except Exception as e:
                self.console.print(f"[red]Error displaying status: {e}[/red]")

    def player_turn(self):
        try:
            actions = [
                "Cargo Market",
                "Travel to New Planet",
                "Upgrade Ship",
                "View Technologies",
                "View Storyline",
                "View Trade Statistics",
                "Scan Spaceport",
                "Customize Ship",
                "Save Game",
                "Load Game",
                "Quit Game"
            ]

            self.console.print("\nChoose an action:")
            for i, action in enumerate(actions, 1):
                self.console.print(f"{i}. {action}")

            choice = self.console.input("[bold yellow]Enter your choice: [/bold yellow]")

            try:
                choice = int(choice)
                if choice == 1:
                    self.cargo_market()
                elif choice == 2:
                    self.travel_menu()
                elif choice == 3:
                    self.upgrade_ship()
                elif choice == 4:
                    self.view_technologies()
                elif choice == 5:
                    self.view_storyline()
                elif choice == 6:
                    self.view_trade_statistics()
                elif choice == 7:
                    self.scan_spaceport()
                elif choice == 8:
                    self.customize_ship()
                elif choice == 9:
                    self.save_game('savegame.json')
                elif choice == 10:
                    self.load_game('savegame.json')
                elif choice == 11:
                    self.game_over = True
                else:
                    self.console.print("[bold red]Invalid choice![/bold red]")
            except ValueError:
                self.console.print("[bold red]Please enter a number![/bold red]")
        except Exception as e:
            self.console.print(f"[red]Error in player turn: {e}[/red]")

    def cargo_market(self):
        self.check_market_prices()
        self.trade_goods()

    def check_market_prices(self):
        market_overview = self.economy.get_market_overview()
        table = Table(title="Market Prices Overview")
        table.add_column("Planet", style="cyan")
        for commodity in self.economy.commodities:
            table.add_column(commodity, style="green")

        for index, row in market_overview.iterrows():
            row_style = "blue" if row['Planet'] == self.current_planet.name else "default"
            table.add_row(row['Planet'], *[f"{row[commodity]:.1f}" for commodity in self.economy.commodities], style=row_style)

        self.console.print(table)

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
                    self.console.print(f"{i}. {commodity}: {price:.1f} credits")
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
                                self.console.print(f"[green]Bought {quantity} {selected_commodity} for {total_cost:.1f} credits[/green]")
                                self.status_changed = True
                            else:
                                self.console.print("[red]Purchase failed. Check your cargo space or credits.[/red]")
                        else:
                            self.console.print("[red]Invalid quantity.[/red]")

                    except ValueError:
                        self.console.print("[red]Please enter a valid number.[/red]")

                elif trade_type in ['s', 'sell']:
                    # Selling logic
                    if selected_commodity not in self.player.inventory:
                        self.console.print(f"[red]You don't have any {selected_commodity} to sell.[/red]")
                        return

                    # Get available quantity safely
                    available_quantity = self.player.inventory.get(selected_commodity, {}).get('quantity', 0)

                    quantity_str = self.console.input(f"[yellow]How many {selected_commodity} do you want to sell? (Max: {available_quantity}): [/yellow]")

                    try:
                        quantity = int(quantity_str)

                        if 0 < quantity <= available_quantity:
                            total_revenue = quantity * price

                            # Perform the sale
                            if self.player.sell_cargo(selected_commodity, quantity, price):
                                self.console.print(f"[green]Sold {quantity} {selected_commodity} for {total_revenue:.1f} credits[/green]")
                                self.status_changed = True
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

    def travel_menu(self):
        try:
            self.console.print("\nChoose a travel option:")
            travel_options = [
                "Select Destination",
                "Quantum Drive",
                "Set Up Trade Route",
                "Frontier Jump"
            ]
            if self.player.trade_route:
                start_planet, target_planet = self.player.trade_route
                travel_options.append(f"Use Trade Route ({start_planet.name} → {target_planet.name})")

            for i, option in enumerate(travel_options, 1):
                self.console.print(f"{i}. {option}")

            travel_choice = self.console.input("[bold yellow]Enter your choice: [/bold yellow]")

            try:
                travel_choice = int(travel_choice)
                if travel_choice == 1:
                    self.select_destination()
                elif travel_choice == 2:
                    self.quantum_drive()
                elif travel_choice == 3:
                    self.set_up_trade_route()
                elif travel_choice == 4:
                    self.frontier_jump()
                elif travel_choice == 5 and self.player.trade_route:
                    self.use_trade_route()
                else:
                    self.console.print("[bold red]Invalid choice![/bold red]")
            except ValueError:
                self.console.print("[bold red]Please enter a number![/bold red]")
        except Exception as e:
            self.console.print(f"[red]Error in travel menu: {e}[/red]")

    def select_destination(self):
        self.console.print("\nSelect a destination:")
        for i, planet in enumerate(self.universe.planets, 1):
            self.console.print(f"{i}. {planet.name}")

        choice = self.console.input("[bold yellow]Enter the number of the planet: [/bold yellow]")
        try:
            choice = int(choice)
            if 1 <= choice <= len(self.universe.planets):
                new_planet = self.universe.planets[choice - 1]
                if new_planet != self.current_planet:
                    self.travel_to_planet(new_planet)
                else:
                    self.console.print("[bold red]You are already at this planet![/bold red]")
            else:
                self.console.print("[bold red]Invalid choice![/bold red]")
        except ValueError:
            self.console.print("[bold red]Please enter a number![/bold red]")

    def quantum_drive(self):
        new_planet = random.choice(self.universe.planets)
        if new_planet != self.current_planet:
            self.travel_to_planet(new_planet)
        else:
            self.console.print("[bold red]You are already at this planet![/bold red]")

    def set_up_trade_route(self):
        self.console.print("\nSet up a trade route:")
        self.console.print("Select a starting planet:")
        for i, planet in enumerate(self.universe.planets, 1):
            self.console.print(f"{i}. {planet.name}")

        start_choice = self.console.input("[bold yellow]Enter the number of the starting planet: [/bold yellow]")
        try:
            start_choice = int(start_choice)
            if 1 <= start_choice <= len(self.universe.planets):
                start_planet = self.universe.planets[start_choice - 1]
                self.console.print("Select a target planet:")
                for i, planet in enumerate(self.universe.planets, 1):
                    self.console.print(f"{i}. {planet.name}")

                target_choice = self.console.input("[bold yellow]Enter the number of the target planet: [/bold yellow]")
                try:
                    target_choice = int(target_choice)
                    if 1 <= target_choice <= len(self.universe.planets):
                        target_planet = self.universe.planets[target_choice - 1]
                        self.player.trade_route = [start_planet, target_planet]
                        self.console.print(f"Trade route set from {start_planet.name} to {target_planet.name}")
                    else:
                        self.console.print("[bold red]Invalid choice![/bold red]")
                except ValueError:
                    self.console.print("[bold red]Please enter a number![/bold red]")
            else:
                self.console.print("[bold red]Invalid choice![/bold red]")
        except ValueError:
            self.console.print("[bold red]Please enter a number![/bold red]")

    def use_trade_route(self):
        if not self.player.trade_route:
            self.console.print("[bold red]No trade route set![/bold red]")
            return

        start_planet, target_planet = self.player.trade_route
        if self.current_planet != start_planet:
            self.console.print("[bold red]You are not at the start planet of this trade route![/bold red]")
            return

        if target_planet == self.current_planet:
            self.console.print("[bold red]You are already at this planet![/bold red]")
            return

        self.travel_to_planet(target_planet)

    def frontier_jump(self):
        frontier_planet_names = [
            "Frontier Asteroid Belt",
            "Frontier Base",
            "Frontier Outpost",
            "Frontier Colony"
        ]
        frontier_planet_name = random.choice(frontier_planet_names)
        frontier_planet = Planet(
            name=frontier_planet_name,
            planet_type="Frontier",
            economy_level=random.uniform(0.3, 1.0),
            resources=self.universe.generate_resources(),
            status="Stable",
            characteristics="Neutral",
            demographics={
                "Population": random.randint(1000, 10000),
                "Cyborgs": random.randint(1, 100),
                "Androids": random.randint(1, 100),
                "Robots": random.randint(1, 100)
            },
            planet_class="Asteroid Belt",
            moons=0,
            geology="Rocky",
            climate="Harsh",
            history=self.universe.generate_history(frontier_planet_name, "Frontier", "Stable", "Neutral", {"Population": random.randint(1000, 10000), "Cyborgs": random.randint(1, 100), "Androids": random.randint(1, 100), "Robots": random.randint(1, 100)}, "Asteroid Belt", 0, "Rocky", "Harsh")
        )
        self.universe.planets.append(frontier_planet)
        self.travel_to_planet(frontier_planet)

    def travel_to_planet(self, planet):
        distance = self.calculate_distance(self.current_planet, planet)
        fuel_consumption = distance * self.player.ship_fuel_efficiency
        if self.player.fuel_level >= fuel_consumption:
            self.player.fuel_level = round(self.player.fuel_level - fuel_consumption, 1)
            self.player.total_fuel_used = round(self.player.total_fuel_used + fuel_consumption, 1)
            self.player.total_trips += 1
            self.current_planet = planet
            self.console.print(f"Traveled to {planet.name} using {fuel_consumption:.1f} units of fuel.")
            self.generate_random_quest()  # Generate new quests when traveling
            self.handle_event(self.event_generator.generate_event())
            self.end_turn()
        else:
            self.console.print("[bold red]Not enough fuel to travel![/bold red]")

    def handle_event(self, event):
        event_type = event['type']
        description = event['description']
        self.console.print(f"[bold yellow]Event:[/bold yellow] {description}")

        if event_type == 'trade_opportunity':
            # Implement trade opportunity logic
            commodity = random.choice(list(self.economy.commodities.keys()))
            price = self.economy.calculate_price(commodity, self.current_planet)
            quantity = random.randint(10, 50)
            self.player.add_cargo(commodity, quantity, price)
            self.console.print(f"You discovered a rare trade opportunity and acquired {quantity} units of {commodity} at {price} credits each.")

        elif event_type == 'pirate_encounter':
            # Implement pirate encounter logic
            loss = random.uniform(0.1, 0.3) * self.player.credits
            self.player.credits -= loss
            self.console.print(f"Pirates attacked! You lost {loss:.1f} credits.")

        elif event_type == 'market_crash':
            # Implement market crash logic
            for commodity in self.economy.commodities:
                self.economy.commodities[commodity]['base_price'] *= 0.5
            self.console.print("A sudden market crash has reduced commodity prices by 50%.")

        elif event_type == 'technological_breakthrough':
            # Implement technological breakthrough logic
            # For example, grant a free technology upgrade
            available_upgrades = self.tech_tree.get_available_upgrades()
            if available_upgrades:
                category = random.choice(list(available_upgrades.keys()))
                upgrade = random.choice(available_upgrades[category])
                self.apply_upgrade_effects(upgrade)
                self.console.print(f"You've made a technological breakthrough: {upgrade['name']} has been granted to you for free.")
            else:
                self.console.print("You've made a technological breakthrough, but no upgrades are available at this time.")

        elif event_type == 'fuel_shortage':
            # Implement fuel shortage logic
            self.player.fuel_level *= 0.5
            self.console.print("A fuel shortage has reduced your fuel level by 50%.")

        elif event_type == 'cargo_loss':
            # Implement cargo loss logic
            if self.player.inventory:
                commodity = random.choice(list(self.player.inventory.keys()))
                loss_quantity = random.randint(1, self.player.inventory[commodity]['quantity'])
                self.player.inventory[commodity]['quantity'] -= loss_quantity
                self.console.print(f"You lost {loss_quantity} units of {commodity} due to an accident.")
            else:
                self.console.print("You narrowly avoided cargo loss as you have no cargo on board.")    
    
    def calculate_distance(self, planet1, planet2):
        # Placeholder for actual distance calculation logic
        return random.uniform(1, 10)

    def end_turn(self):
        self.console.print("\n[bold yellow]End of turn.[/bold yellow]")
        self.status_changed = True
        self.player_turn()

    def upgrade_ship(self):
        available_upgrades = self.tech_tree.get_available_upgrades()
        if not available_upgrades:
            self.console.print("No available upgrades at this time.")
            return

        self.console.print("Available Upgrades:")
        upgrade_options = []
        for category, upgrades in available_upgrades.items():
            self.console.print(f"\n{category}:")
            for upgrade in upgrades:
                upgrade_options.append(upgrade)
                self.console.print(f"{len(upgrade_options)}. {upgrade['name']} (Cost: {upgrade['cost']:.1f} credits)")

        upgrade_choice = self.console.input("Enter the number of the upgrade to purchase (or 'cancel'): ")
        if upgrade_choice.lower() == 'cancel':
            return

        try:
            upgrade_index = int(upgrade_choice)
            if 1 <= upgrade_index <= len(upgrade_options):
                selected_upgrade = upgrade_options[upgrade_index - 1]
                if self.player.credits >= selected_upgrade['cost']:
                    self.player.credits -= selected_upgrade['cost']
                    # Apply upgrade effects
                    self.apply_upgrade_effects(selected_upgrade)
                    self.console.print(f"Purchased {selected_upgrade['name']} for {selected_upgrade['cost']:.1f} credits.")
                    self.status_changed = True
                else:
                    self.console.print("Insufficient credits to purchase this upgrade.")
            else:
                self.console.print("[bold red]Invalid choice![/bold red]")
        except ValueError:
            self.console.print("[bold red]Please enter a number![/bold red]")

    def apply_upgrade_effects(self, upgrade):
        category = upgrade['category']
        upgrade_name = upgrade['name']
        effects = upgrade['effects']

        if category == 'cargo':
            self.player.cargo_capacity = effects['cargo_capacity']
            self.console.print(f"Cargo capacity increased to {self.player.cargo_capacity}")
        elif category == 'ship_level':
            self.player.ship_level += 1
            self.console.print(f"Ship level increased to {self.player.ship_level}")
        elif category == 'fuel_efficiency':
            self.player.ship_fuel_efficiency = effects['fuel_efficiency']
            self.console.print(f"Fuel efficiency increased to {self.player.ship_fuel_efficiency}")
        elif category == 'life_support':
            self.player.life_support_expansion = effects['life_support_capacity']
            self.console.print(f"Life support capacity increased to {self.player.life_support_expansion}")
        elif category == 'passenger_pod':
            self.player.passenger_pod_capacity = effects['passenger_pod_capacity']
            self.console.print(f"Passenger pod capacity increased to {self.player.passenger_pod_capacity}")
        # Add other categories and effects as needed

    def view_technologies(self):
        self.console.print("Current Technologies:")
        for category, techs in self.tech_tree.technologies.items():
            self.console.print(f"\n{category}:")
            for tech_name, tech_info in techs.items():
                self.console.print(f"- {tech_name} (Level {tech_info['level']})")

    def view_storyline(self):
        storyline = self.get_storyline()
        if not storyline:
            self.console.print("No storyline available yet.")
            return
        self.console.print("Storyline:")
        for entry in storyline:
            self.display_storyline_entry(entry)

    def get_storyline(self):
        return self.storyline.get_story_up_to_level(self.player.level)

    def display_storyline_entry(self, entry):
        self.console.print(f"[bold yellow]Press any key to continue...[/bold yellow]")
        for char in entry:
            self.console.print(char, end='')
            time.sleep(0.05)  # Adjust the speed as needed
        self.console.input()

    def view_trade_statistics(self):
        self.console.print("Trade Statistics:")
        self.console.print(f"Total Profit: {self.player.total_profit:.1f} credits")
        self.console.print(f"Total Loss: {self.player.total_loss:.1f} credits")
        self.console.print(f"Total Spent: {self.player.total_spent:.1f} credits")
        self.console.print(f"Most Profitable Good: {self.player.most_profitable_good}")
        self.console.print(f"Most Profitable Trade Route: {self.player.most_profitable_route}")
        self.console.print(f"Total Fuel Used: {self.player.total_fuel_used:.1f} units")
        if self.player.total_trips > 0:
            self.console.print(f"Average Fuel Consumption per Trip: {self.player.total_fuel_used / self.player.total_trips:.1f} units")
        else:
            self.console.print(f"Average Fuel Consumption per Trip: 0.0 units")

        # Display a table of trade history
        table = Table(title="Trade History")
        table.add_column("Transaction ID", style="cyan")
        table.add_column("Good", style="magenta")
        table.add_column("Quantity", style="green")
        table.add_column("Price per Unit", style="yellow")
        table.add_column("Total", style="bold")

        for transaction in self.player.trade_history:
            table.add_row(
                str(transaction['id']),
                transaction['good'],
                str(transaction['quantity']),
                str(transaction['price_per_unit']),
                str(transaction['total'])
            )

        self.console.print(table)

    def scan_spaceport(self):
        self.console.print("Spaceport Information:")
        current_planet = self.current_planet
        table = Table(show_header=False, box=None)
        table.add_column()
        table.add_column()

        table.add_row("Name", current_planet.name)
        table.add_row("Type", current_planet.type)
        table.add_row("Fuel Price", f"{self.economy.calculate_price('fuel', current_planet):.1f} credits")
        resources_display = ", ".join([f"{r}: {v:.1f}" for r, v in current_planet.resources.items() if r != 'fuel'])
        table.add_row("Resources", resources_display)
        table.add_row("Status", current_planet.status)
        table.add_row("Characteristics", current_planet.characteristics)
        demographics_display = f"Population: {current_planet.demographics['Population']}, Cyborgs: {current_planet.demographics['Cyborgs']}, Androids: {current_planet.demographics['Androids']}, Robots: {current_planet.demographics['Robots']}"
        table.add_row("Demographics", demographics_display)
        description_display = f"Class: {current_planet.planet_class}, Moons: {current_planet.moons}, Geology: {current_planet.geology}, Climate: {current_planet.climate}"
        table.add_row("Description and Environment", description_display)
        table.add_row("History", current_planet.history)

        self.console.print(table)

        # Check for quest completion
        for quest in self.player.active_quests:
            if quest['conditions']['destination'] == current_planet.name:
                self.console.print(f"[bold green]Quest completed: {quest['description']}[/bold green]")
                self.player.complete_quest(quest)

        # Determine the number of quests to display based on the player's level
        if self.player.level <= 3:
            max_quests = 1
        elif self.player.level <= 10:
            max_quests = 2
        else:
            max_quests = 3

        # Ensure we only sample as many quests as are available
        available_quests = random.sample(self.universe.quests, min(max_quests, len(self.universe.quests)))

        # Add quest system
        self.console.print("\nAvailable Quests:")
        if not available_quests:
            self.console.print("No quests available at this time.")
        else:
            for i, quest in enumerate(available_quests, 1):
                self.console.print(f"{i}. {quest['description']}")
                self.console.print(f"   Backstory: {quest['backstory']}")

            quest_choice = self.console.input("[bold yellow]Enter the number of the quest to accept (or 'cancel'): [/bold yellow]")
            if quest_choice.lower() == 'cancel':
                return

            try:
                quest_index = int(quest_choice)
                if 1 <= quest_index <= len(available_quests):
                    selected_quest = available_quests[quest_index - 1]
                    self.player.accept_quest(selected_quest)
                    self.universe.quests.remove(selected_quest)
                    # Clear available quests after accepting a quest
                    self.universe.quests = []
                else:
                    self.console.print("[bold red]Invalid choice![/bold red]")
            except ValueError:
                self.console.print("[bold red]Please enter a number![/bold red]")

    def customize_ship(self):
        self.console.print("Ship Customization:")
        self.console.print("Allocate resources to different ship components:")
        components = [
            ("Cargo Capacity", 5000),
            ("Fuel Efficiency", 3000),
            ("Ship Speed", 2000),
            ("Life Support", 4000),
            ("Radiation Shield", 6000),
            ("Business Class Module", 8000)
        ]
        for i, (component, price) in enumerate(components, 1):
            self.console.print(f"{i}. {component} (Cost: {price:.1f} credits)")

        choice = self.console.input("[bold yellow]Enter the number of the component to upgrade: [/bold yellow]")

        try:
            choice = int(choice)
            if 1 <= choice <= len(components):
                component, price = components[choice - 1]
                if self.player.credits >= price:
                    self.player.credits -= price
                    if component == "Cargo Capacity":
                        self.player.cargo_capacity += 50
                        self.console.print(f"Cargo capacity increased to {self.player.cargo_capacity}")
                    elif component == "Fuel Efficiency":
                        self.player.ship_fuel_efficiency += 0.1
                        self.console.print(f"Fuel efficiency increased to {self.player.ship_fuel_efficiency}")
                    elif component == "Ship Speed":
                        self.player.ship_speed += 0.1
                        self.console.print(f"Ship speed increased to {self.player.ship_speed}")
                    elif component == "Life Support":
                        self.player.life_support_expansion += 10
                        self.console.print(f"Life support capacity increased to {self.player.life_support_expansion}")
                    elif component == "Radiation Shield":
                        self.player.radiation_shield = True
                        self.console.print("Radiation Shield installed.")
                    elif component == "Business Class Module":
                        self.player.business_class_module = True
                        self.console.print("Business Class Module installed.")
                else:
                    self.console.print("Insufficient credits to purchase this upgrade.")
            else:
                self.console.print("[bold red]Invalid choice![/bold red]")
        except ValueError:
            self.console.print("[bold red]Please enter a number![/bold red]")

    def save_game(self, filename):
        game_state = {
            'player': self.player.__dict__,
            'universe': {
                'planets': [planet.__dict__ for planet in self.universe.planets],
                'quests': self.universe.quests
            },
            'current_planet': self.current_planet.name,
            'game_over': self.game_over,
            'status_changed': self.status_changed
        }
        with open(filename, 'w') as file:
            json.dump(game_state, file)
        self.console.print(f"Game saved to {filename}")

    def load_game(self, filename):
        with open(filename, 'r') as file:
            game_state = json.load(file)
            self.player = Player(self.console)
            self.player.__dict__.update(game_state['player'])
            self.universe.planets = [Planet(**planet) for planet in game_state['universe']['planets']]
            self.universe.quests = game_state['universe']['quests']
            self.current_planet = next(planet for planet in self.universe.planets if planet.name == game_state['current_planet'])
            self.game_over = game_state['game_over']
            self.status_changed = game_state['status_changed']
        self.console.print(f"Game loaded from {filename}")

    def accept_quest(self, quest):
        # Check if the player has the required upgrades for passenger transport quests
        if quest['type'] == 'passenger_transport':
            if self.player.passenger_pod_capacity < quest['conditions']['quantity']:
                self.console.print("[bold red]You do not have enough passenger pod capacity to accept this quest.[/bold red]")
                return
            if self.player.life_support_expansion < quest['conditions']['quantity']:
                self.console.print("[bold red]You do not have enough life support expansion to accept this quest.[/bold red]")
                return

        # Accept the quest
        self.console.print(f"Quest accepted: {quest['description']}")
        self.player.accept_quest(quest)

    def generate_random_quest(self):
        # Determine the number of quests to generate based on the player's level
        if self.player.level <= 3:
            num_quests = 1
        elif self.player.level <= 10:
            num_quests = 2
        else:
            num_quests = 3

        # Generate random quests and add them to the universe quests list
        random_quests = random.sample(self.universe.quests, min(num_quests, len(self.universe.quests)))
        for quest in random_quests:
            self.console.print(f"\n[bold yellow]New Quest Available:[/bold yellow]")
            self.console.print(f"{quest['description']}")
            self.console.print(f"Backstory: {quest['backstory']}")
            self.universe.quests.append(quest)

def main():
    try:
        game = CargoHauler(difficulty=2)
        game.start_game()
    except Exception as e:
        print(f"Error starting the game: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    main()