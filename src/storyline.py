class Storyline:
    def __init__(self):
        self.story_parts = {
            1: "You start your journey as a space trader, aiming to make a name for yourself in the cosmos.",
            2: "After several successful trades, you hear rumors of a hidden treasure on a distant planet.",
            3: "As you expand your trade routes, you encounter a group of pirates who challenge your dominance.",
            4: "You discover an ancient technology that could revolutionize space travel, but it's protected by a powerful faction.",
            5: "With your growing reputation, you are invited to join a prestigious space traders' guild.",
            # Add more story parts for higher levels
        }

    def get_story_up_to_level(self, level):
        return [self.story_parts.get(lvl, "") for lvl in range(1, level + 1) if lvl in self.story_parts]
