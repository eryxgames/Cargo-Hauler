import random

class EventGenerator:
    def __init__(self):
        self.events = {
            'trade_opportunity': {
                'weight': 0.3,
                'description': "Discovered a rare trade opportunity!"
            },
            'pirate_encounter': {
                'weight': 0.2,
                'description': "Pirates attempt to intercept your cargo!"
            },
            'market_crash': {
                'weight': 0.1,
                'description': "Sudden market crash affects commodity prices!"
            },
            'technological_breakthrough': {
                'weight': 0.2,
                'description': "A new technology has been discovered!"
            }
        }

    def generate_event(self):
        # Weighted random event selection
        events = list(self.events.keys())
        weights = [self.events[event]['weight'] for event in events]

        selected_event = random.choices(events, weights=weights)[0]
        return {
            'type': selected_event,
            'description': self.events[selected_event]['description']
        }
