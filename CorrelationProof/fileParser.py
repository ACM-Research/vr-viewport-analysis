from typing import List, Tuple


class SalientFeaturePosition:
    frame: int
    positions: List[Tuple[int, int]]

    def __init__(self):
        self.frame = 0  # placeholder values...
        self.positions = [(0, 0), (0, 0)]  # X, Y of each salient feature

    def count(self):
        """Returns number of salient features"""
        return len(self.positions)

    def __gt__(self, other):
        return self.frame > other.frame

    def __lt__(self, other):
        return self.frame < other.frame

    def __eq__(self, other):
        return self.frame == other.frame
