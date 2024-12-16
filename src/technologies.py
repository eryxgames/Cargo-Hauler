class TechnologyTree:
    def __init__(self):
        self.technologies = {
            'Propulsion': {
                'Chemical Thrusters': {
                    'level': 1,
                    'cost': 1000,
                    'effects': {
                        'speed': 1.0,
                        'fuel_efficiency': 0.8
                    }
                },
                'Ion Drives': {
                    'level': 2,
                    'cost': 5000,
                    'effects': {
                        'speed': 1.5,
                        'fuel_efficiency': 1.2
                    }
                }
            },
            'Cargo': {
                'Basic Cargo Pods': {
                    'level': 1,
                    'cost': 1500,
                    'effects': {
                        'cargo_capacity': 100
                    }
                },
                'Advanced Containers': {
                    'level': 2,
                    'cost': 7500,
                    'effects': {
                        'cargo_capacity': 250
                    }
                }
            }
        }

    def get_available_upgrades(self, current_tech=None):
        available = {}
        for category, techs in self.technologies.items():
            available[category] = []
            for tech_name, tech_info in techs.items():
                if not current_tech or tech_info['level'] > current_tech.get(tech_name, {}).get('level', 0):
                    available[category].append({
                        'name': tech_name,
                        'cost': tech_info['cost']
                    })
        return available
