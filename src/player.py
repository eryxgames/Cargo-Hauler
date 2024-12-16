import random
from rich.console import Console
from rich.table import Table
import time
import json

class Player:
    def __init__(self, console):
        # Existing attributes
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
        self.life_support_expansion = 0
        self.passenger_pod_capacity = 0
        self.cargo_capacity = 100
        self.cargo_used = 0
        self.level = 1
        self.experience = 0
        self.active_quests = []
        self.ship_level = 1
        self.ship_fuel_efficiency = 1.0
        self.fuel_tank_capacity = 100
        self.fuel_level = 100
        self.total_fuel_used = 0
        self.total_trips = 0
        self.radiation_shield = False
        self.business_class_module = False
        self.passengers = []

    def add_passenger(self, passenger):
        if len(self.passengers) < self.passenger_pod_capacity:
            self.passengers.append(passenger)
            return True
        else:
            return False

    def remove_passenger(self, passenger):
        if passenger in self.passengers:
            self.passengers.remove(passenger)
            return True
        else:
            return False

    def view_passengers(self):
        table = Table(title="Passengers On Board")
        table.add_column("Name", style="cyan")
        table.add_column("Type", style="magenta")
        table.add_column("Destination", style="green")
        table.add_column("Reward", style="yellow")

        for passenger in self.passengers:
            table.add_row(
                passenger['name'],
                passenger['type'],
                passenger['destination'],
                str(passenger['reward'])
            )

        self.console.print(table)

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

    def view_trade_statistics(self):
        table = Table(title="Trade Statistics")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="magenta")

        table.add_row("Total Profit", f"{self.total_profit:.1f} credits")
        table.add_row("Total Loss", f"{self.total_loss:.1f} credits")
        table.add_row("Total Spent", f"{self.total_spent:.1f} credits")
        if self.most_profitable_good:
            table.add_row("Most Profitable Good", f"{self.most_profitable_good['good']}: {self.most_profitable_good['profit']:.1f} credits")
        else:
            table.add_row("Most Profitable Good", "None")
        if self.most_profitable_route:
            table.add_row("Most Profitable Route", self.most_profitable_route)
        else:
            table.add_row("Most Profitable Route", "None")
        table.add_row("Total Fuel Used", f"{self.total_fuel_used:.1f} units")
        if self.total_trips > 0:
            table.add_row("Average Fuel Consumption per Trip", f"{self.total_fuel_used / self.total_trips:.1f} units")
        else:
            table.add_row("Average Fuel Consumption per Trip", "0.0 units")
        table.add_row("Passengers Transported", str(len(self.passengers)))

        self.console.print(table)

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

    def view_trade_statistics1(self):
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
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Attribute", style="cyan")
        table.add_column("Value", style="magenta")

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

        # Display available passengers
        self.console.print("\nAvailable Passengers:")
        passengers = self.generate_available_passengers(current_planet)
        if not passengers:
            self.console.print("No passengers available at this time.")
        else:
            for i, passenger in enumerate(passengers, 1):
                self.console.print(f"{i}. {passenger['type']} - Destination: {passenger['destination']}, Reward: {passenger['reward']} credits")

            passenger_choice = self.console.input("[bold yellow]Enter the number of the passenger to pick up (or 'cancel'): [/bold yellow]")
            if passenger_choice.lower() == 'cancel':
                return

            try:
                passenger_index = int(passenger_choice)
                if 1 <= passenger_index <= len(passengers):
                    selected_passenger = passengers[passenger_index - 1]
                    if self.player.passenger_pod_capacity >= len(self.player.passengers) + 1:
                        self.player.add_passenger(selected_passenger)
                        self.console.print(f"Picked up {selected_passenger['type']} heading to {selected_passenger['destination']}.")
                    else:
                        self.console.print("[bold red]Not enough passenger pod capacity![/bold red]")
                else:
                    self.console.print("[bold red]Invalid choice![/bold red]")
            except ValueError:
                self.console.print("[bold red]Please enter a number![/bold red]")

    def generate_available_passengers(self, planet):
        # Logic to generate available passengers based on planet and player's ship upgrades
        passenger_types = ["Colonist", "Tourist", "Scientist"]
        destinations = [p.name for p in self.universe.planets if p != planet]
        passengers = []
        for _ in range(random.randint(1, 5)):
            passenger = {
                "name": f"Passenger_{len(passengers)+1}",
                "type": random.choice(passenger_types),
                "destination": random.choice(destinations),
                "reward": random.randint(100, 500)
            }
            passengers.append(passenger)
        return passengers
    
    
