from key import Key, get_sharp_enharmonic

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

    @property
    def formula(self):
        return self.scale.formula

    @property
    def root(self):
        return self.notes[0]

    @property
    def normalized_notes(self):
        return [
            get_sharp_enharmonic(note)
            if 'b' in note
            else note
            for note in self.notes
        ]

    @staticmethod
    def make(scale, mode_name):
        mode = MODES[mode_name]
        shift_by = mode - 1
        notes = shift(scale.notes, shift_by)
        return Mode(scale, mode_name, notes)

    @staticmethod
    def make_all_dorian():
        keys = Key.make_all_majors()
        dorian_modes = []
        for key in keys:
            scale = key.get_corrected_scale()
            mode = Mode.make(scale, 'dorian')
            dorian_modes.append(mode)
        return dorian_modes

    def __str__(self):
        return '{root} {mode_name} mode ({scale_name}) -> {scale_notes}'.format(
            root=self.root,
            mode_name=self.mode_name,
            scale_name=self.scale.get_scale_name(),
            scale_notes=' '.join(self.notes),
        )
