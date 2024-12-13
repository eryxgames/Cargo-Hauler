import random

class Player:
    def __init__(self, starting_credits=10000):
        self.credits = starting_credits
        self.cargo = {}
        self.cargo_capacity = 100
        self.cargo_used = 0
        self.ship_level = 1
        self.technologies = []
    
    def add_cargo(self, commodity, quantity, price):
        # Check if there's enough cargo space
        if self.cargo_used + quantity > self.cargo_capacity:
            return False
        
        # Check if player has enough credits
        total_cost = quantity * price
        if total_cost > self.credits:
            return False
        
        # Add commodity to cargo
        if commodity['name'] in self.cargo:
            self.cargo[commodity['name']]['quantity'] += quantity
        else:
            self.cargo[commodity['name']] = {
                'quantity': quantity,
                'buy_price': price,
                'volume': commodity.get('volume_per_unit', 1)
            }
        
        # Update player's finances and cargo
        self.credits -= total_cost
        self.cargo_used += quantity * commodity.get('volume_per_unit', 1)
        
        return True
    
    def sell_cargo(self, commodity_name, quantity, price):
        # Check if player has enough cargo
        if commodity_name not in self.cargo or self.cargo[commodity_name]['quantity'] < quantity:
            return False
        
        # Sell cargo and update player's finances
        self.cargo[commodity_name]['quantity'] -= quantity
        self.credits += quantity * price
        
        # Reduce cargo used
        cargo_volume = self.cargo[commodity_name].get('volume', 1)
        self.cargo_used -= quantity * cargo_volume
        
        # Remove commodity if quantity is zero
        if self.cargo[commodity_name]['quantity'] == 0:
            del self.cargo[commodity_name]
        
        return True
    
    def get_cargo_summary(self):
        summary = []
        for name, details in self.cargo.items():
            summary.append({
                'name': name,
                'quantity': details['quantity'],
                'buy_price': details['buy_price']
            })
        return summary