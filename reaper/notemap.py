import os
from ..mode import Mode
from ..midi import get_midi_numbers_to_note_names

OUT_DIR = os.path.join(os.environ['HOME'], 'reaper-magic/notemaps')

class NoteMap(object):
    def __init__(self, mode, notes):
        self.mode = mode
        self.notes = notes

    @property
    def notes_to_intervals(self):
        return dict(zip(self.notes, self.mode.formula))

    @property
    def relative_filename(self):
        return 'modes/{mode_name}/{mode_root}-{mode_name}-notemap.txt'.format(
            mode_name=self.mode.mode_name,
            mode_root=self.mode.root,
        )

    @staticmethod
    def make(mode):
        notes = mode.normalized_notes
        return NoteMap(mode, notes)

    @staticmethod
    def make_all_dorian_note_maps():
        dorian_modes = Mode.make_all_dorian()
        return [NoteMap.make(mode) for mode in dorian_modes]

    @staticmethod
    def write_all_dorian_note_maps():
        for note_map in NoteMap.make_all_dorian_note_maps():
            note_map.write()

    def write(self):
        with open(self.get_filename(), 'wb') as out_file:
            out_file.writelines(
                map(lambda x: str(x) + '\n', NoteMapItem.make_all(self))
            )

    def get_filename(self):
        return os.path.join(OUT_DIR, self.relative_filename)

    def __str__(self):
        return 'NoteMap for {}'.format(self.relative_filename)

class NoteMapItem(object):
    def __init__(self, midi_number, interval_symbol):
        self.midi_number = midi_number
        self.interval_symbol = interval_symbol

    def __str__(self):
        return '{} {}'.format(self.midi_number, self.interval_symbol)

    @staticmethod
    def make_all(note_map):
        return filter(bool, [
            NoteMapItem(midi_number, note_map.notes_to_intervals[note_name])
            if note_name in note_map.notes_to_intervals.keys()
            else None
            for midi_number, note_name in get_midi_numbers_to_note_names()
        ])

