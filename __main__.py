from key import Key
from scale import Scale
from mode import Mode

if __name__ == '__main__':
    dorian_modes = Mode.make_all_dorian()
    for mode in dorian_modes:
        print(mode)
