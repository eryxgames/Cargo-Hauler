import random
import json
import pandas as pd
import os

class EconomySimulator:
    def __init__(self, planets):
        self.planets = planets
        self.commodities = self.generate_commodities()
        self.market_data = {planet.name: {commodity: {'price': self.calculate_price(commodity, planet), 'quantity': random.randint(50, 200)} for commodity in self.commodities} for planet in self.planets}

    def generate_commodities(self):
        commodity_types = [
            "raw_materials",
            "agricultural_goods",
            "technological_goods",
            "luxury_goods",
            "industrial_goods",
            "fuel"  # Adding fuel as a commodity
        ]

        commodities = {}
        for commodity in commodity_types:
            commodities[commodity] = {
                'base_price': random.uniform(50, 500),
                'price_volatility': random.uniform(0.05, 0.2)
            }

        return commodities

    def calculate_price(self, commodity, planet):
        # Ensure the commodity exists in our commodities dictionary
        if commodity not in self.commodities:
            raise ValueError(f"Commodity {commodity} not found in market")

        # Safely extract commodity information
        commodity_info = self.commodities[commodity]

        # Extract base price and volatility
        base_price = commodity_info['base_price']
        volatility = commodity_info['price_volatility']

        # Adjust price based on planet's economy and available resources
        economy_multiplier = planet.economy_level

        # Check if the planet has this commodity in its resources
        resource_multiplier = planet.resources.get(commodity, 0.5)

        # Calculate price variation
        price_variation = random.uniform(-volatility, volatility)

        # Calculate final price
        final_price = base_price * (1 + price_variation) * economy_multiplier * resource_multiplier

        return round(final_price, 2)

    def get_market_overview(self):
        market_data = []
        for planet in self.planets:
            planet_prices = {
                'Planet': planet.name,
            }
            for commodity in self.commodities:
                planet_prices[commodity] = self.calculate_price(commodity, planet)
            market_data.append(planet_prices)

        return pd.DataFrame(market_data)

    def get_tradable_commodities(self, planet):
        tradable = []
        for category, items in planet.market.items():
            for item, details in items.items():
                if details['quantity'] > 0:
                    tradable.append((category, item, details['price']))
        return tradable

    def update_market(self):
        for planet in self.planets:
            for commodity in self.commodities:
                quantity = self.market_data[planet.name][commodity]['quantity']
                price = self.calculate_price(commodity, planet)
                self.market_data[planet.name][commodity]['price'] = price
                self.market_data[planet.name][commodity]['quantity'] = quantity