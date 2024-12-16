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
                    },
                    'category': 'Propulsion'
                },
                'Ion Drives': {
                    'level': 2,
                    'cost': 5000,
                    'effects': {
                        'speed': 1.5,
                        'fuel_efficiency': 1.2
                    },
                    'category': 'Propulsion'
                }
            },
            'Cargo': {
                'Basic Cargo Pods': {
                    'level': 1,
                    'cost': 1500,
                    'effects': {
                        'cargo_capacity': 100
                    },
                    'category': 'Cargo'
                },
                'Advanced Containers': {
                    'level': 2,
                    'cost': 7500,
                    'effects': {
                        'cargo_capacity': 250
                    },
                    'category': 'Cargo'
                }
            },
            'Life Support': {
                'Life Support Expansion': {
                    'level': 1,
                    'cost': 5000,
                    'effects': {
                        'life_support_capacity': 50
                    },
                    'category': 'Life Support'
                },
                'Passenger Pod': {
                    'level': 1,
                    'cost': 5000,
                    'effects': {
                        'passenger_pod_capacity': 50
                    },
                    'category': 'Passenger Pod'
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
                        'cost': tech_info['cost'],
                        'category': tech_info['category']
                    })
        return available
