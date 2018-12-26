from scale import Scale

# There are 12 major keys
# Three of the major keys have two different spellings
# So, there are 15 major key spellings
# In the same way, there are 15 minor key spellings
# I've stolen these key spellings from the circle of fifths found at
# http://www.wkiri.com/today/?p=2553
# Go and read the thing to actually understand why this is like this
MAJOR_KEY_SPELLINGS = 'C G D A E B Cb F# Gb C# Db Ab Eb Bb F'.split()
MINOR_KEY_SPELLINGS = 'A E B F# C# G# Ab D# Eb Bb A# F C D D'.split()
MAJOR_KEYS_WITH_SHARPS = 'G D A E B F# C#'.split()
MAJOR_KEYS_WITH_FLATS = 'F Bb Eb Ab Db Gb Cb'.split()
MINOR_KEYS_WITH_SHARPS = 'E B F# C# G# D# A#'.split()
MINOR_KEYS_WITH_FLATS = 'D G C F Bb Eb Ab'.split()

def get_sharp_enharmonic(note):
    return {
        'Db': 'C#',
        'Eb': 'D#',
        'Gb': 'F#',
        'Ab': 'G#',
        'Bb': 'A#',
        'Cb': 'B',
        'F': 'E#',
        'C': 'B#',
    }[note]

def get_flat_enharmonic(note):
    return {
        'C#': 'Db',
        'D#': 'Eb',
        'F#': 'Gb',
        'G#': 'Ab',
        'A#': 'Bb',
        'B': 'Cb',
        'E': 'Fb',
    }[note]

def get_next_base_note_name(note):
    base_note_names = 'ABCDEFG'
    base_note_names_twice = base_note_names * 2
    return base_note_names_twice[base_note_names_twice.index(note) + 1]

def correct_enharmonics(key, scale):
    key_root, key_quality = key
    prev_base_note_name = None
    notes = [key_root]
    prev_base_note_name = key_root.replace('#', '').replace('b', '')
    for note in scale[1:]:
        expected_base_note_name = None
        if prev_base_note_name:
            expected_base_note_name = get_next_base_note_name(prev_base_note_name)
        current_base_note_name = note.replace('#', '').replace('b', '')
        corrected_note_name = note
        if prev_base_note_name and current_base_note_name != expected_base_note_name:
            if key_quality == 'major' and key_root in MAJOR_KEYS_WITH_SHARPS:
                corrected_note_name = get_sharp_enharmonic(note)
            elif key_quality == 'major' and key_root in MAJOR_KEYS_WITH_FLATS:
                corrected_note_name = get_flat_enharmonic(note)
            elif key_quality == 'minor' and key_root in MINOR_KEYS_WITH_SHARPS:
                corrected_note_name = get_sharp_enharmonic(note)
            elif key_quality == 'minor' and key_root in MINOR_KEYS_WITH_FLATS:
                corrected_note_name = get_flat_enharmonic(note)
            else:
                raise Exception('Should never get here')
        notes.append(corrected_note_name)
        prev_base_note_name = corrected_note_name.replace('#', '').replace('b', '')
    return notes

class Key(object):
    def __init__(self, key_root, key_quality, notes):
        self.key_root = key_root
        self.key_quality = key_quality
        self.notes = notes

    @staticmethod
    def make(key_root, key_quality):
        key_name = key_root
        if 'b' in key_name:
            key_name = get_sharp_enharmonic(key_name)
        if key_quality == 'major':
            notes = correct_enharmonics((key_root, key_quality), Scale.make(key_name, 'ionian').notes)
        elif key_quality == 'minor':
            notes = correct_enharmonics((key_root, key_quality), Scale.make(key_name, 'aeolian').notes)
        else:
            raise Exception('Should never get here')
        return Key(key_root, key_quality, notes)

    @staticmethod
    def make_all():
        return [
            Key.make('C', 'major'),
            Key.make('A', 'minor'),
        ] + \
            [Key.make(key, 'major') for key in MAJOR_KEYS_WITH_SHARPS] + \
            [Key.make(key, 'major') for key in MAJOR_KEYS_WITH_FLATS] + \
            [Key.make(key, 'minor') for key in MINOR_KEYS_WITH_SHARPS] + \
            [Key.make(key, 'minor') for key in MINOR_KEYS_WITH_FLATS]

    def __str__(self):
        return self.key_root + ' ' + self.key_quality + ' key -> ' + ' '.join(self.notes)
