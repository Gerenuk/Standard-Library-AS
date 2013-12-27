import random
import brewer2mpl

QUALI_COLOR_PARAM = ['Paired', 'Qualitative', 12]


CMAP = brewer2mpl.get_map(*QUALI_COLOR_PARAM)
def get_quali_color(hashable=None):
    if hashable is None:
        color = random.randrange(12)
    else:
        color = (hash(hashable) & 255) % QUALI_COLOR_PARAM[2]
    return CMAP.hex_colors[color]


class CycleCounter:
    def __init__(self, cycle):
        self.cycle = cycle
        self.count = 0

    def __bool__(self):
        self.count += 1
        if self.count == self.cycle:
            self.count = 0
            return True
        return False


class MaxFinder:
    def __init__(self):
        self.max_score = None
        self.max_object = None

    def add(self, score, object_=None):
        if self.max_score is None or score > self.max_score:
            self.max_score = score
            self.max_object = object_

    def get_max(self):
        return (self.max_score, self.max_object)
