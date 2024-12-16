import random
import json
import networkx as nx
import os

class Planet:
    def __init__(self, name, planet_type, economy_level, resources, status, characteristics, demographics, planet_class, moons, geology, climate, history):
        self.name = name
        self.type = planet_type
        self.economy_level = economy_level
        self.resources = resources
        self.status = status
        self.characteristics = characteristics
        self.demographics = demographics
        self.planet_class = planet_class
        self.moons = moons
        self.geology = geology
        self.climate = climate
        self.history = history

    def __repr__(self):
        return f"Planet({self.name})"

    def __eq__(self, other):
        if isinstance(other, Planet):
            return self.name == other.name
        return False

    def __hash__(self):
        return hash(self.name)

class UniverseGenerator:
    def __init__(self, difficulty=2):
        self.difficulty = difficulty
        self.planets = []
        self.trade_network = nx.Graph()
        self.quests = []
        self.generate_universe()
        self.load_quests()

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

            # Generate random status and characteristics
            status = random.choice(["Stable", "Unstable", "War-torn"])
            characteristics = random.choice(["Friendly", "Hostile", "Neutral"])

            # Generate random demographics
            demographics = {
                "Population": random.randint(1000, 10000),
                "Cyborgs": random.randint(1, 100),
                "Androids": random.randint(1, 100),
                "Robots": random.randint(1, 100)
            }

            # Generate additional attributes
            planet_class = random.choice(["Terrestrial", "Gas Giant", "Ice World", "Asteroid Belt"])
            moons = random.randint(0, 5)
            geology = random.choice(["Rocky", "Volcanic", "Mountainous", "Flat"])
            climate = random.choice(["Temperate", "Arid", "Frozen", "Harsh"])

            # Generate planet type
            planet_type = random.choice(planet_types)

            # Generate history
            history = self.generate_history(planet_name, planet_type, status, characteristics, demographics, planet_class, moons, geology, climate)

            planet = Planet(
                name=planet_name,
                planet_type=planet_type,
                economy_level=random.uniform(0.3, 1.0),
                resources=self.generate_resources(),
                status=status,
                characteristics=characteristics,
                demographics=demographics,
                planet_class=planet_class,
                moons=moons,
                geology=geology,
                climate=climate,
                history=history
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

    def generate_history(self, name, planet_type, status, characteristics, demographics, planet_class, moons, geology, climate):
        # Generate a creative and interesting history for the planet
        history_templates = [
            f"{name} was colonized by the first wave of interstellar explorers. Its {planet_type} environment made it a prime candidate for {characteristics} settlements. The planet is known for its {geology} landscapes and {climate} weather conditions. With a population of {demographics['Population']}, it has become a hub for {planet_class} activities.",
            f"{name} has a rich history of {status} conflicts. Its {planet_type} terrain and {geology} features have made it a strategic location for various factions. The planet's {climate} climate and {moons} moons add to its unique charm. With a population of {demographics['Population']}, it continues to be a center of {characteristics} interactions.",
            f"{name} was discovered during the great expansion era. Its {planet_type} resources and {geology} formations attracted early settlers. The planet's {climate} environment and {moons} moons have shaped its cultural identity. With a population of {demographics['Population']}, it remains a key player in interstellar {planet_class} trade.",
            f"{name} has always been a {characteristics} planet, known for its {planet_type} exports and {geology} landscapes. Its {climate} weather and {moons} moons have influenced its development. With a population of {demographics['Population']}, it continues to thrive as a {planet_class} colony.",
            f"{name} was once a {status} outpost, but its {planet_type} resources and {geology} features have transformed it into a bustling metropolis. The planet's {climate} climate and {moons} moons have contributed to its growth. With a population of {demographics['Population']}, it is now a major {planet_class} hub."
        ]
        return random.choice(history_templates)

    def load_quests(self):
        # Load quests from the external JSON file
        with open(os.path.join(os.path.dirname(__file__), '../data/quests.json'), 'r') as file:
            quest_data = json.load(file)
            self.quests = quest_data['quests']

    def generate_random_quest(self):
        # Generate a random quest at the start of each player turn
        num_quests = max(1, min(4, self.player.level // 3))  # Adjust the number of quests based on the player's level
        random_quests = random.sample(self.quests, min(num_quests, len(self.quests)))
        for quest in random_quests:
            self.console.print(f"\n[bold yellow]New Quest Available:[/bold yellow]")
            self.console.print(f"{quest['description']}")
            self.console.print(f"Backstory: {quest['backstory']}")
            self.quests.append(quest)
