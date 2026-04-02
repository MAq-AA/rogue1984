import json
from dataclasses import dataclass, fields

from api import GameStats, RunStats


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

    def get_all_stats(self) -> list:
        try:
            with open("statistics.json", "r") as f:
                all_stats = json.load(f)
        except FileNotFoundError:
            all_stats = []
        return all_stats

    def write_stats(self):
        all_stats = self.get_all_stats()
        new_record = {stat: getattr(self, stat) for stat in self.stats}
        all_stats.append(new_record)
        with open("statistics.json", "w") as f:
            json.dump(all_stats, f)

    def load_stats(self) -> GameStats:
        all_stats = self.get_all_stats()
        run_list = [RunStats(**row) for row in all_stats]
        return GameStats(run_list)


stat_tracker = _Tracker()
