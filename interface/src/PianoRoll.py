from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import QSize
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame.midi

from midi_extended.UtilityBox import *
from interface.src.Key import Key

class PianoRoll(QWidget):

    def __init__(self, player, volume, octave, mode, root_note_name, mode_display):
        super().__init__()
        self.setObjectName('PianoRoll')
        self.octave = octave
        self.volume = volume
        self.mode = mode
        self.mode_pattern = get_mode_dict()[self.mode[0]][self.mode[1]]
        self.mode_distance = [sum(self.mode_pattern[:index+1]) for index in range(len(self.mode_pattern))]

        self.root_note_name = root_note_name
        self.root_note_pos = raw_note_name_to_dist(root_note_name)

        self.mode_display = mode_display

        if self.mode[0] == 'Heptatonic':
            self.stable_distance = [ (self.root_note_pos + dist) % 12 for dist in [self.mode_distance[0], self.mode_distance[2], self.mode_distance[4]]]
            self.unstable_distance= [ (self.root_note_pos + dist) % 12 for dist in [self.mode_distance[1], self.mode_distance[3], self.mode_distance[5], self.mode_distance[6]]]
        else:
            self.stable_distance = [(self.root_note_pos + dist) % 12 for dist in
                                    [self.mode_distance[0], self.mode_distance[2], self.mode_distance[4]]]
            self.unstable_distance = [(self.root_note_pos + dist) % 12 for dist in
                                      [self.mode_distance[1], self.mode_distance[3]]]

        self.is_recording = False
        self.music_segment = None

        self.white_notes_margin = [0, 2, 2, 1, 2, 2, 2]
        self.black_notes_margin = [1, 2, 3, 2, 2]

        self.white_notes_distance = [[0, 2, 4, 5, 7, 9, 11], [12, 14, 16, 17, 19, 21, 23, 24]]
        self.black_notes_distance = [[1, 3, 6, 8, 10], [13, 15, 18, 20, 22]]

        self.blackKeysList = [[], []]
        self.whiteKeysList = [[], []]

        self.pressed_time = 0
        self.release_time = 0

        self.start_note = 60 + (self.octave - 4) * 12

        self.player = player

        self.initUI()

    def start_recording(self, music_segment):
        self.is_recording = True
        self.music_segment = music_segment
        for group in range(2):
            for black_key in self.blackKeysList[group]:
                black_key.start_recording(music_segment)
            for white_key in self.whiteKeysList[group]:
                white_key.start_recording(music_segment)

    def end_recording(self):
        self.is_recording = False
        self.music_segment = None
        for group in range(2):
            for black_key in self.blackKeysList[group]:
                black_key.is_recording = False
            for white_key in self.whiteKeysList[group]:
                white_key.is_recording = False

    def delete_player(self):
        try:
            self.player.close()
            pygame.midi.quit()
        except:
            pass

    def change_volume(self, volume):
        self.volume = volume
        for group in range(2):
            for black_key in self.blackKeysList[group]:
                black_key.change_volume(self.volume)
            for white_key in self.whiteKeysList[group]:
                white_key.change_volume(self.volume)

    def change_instrument(self, instr):
        self.instr = instr
        self.player.set_instrument(self.instr)

    def initUI(self):
        self.blackKeysBoxes = [QHBoxLayout(), QHBoxLayout()]
        self.whiteKeysBoxes = [QHBoxLayout(), QHBoxLayout()]
        self.octaveRollBoxes = [QVBoxLayout(), QVBoxLayout()]

        for group in range(2):
            for index in range(len(self.black_notes_distance[group])):
                note = self.start_note + self.black_notes_distance[group][index]

                if self.mode_display == True:
                    if note % 12 == self.stable_distance[0]:
                        new_key = Key(self.player, note, self.volume, 'y')
                        self.blackKeysList[group].append(new_key)
                    elif note % 12 in self.stable_distance:
                        new_key = Key(self.player, note, self.volume, 'r')
                        self.blackKeysList[group].append(new_key)
                    elif note % 12 in self.unstable_distance:
                        new_key = Key(self.player, note, self.volume, 'g')
                        self.blackKeysList[group].append(new_key)
                    else:
                        new_key = Key(self.player, note, self.volume, 'b')
                        self.blackKeysList[group].append(new_key)
                else:
                    new_key = Key(self.player, note, self.volume, 'b')
                    self.blackKeysList[group].append(new_key)

            for index in range(len(self.white_notes_distance[group])):
                note = self.start_note + self.white_notes_distance[group][index]
                if self.mode_display == True:
                    if note % 12 == self.stable_distance[0]:
                        new_key = Key(self.player, note, self.volume, 'y')
                        self.whiteKeysList[group].append(new_key)
                    elif note % 12 in self.stable_distance:
                        new_key = Key(self.player, note, self.volume, 'r')
                        self.whiteKeysList[group].append(new_key)
                    elif note % 12 in self.unstable_distance:
                        new_key = Key(self.player, note, self.volume, 'g')
                        self.whiteKeysList[group].append(new_key)
                    else:
                        new_key = Key(self.player, note, self.volume, 'w')
                        self.whiteKeysList[group].append(new_key)
                else:
                    new_key = Key(self.player, note, self.volume, 'w')
                    self.whiteKeysList[group].append(new_key)

            for btn in self.blackKeysList[group]:
                self.blackKeysBoxes[group].addWidget(btn)
            self.blackKeysBoxes[group].setStretch(0, 2)
            self.blackKeysBoxes[group].setStretch(1, 4)
            self.blackKeysBoxes[group].setStretch(2, 2)
            self.blackKeysBoxes[group].setStretch(3, 2)
            self.blackKeysBoxes[group].setStretch(4, 2)

            for btn in self.whiteKeysList[group]:
                self.whiteKeysBoxes[group].addWidget(btn)
            self.whiteKeysBoxes[group].setSpacing(20)
            self.octaveRollBoxes[group].addLayout(self.blackKeysBoxes[group])
            self.octaveRollBoxes[group].addLayout(self.whiteKeysBoxes[group])
            self.octaveRollBoxes[group].setSpacing(2)

        self.whiteKeysBoxes[0].setContentsMargins(0, 0, 0, 0)
        self.whiteKeysBoxes[1].setContentsMargins(0, 0, 0, 0)
        self.whiteKeysBoxes[0].addSpacing(25)
        self.whiteKeysBoxes[1].addSpacing(25)
        self.blackKeysBoxes[0].setContentsMargins(50, 0, 55, 0)
        self.blackKeysBoxes[1].setContentsMargins(50, 0, 155, 0)

        self.wholeLayout = QHBoxLayout()
        self.wholeLayout.addLayout(self.octaveRollBoxes[0])
        self.wholeLayout.addLayout(self.octaveRollBoxes[1])
        self.wholeLayout.setStretch(0, 7)
        self.wholeLayout.setStretch(1, 8)
        self.wholeLayout.setSpacing(1)
        self.wholeLayout.setContentsMargins(10, 10, 10, 10)
        self.setLayout(self.wholeLayout)
        self.setFixedSize(QSize(1500, 550))


    def keyPressed(self, color, group, index):
        if color == 'white':
            self.whiteKeysList[group][index].set_pressed_style()

        elif color == 'black':
            self.blackKeysList[group][index].set_pressed_style()

    def keyRelease(self, color, group, index):
        if color == 'white':
            self.whiteKeysList[group][index].set_default_style()

        elif color == 'black':
            self.blackKeysList[group][index].set_default_style()

    def get_note(self, color, group, index):
        if color == 'white':
            return self.whiteKeysList[group][index].note
        elif color == 'black':
            return self.blackKeysList[group][index].note
