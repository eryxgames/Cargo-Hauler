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
        if self.cargo_used + quantity > self.cargo_capacity:
            return False
        
        if good in self.cargo:
            self.cargo[good]['quantity'] += quantity
        else:
            self.cargo[good] = {
                'quantity': quantity,
                'buy_price': price
            }
        
        self.cargo_used += quantity
        self.credits -= quantity * price
        return True
    
    def sell_cargo(self, good, quantity, price):
        if good not in self.cargo or self.cargo[good]['quantity'] < quantity:
            return False
        
        self.cargo[good]['quantity'] -= quantity
        self.credits += quantity * price
        self.cargo_used -= quantity
        
        if self.cargo[good]['quantity'] == 0:
            del self.cargo[good]
        
        return True