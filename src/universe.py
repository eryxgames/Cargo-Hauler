import random
import json
import networkx as nx

class Planet:
    def __init__(self, name, planet_type, economy_level):
        self.name = name
        self.type = planet_type
        self.economy_level = economy_level
        self.resources = self.generate_resources()
    
    def generate_resources(self):
        resource_types = [
            "Minerals", "Agricultural Goods", "Technology", 
            "Rare Elements", "Manufactured Goods"
        ]
        return {
            resource: random.uniform(0.1, 1.0) 
            for resource in random.sample(resource_types, 3)
        }

class UniverseGenerator:
    def __init__(self, difficulty=2):
        self.difficulty = difficulty
        self.planets = []
        self.trade_network = nx.Graph()
        self.generate_universe()
    
    def generate_universe(self):
        planet_names = [
            "New Terra", "Proxima", "Arcturus", "Orion Prime", 
            "Sigma Outpost", "Epsilon Station", "Nova Haven"
        ]
        planet_types = [
            "Desert", "Oceanic", "Industrial", "Agricultural", 
            "High-Tech", "Mining", "Trading Hub"
        ]
        
        # Generate planets based on difficulty
        num_planets = 5 + (self.difficulty * 2)
        
        for _ in range(num_planets):
            planet = Planet(
                name=random.choice(planet_names),
                planet_type=random.choice(planet_types),
                economy_level=random.uniform(0.3, 1.0)
            )
            self.planets.append(planet)
            planet_names.remove(planet.name)  # Ensure unique names
        
        # Create trade network
        self.create_trade_network()
    
    def create_trade_network(self):
        # Fully connect planets for simplicity
        for planet in self.planets:
            self.trade_network.add_node(planet)
        
        for i in range(len(self.planets)):
            for j in range(i+1, len(self.planets)):
                # Add some randomness to connections
                if random.random() > 0.3:
                    self.trade_network.add_edge(
                        self.planets[i], 
                        self.planets[j], 
                        distance=random.uniform(1, 10)
                    )