import random
import pandas as pd

class EconomySimulator:
    def __init__(self, planets):
        self.planets = planets
        self.commodities = self.generate_commodities()
    
    def generate_commodities(self):
        commodity_types = [
            "Minerals", "Grain", "Technology Components", 
            "Rare Metals", "Manufactured Goods"
        ]
        
        commodities = {}
        for commodity in commodity_types:
            base_price = random.uniform(50, 500)
            commodities[commodity] = {
                'base_price': base_price,
                'price_volatility': random.uniform(0.05, 0.2)
            }
        
        return commodities
    
    def calculate_price(self, commodity, planet):
        base_price = self.commodities[commodity]['base_price']
        volatility = self.commodities[commodity]['price_volatility']
        
        # Adjust price based on planet's economy and resource abundance
        economy_multiplier = planet.economy_level
        resource_multiplier = planet.resources.get(commodity, 0.5)
        
        price_variation = random.uniform(-volatility, volatility)
        
        final_price = base_price * (1 + price_variation) * economy_multiplier * resource_multiplier
        
        return round(final_price, 2)
    
    def get_market_overview(self):
        market_data = []
        for planet in self.planets:
            planet_prices = {
                'Planet': planet.name,
                'Economy Level': planet.economy_level
            }
            
            for commodity in self.commodities:
                planet_prices[commodity] = self.calculate_price(commodity, planet)
            
            market_data.append(planet_prices)
        
        return pd.DataFrame(market_data)