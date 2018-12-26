NOTE_NAMES = 'C C# D D# E F F# G G# A A# B'.split()

FORMULAS = {
    'ionian'        :   '1	2	3	4	5	6	7'.split(),
    'dorian'        :   '1	2	b3	4	5	6	b7'.split(),
    'phrygian'      :   '1	b2	b3	4	5	b6	b7'.split(),
    'lydian'        :   '1	2	3	#4	5	6	7'.split(),
    'mixolydian'    :   '1	2	3	4	5	6	b7'.split(),
    'aeolian'       :   '1	2	b3	4	5	b6	b7'.split(),
    'locrian'       :   '1	b2	b3	4	b5	b6	b7'.split(),
}

INTERVALS_TO_SEMITONES = {
    '1': 0,
    'b2': 1,
    '2': 2,
    'b3': 3,
    '3': 4,
    '4': 5,
    '4#': 6,
    '5': 7,
    'b6': 8,
    '6': 9,
    'b7': 10,
    '7': 11,
}

"""
Makes scales with no key context
"""
class Scale(object):
    @staticmethod
    def make(root, scale_type):
        formula = FORMULAS[scale_type]
        note_names_twice = NOTE_NAMES * 2
        first_index = note_names_twice.index(root)
        note_names = note_names_twice[first_index:]
        notes = []
        for interval in formula:
            semitones = INTERVALS_TO_SEMITONES[interval]
            notes.append(note_names[semitones])
        return notes
