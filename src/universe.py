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
        
        # Define planet names as a reusable list
        self.planet_names = [
            "New Terra", "Proxima", "Arcturus", "Orion Prime", 
            "Sigma Outpost", "Epsilon Station", "Nova Haven",
            "Andromeda Base", "Centauri Outpost", "Nebula Prime",
            "Starlight Station", "Horizon Colony", "Quantum Nexus"
        ]
        self.planet_types = [
            "Desert", "Oceanic", "Industrial", "Agricultural", 
            "High-Tech", "Mining", "Trading Hub"
        ]
        
        self.generate_universe()
    
    def generate_universe(self):
        # Generate planets based on difficulty
        num_planets = 5 + (self.difficulty * 2)
        
        # Create a copy of planet names to avoid modifying the original list
        available_names = self.planet_names.copy()
        
        for _ in range(min(num_planets, len(available_names))):
            # If no names left, break the loop
            if not available_names:
                break
            
            # Choose and remove a random name
            name = random.choice(available_names)
            available_names.remove(name)
            
            planet = Planet(
                name=name,
                planet_type=random.choice(self.planet_types),
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