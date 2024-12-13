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
        # Align resource types with commodity types
        resource_types = [
            "raw_materials", 
            "agricultural_goods", 
            "technological_goods", 
            "luxury_goods", 
            "industrial_goods"
        ]
        
        # Randomly select 3-4 resources and assign them a value
        selected_resources = random.sample(resource_types, random.randint(3, 4))
        return {
            resource: random.uniform(0.1, 1.0) 
            for resource in selected_resources
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
            "Sigma Outpost", "Epsilon Station", "Nova Haven", 
            "Quantum Nexus", "Helios Prime", "Crimson Horizon"
        ]
        planet_types = [
            "Desert", "Oceanic", "Industrial", "Agricultural", 
            "High-Tech", "Mining", "Trading Hub", "Research Colony"
        ]
        
        # Generate planets based on difficulty
        num_planets = 5 + (self.difficulty * 2)
        
        for _ in range(num_planets):
            # Ensure unique planet names
            planet_name = random.choice(planet_names)
            planet_names.remove(planet_name)
            
            planet = Planet(
                name=planet_name,
                planet_type=random.choice(planet_types),
                economy_level=random.uniform(0.3, 1.0)
            )
            self.planets.append(planet)
        
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