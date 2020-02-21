from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

from midi_extended.UtilityBox import *

class Key(QWidget):

    def __init__(self, player, note, volume=63, color='w'):
        super().__init__()
        self.player = player
        self.note = note
        self.volume = volume
        if is_cmajor_note(note):
            self.note_name = note_number_to_name(note, 's')
        else:
            self.note_name = note_number_to_name(note, 's') + '\n' + note_number_to_name(note, 'f')
        # print(self.note_name)
        self.color = color

        self.is_recording = False
        self.music_segment = None

        self.pressed_style = None
        self.default_style = None

        self.initUI()

    def change_volume(self, volume):
        self.volume = volume

    def set_note_signal_value(self):
        print('note ' + self.note)

    def initUI(self):
        self.keyBtn = QPushButton(self.note_name)
        self.note_font = QFont()
        self.note_font.setFamily('Times New Roman')
        self.note_font.setWeight(QFont.DemiBold)
        self.note_font.setPixelSize(14)
        self.keyBtn.setFont(self.note_font)
        self.keyBtn.setFixedHeight(250)
        self.keyBtn.setFixedWidth(50)
        self.keyBtn.setCursor(Qt.PointingHandCursor)
        self.keyBtn.pressed.connect(self.pressedKeyResponse)
        self.keyBtn.released.connect(self.releasedKeyResponse)
        self.keyLayout = QVBoxLayout()
        self.keyLayout.addWidget(self.keyBtn)
        self.setLayout(self.keyLayout)

        if self.color == 'w':
            self.default_style = '''QPushButton{background-color: white; color: black; border: 4px outset #828282;} 
                                  QPushButton:hover{background-color: #B5B5B5; color: black; border: 4px outset #828282;} 
                                  QPushButton:pressed{background-color: #CFCFCF; color: black; border: 4px inset #828282;}'''

            self.pressed_style = 'QPushButton{background-color: #CFCFCF; color: black; border: 4px inset #828282;}'
            self.setStyleSheet(self.default_style)

        elif self.color == 'b':
            self.default_style =  '''QPushButton{background-color: black; color: white; border: 4px outset #828282;} 
                                   QPushButton:hover{background-color: #4F4F4F; color: white; border: 4px outset #828282;} 
                                   QPushButton:pressed{background-color: #363636; color: white; border: 4px inset #828282;}'''

            self.pressed_style = 'QPushButton{background-color: #363636; color: white; border: 4px inset #828282;}'
            self.setStyleSheet(self.default_style)

        elif self.color == 'r':
            self.default_style = '''QPushButton{background-color: #FF4040; color: #FFE4E1; border: 4px outset #9C9C9C;} 
                                  QPushButton:hover{background-color: #FA8072; color: #8B2323; border: 4px outset #9C9C9C;} 
                                  QPushButton:pressed{background-color: #CD2626; color: #FFE4E1; border: 4px inset #9C9C9C;}'''
            self.pressed_style = 'QPushButton{background-color: #CD2626; color: #FFE4E1; border: 4px inset #9C9C9C;}'
            self.setStyleSheet(self.default_style)

        elif self.color == 'g':
            self.default_style = '''QPushButton{background-color: #008B45; color: #C0FF3E; border: 4px outset #9C9C9C;}
                                 QPushButton:hover{background-color: #9AFF9A; color: #6B8E23; border: 4px outset #9C9C9C;}
                                 QPushButton:pressed{background-color: #6E8B3D; color: #8FBC8F; border: 4px inset #9C9C9C;}'''
            self.pressed_style = 'QPushButton{background-color: #6E8B3D; color: #8FBC8F; border: 4px inset #9C9C9C;}'
            self.setStyleSheet(self.default_style)

        elif self.color == 'y':
            self.default_style = '''QPushButton{background-color: #FFFF00; color: #8B4513; border: 4px outset #CDCD00;}
                                 QPushButton:hover{background-color: #CDAA7D; color: #8B4513; border: 4px outset #EE9A49;}
                                 QPushButton:pressed{background-color: #8B7500; color: #FAFAD2; border: 4px inset #FFC125;}'''
            self.pressed_style = 'QPushButton{background-color: #8B7500; color: #FAFAD2; border: 4px inset #FFC125;}'
            self.setStyleSheet(self.default_style)

        # self.resize(3, 20)

    def pressedKeyResponse(self):
        # self.note_sig.emit()
        self.player.note_on(self.note, self.volume)

    def start_recording(self, music_segment):
        self.is_recording = True
        self.music_segment = music_segment

    def set_pressed_style(self):
        self.setStyleSheet(self.pressed_style)

    def set_default_style(self):
        self.setStyleSheet(self.default_style)

    def releasedKeyResponse(self):
        self.player.note_off(self.note, self.volume)

        if self.is_recording:
            self.music_segment.add_note(self.note, self.music_segment.length_per_note)
            if self.music_segment.window_on == True:
                self.music_segment.replot()
                '''
                self.segment_window = SegmentWindow(self.music_segment)
                self.segment_window.show()
                self.segment_window.move(1200, 30)
                '''