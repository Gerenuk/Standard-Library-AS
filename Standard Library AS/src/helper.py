import random
import brewer2mpl

QUALI_COLOR_PARAM = ['Paired', 'Qualitative', 12]


CMAP = brewer2mpl.get_map(*QUALI_COLOR_PARAM)


def get_quali_color(hashable=None, color_type="hex_colors"):
    if hashable is None:
        color = random.randrange(12)
    else:
        color = (hash(hashable) & 255) % QUALI_COLOR_PARAM[2]
    return getattr(CMAP, color_type)[color]


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


class CycleCaller:
    def __init__(self, cycle, obj):
        self.cycle = cycle
        self.obj = obj
        self.count = 0

    def __getattr__(self, name):
        self.count += 1
        if self.count >= self.cycle:
            self.count = 0
            return getattr(self.obj, name)
        else:
            return self._void

    def _void(self, *args, **kwargs):
        pass


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
