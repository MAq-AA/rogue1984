import json
from dataclasses import dataclass, fields


@dataclass
class _Tracker:
    treasure: int = 0
    level: int = 1
    enemies: int = 0
    food: int = 0
    elixirs: int = 0
    scrolls: int = 0
    attacks: int = 0
    hits: int = 0
    tiles: int = 0

    def __init__(self):
        self.stats = [x.name for x in fields(self)]

    def write_stats(self):
        try:
            with open("statistics.json", "r") as f:
                all_stats = json.load(f)
        except FileNotFoundError:
            all_stats = []
        new_record = {stat: getattr(self, stat) for stat in self.stats}
        all_stats.append(new_record)
        with open("statistics.json", "w") as f:
            json.dump(all_stats, f)


stat_tracker = _Tracker()
