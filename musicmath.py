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
