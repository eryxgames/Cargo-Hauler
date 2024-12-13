import random
import json
import pandas as pd
import os

class EconomySimulator:
    def __init__(self, planets):
        self.planets = planets
        self.commodities = self.load_commodities()
    
    def load_commodities(self):
        # Determine the path to the commodities.json file
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        commodities_path = os.path.join(base_path, 'data', 'commodities.json')
        
        try:
            with open(commodities_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Warning: Commodities file not found at {commodities_path}")
            return self.generate_default_commodities()
    
    def generate_default_commodities(self):
        # Fallback method if JSON is not found
        return {
            "raw_materials": [
                {
                    "name": "Minerals",
                    "base_price": 150.00,
                    "volume_per_unit": 2.5,
                    "price_volatility": 0.15
                }
            ]
        }
    
    def calculate_price(self, commodity, planet):
        # More complex price calculation using commodity details
        base_price = commodity['base_price']
        volatility = commodity['price_volatility']
        
        # Adjust price based on planet's economy and random factors
        economy_multiplier = planet.economy_level
        price_variation = random.uniform(-volatility, volatility)
        
        final_price = base_price * (1 + price_variation) * economy_multiplier
        
        return round(final_price, 2)
    
    def get_market_overview(self):
        market_data = []
        
        # Iterate through all commodity categories
        for category, commodities in self.commodities.items():
            for commodity in commodities:
                planet_prices = {
                    'Category': category,
                    'Commodity': commodity['name']
                }
                
                # Get prices for each planet
                for planet in self.planets:
                    planet_prices[planet.name] = self.calculate_price(commodity, planet)
                
                market_data.append(planet_prices)
        
        return pd.DataFrame(market_data)
    
    def get_tradable_commodities(self):
        # Flatten the commodities dictionary into a list
        all_commodities = []
        for category, commodities in self.commodities.items():
            all_commodities.extend(commodities)
        return all_commodities