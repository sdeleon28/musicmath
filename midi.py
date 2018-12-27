class MidiNote(object):
    def __init__(self, note_name, octave):
        self.note_name = note_name
        self.octave = octave

    def __str__(self):
        return '{} - {}'.format(self.note_name, octave)

# note (note_name, octave)
MIDI_NUMBERS_TO_NOTES = [
    [21, MidiNote('A', 0)],
    [22, MidiNote('A#', 0)],
    [23, MidiNote('B', 1)],
    [24, MidiNote('C', 1)],
    [25, MidiNote('C#', 1)],
    [26, MidiNote('D', 1)],
    [27, MidiNote('D#', 1)],
    [28, MidiNote('E', 1)],
    [29, MidiNote('F', 1)],
    [30, MidiNote('F#', 1)],
    [31, MidiNote('G', 1)],
    [32, MidiNote('G#', 1)],
]

def add_actaves(midi_numbers_to_notes, octaves_up):
    res = []
    for midi_number, note in midi_numbers_to_notes:
        res.append([midi_number + (octaves_up * 12), MidiNote(note.note_name, note.octave + octaves_up)])
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

def get_midi_numbers_to_note_names():
    def unpack(number_to_note):
        number, note = number_to_note
        return [number, note.note_name]
    return map(unpack, get_midi_numbers_to_notes())
