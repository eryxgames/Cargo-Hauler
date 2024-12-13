import random

class Player:
    def __init__(self):
        self.credits = 10000
        self.cargo = {}
        self.cargo_capacity = 100
        self.cargo_used = 0
        self.ship_level = 1
        self.technologies = []
    
    def add_cargo(self, good, quantity, price):
        """
        Add cargo to the player's inventory
        
        Args:
            good (str): Name of the commodity
            quantity (int): Number of units to add
            price (float): Price per unit
        
        Returns:
            bool: True if successful, False otherwise
        """
        # Validate inputs
        if not isinstance(good, str):
            print(f"[ERROR] Invalid good type: {type(good)}")
            return False
        
        try:
            quantity = int(quantity)
            price = float(price)
        except (ValueError, TypeError):
            print(f"[ERROR] Invalid quantity or price: {quantity}, {price}")
            return False
        
        # Check cargo space
        if self.cargo_used + quantity > self.cargo_capacity:
            print("[ERROR] Not enough cargo space")
            return False
        
        # Check credits
        total_cost = quantity * price
        if total_cost > self.credits:
            print("[ERROR] Not enough credits")
            return False
        
        # Add or update cargo
        if good in self.cargo:
            # Update existing cargo entry
            existing_entry = self.cargo[good]
            
            # Ensure the entry is a dictionary
            if not isinstance(existing_entry, dict):
                existing_entry = {
                    'quantity': 0,
                    'buy_price': price
                }
            
            # Update quantity and recalculate average buy price
            total_quantity = existing_entry.get('quantity', 0) + quantity
            total_value = (existing_entry.get('quantity', 0) * existing_entry.get('buy_price', price)) + (quantity * price)
            
            self.cargo[good] = {
                'quantity': total_quantity,
                'buy_price': total_value / total_quantity
            }
        else:
            # Create new cargo entry
            self.cargo[good] = {
                'quantity': quantity,
                'buy_price': price
            }
        
        # Update player's state
        self.cargo_used += quantity
        self.credits -= total_cost
        
        return True
    
    def sell_cargo(self, good, quantity, price):
        """
        Sell cargo from the player's inventory
        
        Args:
            good (str): Name of the commodity
            quantity (int): Number of units to sell
            price (float): Price per unit
        
        Returns:
            bool: True if successful, False otherwise
        """
        # Validate inputs
        if good not in self.cargo:
            print(f"[ERROR] No {good} in cargo")
            return False
        
        try:
            quantity = int(quantity)
            price = float(price)
        except (ValueError, TypeError):
            print(f"[ERROR] Invalid quantity or price: {quantity}, {price}")
            return False
        
        # Check available quantity
        cargo_entry = self.cargo[good]
        
        # Ensure cargo_entry is a dictionary
        if not isinstance(cargo_entry, dict):
            print(f"[ERROR] Invalid cargo entry for {good}")
            return False
        
        available_quantity = cargo_entry.get('quantity', 0)
        
        if quantity > available_quantity:
            print(f"[ERROR] Not enough {good} to sell")
            return False
        
        # Calculate total revenue
        total_revenue = quantity * price
        
        # Update cargo
        cargo_entry['quantity'] -= quantity
        
        # Remove entry if quantity becomes zero
        if cargo_entry['quantity'] == 0:
            del self.cargo[good]
        
        # Update player's state
        self.cargo_used -= quantity
        self.credits += total_revenue
        
        return True
    
    def display_cargo(self):
        """
        Display current cargo inventory
        """
        print("Current Cargo:")
        if not self.cargo:
            print("  Empty")
            return
        
        for good, details in self.cargo.items():
            print(f"  {good}: {details.get('quantity', 0)} units (Avg. Buy Price: {details.get('buy_price', 0):.2f} credits)")
    
    def get_cargo_summary(self):
        summary = []
        for name, details in self.cargo.items():
            summary.append({
                'name': name,
                'quantity': details['quantity'],
                'buy_price': details['buy_price']
            })
        return summary