import json
import os

class TechnologyTree:
    def __init__(self):
        self.technologies = self.load_technologies()

    def load_technologies(self):
        with open(os.path.join(os.path.dirname(__file__), '../data/technologies.json'), 'r') as file:
            return json.load(file)

    def get_available_upgrades(self, current_tech=None):
        available = {}
        for category, techs in self.technologies.items():
            available[category] = []
            for tech_name, tech_info in techs.items():
                if not current_tech or tech_info['level'] > current_tech.get(tech_name, {}).get('level', 0):
                    available[category].append({
                        'name': tech_name,
                        'cost': tech_info['cost'],
                        'category': tech_info['category'],
                        'effects': tech_info['effects']
                    })
        return available
