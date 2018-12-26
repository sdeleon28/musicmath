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
    def __init__(self, scale, mode_name, notes):
        self.scale = scale
        self.mode_name = mode_name
        self.notes = notes

    @staticmethod
    def make(scale, mode_name):
        mode = MODES[mode_name]
        shift_by = mode - 1
        notes = shift(scale.notes, shift_by)
        return Mode(scale, mode_name, notes)

    def __str__(self):
        return self.mode_name + ' mode of the ' + self.scale.get_scale_name() + ' -> ' + ' '.join(self.notes)
