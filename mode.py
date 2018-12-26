MODES = {
    'ionian': 1,
    'dorian': 2,
    'phrygian': 3,
    'lydian': 4,
    'mixolydian': 5,
    'aeolian': 6,
    'locrian': 7,
}

def shift(elements, shift_by):
    out = elements[:]
    while shift_by:
        out.append(out.pop(0))
        shift_by -= 1
    return out

class Mode(object):
    @staticmethod
    def make(scale, mode_name):
        mode = MODES[mode_name]
        shift_by = mode - 1
        return shift(scale, shift_by)
