from key import Key
from scale import Scale
from mode import Mode

if __name__ == '__main__':
    scale = Key.make('C', 'major').notes
    mode = Mode.make(scale, 'dorian')
    print(mode)
