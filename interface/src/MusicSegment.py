import numpy as np
import time
import json

class MusicSegment:
    def __init__(self, metre, bpm, root_note, mode, total_length=128):
        self.metre_effects = {
            '1/4': (1, 4),
            '2/4': (2, 4),
            '3/4': (3, 4),
            '4/4': (4, 4),
            '3/8': (3, 8),
            '6/8': (6, 8)
        }

        self.metre = metre
        self.metre_numerator = self.metre_effects[self.metre][0]
        self.metre_denominator = self.metre_effects[self.metre][1]

        self.time_scale = 16

        self.bpm = bpm
        self.time_per_unit = ( 60 / self.bpm ) * 4
        self.total_length = total_length
        # self.length_per_note = length_per_note
        # self.matrix  = self.turn_into_numpy_matrix()

        self.root_note = root_note
        self.mode = mode
        # self.volume = volume

        self.msgs = []
        self.time_stamps = []
        # self.canvas = SegmentCanvas()
        self.window_on = False

        self.length_per_note = 1/2

        self.segment_window = None

    def set_length_per_note(self, lpn):
        self.length_per_note = lpn

    def add_note(self, note, raw_time):
        self.time_stamps.append(raw_time)
        msg = (note, raw_time, sum(self.time_stamps[:-1]))
        self.msgs.append(msg)
        # self.time_and_note.append((sum([msg[1] for msg in self.msgs]), note))

    def is_empty(self):
        return len(self.msgs) == 0

    def add_rest(self, raw_time):
        self.time_stamps.append(raw_time)
        msg = (-1, raw_time, sum(self.time_stamps[:-1]))
        self.msgs.append(msg)

    def delete_last_msg(self):
        self.msgs.pop(len(self.msgs)-1)
        self.time_stamps.pop(len(self.time_stamps)-1)

    def replot(self):
        self.segment_window.replot(self)

    def print_notes(self):
        for msg in self.msgs:
            print(msg)

    def set_volume(self, volume):
        self.volume = volume


    def play_music(self, player):
        for msg in self.msgs:
            if msg[0] == -1:
                time.sleep(msg[1] * self.time_per_unit)
            else:
                player.note_on(msg[0], self.volume)
                time.sleep(msg[1] * self.time_per_unit)
                player.note_off(msg[0], self.volume)

    def turn_into_numpy_matrix(self):
        # time_per_unit = 60 * 60 * 10 / self.bpm / 4
        notes = [msg[0] for msg in self.msgs]
        length_units = [round(msg[1] * self.metre_denominator) for msg in self.msgs]
        print(length_units)

        piano_roll = np.zeros((sum(length_units), 128))

        times = []
        for i in range(len(length_units)):
            time_point = 0
            time_point = sum(length_units[:i])
            times.append(time_point)

        for i in range(len(times) - 1):
            start = times[i]
            end = times[i + 1]
            note = notes[i]
            for time in range(start, end):
                piano_roll[time][note] = 1
        # plt.scatter(times, notes)
        # plt.show()
        # np.save(path, piano_roll)
        return piano_roll

    def save(self, path):
        segment_data = {
            'bpm': self.bpm,
            'metre': self.metre,
            'root_note': self.root_note,
            'mode': self.mode,
            'total_length': self.total_length,
            'msgs': self.msgs,
            'time_stamps': self.time_stamps
        }

        with open(path, 'w') as out:
            json.dump(segment_data, out)


    @staticmethod
    def load(path):
        with open(path, 'r') as f:
            data = json.load(f)
        # (self, metre, bpm, root_note, mode, total_length=128):
        segment =  MusicSegment(data['metre'], data['bpm'], data['root_note'], data['mode'], data['total_length'])
        segment.msgs = data['msgs']
        segment.time_stamps = data['time_stamps']
        return segment

if __name__ == '__main__':
    MusicSegment.load('../data/music_segments.json')