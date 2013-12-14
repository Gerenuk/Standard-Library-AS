import random
import brewer2mpl

QUALI_COLOR_PARAM=['Paired', 'Qualitative', 12]


CMAP=brewer2mpl.get_map(*QUALI_COLOR_PARAM)
def get_quali_color(hashable=None):
    if hashable is None:
        color=random.randrange(12)
    else:
        color=(hash(hashable)&255) % QUALI_COLOR_PARAM[2]
    return CMAP.hex_colors[color]