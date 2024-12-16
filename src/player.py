import random
from rich.console import Console
from rich.table import Table
import time
import json

class Player:
    def __init__(self, console):
        self.console = console
        self.credits = 10000
        self.inventory = {}
        self.trade_route = []
        self.trade_history = []
        self.total_profit = 0
        self.total_loss = 0
        self.total_spent = 0
        self.most_profitable_good = None
        self.most_profitable_route = None
        self.life_support_expansion = 0  # Add life support expansion attribute
        self.passenger_pod_capacity = 0  # Add passenger pod capacity attribute
        self.cargo_capacity = 100  # Initial cargo capacity
        self.cargo_used = 0  # Initial cargo used
        self.level = 1  # Initial player level
        self.experience = 0  # Initial experience points
        self.active_quests = []  # List of active quests
        self.ship_level = 1  # Initial ship level
        self.ship_fuel_efficiency = 1.0  # Initial fuel efficiency
        self.fuel_tank_capacity = 100  # Initial fuel tank capacity
        self.fuel_level = 100  # Initial fuel level
        self.total_fuel_used = 0  # Total fuel used
        self.total_trips = 0  # Total trips
        self.radiation_shield = False  # New ship upgrade
        self.business_class_module = False  # New ship upgrade

    def add_cargo(self, good, quantity, price_per_unit):
        """
        Add cargo to the player's inventory

        Args:
            good (str): Name of the commodity
            quantity (int): Number of units to add
            price_per_unit (float): Price per unit

        Returns:
            bool: True if successful, False otherwise
        """
        # Validate inputs
        if not isinstance(good, str):
            print(f"[ERROR] Invalid good type: {type(good)}")
            return False

        try:
            quantity = int(quantity)
            price_per_unit = float(price_per_unit)
        except (ValueError, TypeError):
            print(f"[ERROR] Invalid quantity or price: {quantity}, {price_per_unit}")
            return False

        # Check cargo space
        if self.cargo_used + quantity > self.cargo_capacity:
            print("[ERROR] Not enough cargo space")
            return False

        # Check credits
        total_cost = quantity * price_per_unit
        if total_cost > self.credits:
            print("[ERROR] Not enough credits")
            return False

        # Add or update cargo
        if good in self.inventory:
            # Update existing cargo entry
            existing_entry = self.inventory[good]

            # Ensure the entry is a dictionary
            if not isinstance(existing_entry, dict):
                existing_entry = {
                    'quantity': 0,
                    'buy_price': price_per_unit
                }

            # Update quantity and recalculate average buy price
            total_quantity = existing_entry.get('quantity', 0) + quantity
            total_value = (existing_entry.get('quantity', 0) * existing_entry.get('buy_price', price_per_unit)) + (quantity * price_per_unit)

            self.inventory[good] = {
                'quantity': total_quantity,
                'buy_price': total_value / total_quantity
            }
        else:
            # Create new cargo entry
            self.inventory[good] = {
                'quantity': quantity,
                'buy_price': price_per_unit
            }

        # Update player's state
        self.cargo_used += quantity
        self.credits -= total_cost

        return True

    def sell_cargo(self, good, quantity, price_per_unit):
        """
        Sell cargo from the player's inventory

        Args:
            good (str): Name of the commodity
            quantity (int): Number of units to sell
            price_per_unit (float): Price per unit

        Returns:
            bool: True if successful, False otherwise
        """
        # Validate inputs
        if good not in self.inventory:
            print(f"[ERROR] No {good} in cargo")
            return False

        try:
            quantity = int(quantity)
            price_per_unit = float(price_per_unit)
        except (ValueError, TypeError):
            print(f"[ERROR] Invalid quantity or price: {quantity}, {price_per_unit}")
            return False

        # Check available quantity
        cargo_entry = self.inventory[good]

        # Ensure cargo_entry is a dictionary
        if not isinstance(cargo_entry, dict):
            print(f"[ERROR] Invalid cargo entry for {good}")
            return False

        available_quantity = cargo_entry.get('quantity', 0)

        if quantity > available_quantity:
            print(f"[ERROR] Not enough {good} to sell")
            return False

        # Calculate profit
        buy_price = self.inventory[good]['buy_price']
        profit = (price_per_unit - buy_price) * quantity

        # Gain experience
        self.gain_experience(profit)

        # Update trade statistics
        self.update_trade_statistics(good, profit)

        # Calculate total revenue
        total_revenue = quantity * price_per_unit

        # Update cargo
        cargo_entry['quantity'] -= quantity

        # Remove entry if quantity becomes zero
        if cargo_entry['quantity'] == 0:
            del self.inventory[good]

        # Update player's state
        self.cargo_used -= quantity
        self.credits += total_revenue

        return True

    def gain_experience(self, amount):
        self.experience += amount
        self.check_level_up()

    def check_level_up(self):
        experience_thresholds = [100, 200, 300, 400, 500]  # Define experience thresholds for each level
        while self.level < len(experience_thresholds) and self.experience >= experience_thresholds[self.level - 1]:
            self.level += 1
            self.console.print(f"[bold green]Level up! You are now level {self.level}[/bold green]")
            # Grant benefits upon leveling up
            self.grant_level_benefits()

    def grant_level_benefits(self):
        # Define benefits for each level
        if self.level == 2:
            self.cargo_capacity += 50
            self.console.print("Cargo capacity increased to 150")
        elif self.level == 3:
            self.ship_level += 1
            self.console.print("Ship level increased to 2")
        # Add more level benefits as needed

    def update_trade_statistics(self, good, profit):
        if profit > 0:
            self.total_profit += profit
            if self.most_profitable_good is None or profit > self.most_profitable_good['profit']:
                self.most_profitable_good = {
                    'good': good,
                    'profit': profit
                }
        else:
            self.total_loss += abs(profit)

    def accept_quest(self, quest):
        # Implement quest acceptance logic
        self.console.print(f"Quest accepted: {quest['description']}")
        # Add quest rewards
        self.credits += quest['reward']
        self.console.print(f"Reward: {quest['reward']} credits")
        self.active_quests.append(quest)

    def complete_quest(self, quest):
        # Implement quest completion logic
        self.console.print(f"Quest completed: {quest['description']}")
        self.active_quests.remove(quest)

    def view_technologies(self):
        self.console.print("Current Technologies:")
        for category, techs in self.technologies.items():
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
        return self.storyline.get_story_up_to_level(self.level)

    def display_storyline_entry(self, entry):
        self.console.print(f"[bold yellow]Press any key to continue...[/bold yellow]")
        for char in entry:
            self.console.print(char, end='')
            time.sleep(0.05)  # Adjust the speed as needed
        self.console.input()

    def view_trade_statistics(self):
        self.console.print("Trade Statistics:")
        self.console.print(f"Total Profit: {self.total_profit:.1f} credits")
        self.console.print(f"Total Loss: {self.total_loss:.1f} credits")
        self.console.print(f"Total Spent: {self.total_spent:.1f} credits")
        self.console.print(f"Most Profitable Good: {self.most_profitable_good}")
        self.console.print(f"Most Profitable Trade Route: {self.most_profitable_route}")
        self.console.print(f"Total Fuel Used: {self.total_fuel_used:.1f} units")
        if self.total_trips > 0:
            self.console.print(f"Average Fuel Consumption per Trip: {self.total_fuel_used / self.total_trips:.1f} units")
        else:
            self.console.print(f"Average Fuel Consumption per Trip: 0.0 units")

        # Display a table of trade history
        table = Table(title="Trade History")
        table.add_column("Transaction ID", style="cyan")
        table.add_column("Good", style="magenta")
        table.add_column("Quantity", style="green")
        table.add_column("Price per Unit", style="yellow")
        table.add_column("Total", style="bold")

        for transaction in self.trade_history:
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
        table.add_row("Economy Level", f"{current_planet.economy_level:.1f}")
        resources_display = ", ".join([f"{r}: {v:.1f}" for r, v in current_planet.resources.items()])
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
        for quest in self.active_quests:
            if quest['conditions']['destination'] == current_planet.name:
                self.console.print(f"[bold green]Quest completed: {quest['description']}[/bold green]")
                self.complete_quest(quest)

        # Add quest system
        self.console.print("\nAvailable Quests:")
        for i, quest in enumerate(self.universe.quests, 1):
            self.console.print(f"{i}. {quest['description']}")
            self.console.print(f"   Backstory: {quest['backstory']}")

        quest_choice = self.console.input("[bold yellow]Enter the number of the quest to accept (or 'cancel'): [/bold yellow]")
        if quest_choice.lower() == 'cancel':
            return

        try:
            quest_index = int(quest_choice)
            if 1 <= quest_index <= len(self.universe.quests):
                selected_quest = self.universe.quests[quest_index - 1]
                self.accept_quest(selected_quest)
                self.universe.quests.remove(selected_quest)
            else:
                self.console.print("[bold red]Invalid choice![/bold red]")
        except ValueError:
            self.console.print("[bold red]Please enter a number![/bold red]")

