#!/bin/env python

NOTE_NAMES = 'C C# D D# E F F# G G# A A# B'.split()

IONIAN_FORMULA  =    '1	2	3	4	5	6	7	1'.split()
DORIAN_FORMULA =     '1	2	b3	4	5	6	b7	1'.split()
PHRYGIAN_FORMULA =   '1	b2	b3	4	5	b6	b7	1'.split()
LYDIAN_FORMULA =     '1	2	3	#4	5	6	7	1'.split()
MIXOLYDIAN_FORMULA = '1	2	3	4	5	6	b7	1'.split()
AEOLIAN_FORMULA =    '1	2	b3	4	5	b6	b7	1'.split()
LOCRIAN_FORMULA =    '1	b2	b3	4	b5	b6	b7	1'.split()

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

def make_scale(root, formula):
    note_names_twice = NOTE_NAMES * 2
    first_index = note_names_twice.index(root)
    note_names = note_names_twice[first_index:]
    notes = []
    for interval in formula:
        semitones = INTERVALS_TO_SEMITONES[interval]
        notes.append(note_names[semitones])
    return notes

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

# TODO: Assumes first note is correct, fix that
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

def make_key(key):
    key_name, key_quality = key
    key_root = key_name
    if 'b' in key_name:
        key_name = get_sharp_enharmonic(key_name)
    if key_quality == 'major':
        return correct_enharmonics(key, make_scale(key_name, IONIAN_FORMULA))
    if key_quality == 'minor':
        return correct_enharmonics(key, make_scale(key_name, AEOLIAN_FORMULA))

# note (note_name, octave)
MIDI_NUMBERS_TO_NOTES = [
    [21, ('A', 0)],
    [22, ('A#', 0)],
    [23, ('B', 1)],
    [24, ('C', 1)],
    [25, ('C#', 1)],
    [26, ('D', 1)],
    [27, ('D#', 1)],
    [28, ('E', 1)],
    [29, ('F', 1)],
    [30, ('F#', 1)],
    [31, ('G', 1)],
    [32, ('G#', 1)],
]

def add_actaves(midi_numbers_to_notes, octaves_up):
    res = []
    for midi_number, note_octave in midi_numbers_to_notes:
        note, octave = note_octave
        res.append([midi_number + (octaves_up * 12), (note, octave + octaves_up)])
    return res

"""
Returns all the note numbers in the MIDI spec, paired up with their corresponding interpretation (note name and octave)
"""
def get_midi_numbers_to_notes():
    exaggerated_range_midi_numbers_to_notes = \
        add_actaves(MIDI_NUMBERS_TO_NOTES, -1) + \
        MIDI_NUMBERS_TO_NOTES + \
        add_actaves(MIDI_NUMBERS_TO_NOTES, 1) + \
        add_actaves(MIDI_NUMBERS_TO_NOTES, 2) + \
        add_actaves(MIDI_NUMBERS_TO_NOTES, 3) + \
        add_actaves(MIDI_NUMBERS_TO_NOTES, 4) + \
        add_actaves(MIDI_NUMBERS_TO_NOTES, 5) + \
        add_actaves(MIDI_NUMBERS_TO_NOTES, 6) + \
        add_actaves(MIDI_NUMBERS_TO_NOTES, 7)
    def in_range(number_to_note):
        midi_number, _note_octave = number_to_note
        return midi_number > 20 and midi_number <= 108
    return filter(in_range, exaggerated_range_midi_numbers_to_notes)
