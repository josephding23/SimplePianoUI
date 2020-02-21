import numpy as np
import time
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import QRect, pyqtSignal, QPoint, Qt
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.path import Path
import matplotlib.patches as patches
from PyQt5.QtWidgets import *
import os
import sys
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from midi_extended.UtilityBox import *

from midi_extended.UtilityBox import *

def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS',
                        os.path.dirname(os.path.abspath(__file__))
                        )
    return os.path.join(base_path, relative_path)

class SegmentCanvas(FigureCanvas):

    def __init__(self, width=10, height=7,  dpi=100):
        fig = Figure(figsize = (width, height), dpi=dpi, facecolor='#FFFAF0')
        FigureCanvas.__init__(self, fig)
        self.axes = fig.add_subplot(111)
        self.axes.set_xlim(0, 16)
        self.axes.set_xticks(np.arange(0, 16, 1))
        self.axes.set_ylim(60, 72)
        # self.axes.set_yticks(np.arange(min_note, max_note, 1))

    def plot(self, msgs):
        try:
            final_time = msgs[-1][2] + msgs[-1][1]
            min_note_in_msgs = 60
            for msg in msgs:
                if msg[0] != -1 and msg[0] < min_note_in_msgs:
                    min_note_in_msgs = msg[0]
            min_note = min_note_in_msgs - 6
            # min_note = min([min_note_in_msgs - 6, 60])
            max_note = max([msg[0] for msg in msgs]) + 6
            # max_note = max([max([msg[0] for msg in msgs]) + 6, 72])
        except:
            final_time = 0.5
            min_note = 60
            max_note = 72
        note_texts = [note_number_to_name_ignore_semitones(note) for note in range(min_note, max_note+1)]
        self.axes.set_xlim(0, 16)
        self.axes.set_xticks(np.arange(0, 16, 1))
        self.axes.set_ylim(min_note, max_note)
        self.axes.set_yticks(np.arange(min_note, max_note, 1))
        self.axes.tick_params(axis='both', which='minor', labelsize=10)
        # print(note_texts)
        self.axes.set_yticklabels(note_texts)
        bar_width = 0.5
        for msg in msgs:
            note = msg[0]
            if note == -1:
                pass
            else:
                length = msg[1]
                time = msg[2]
                verts = [
                    (time, note - bar_width/2),
                    (time, note + bar_width/2),
                    (time + length, note + bar_width/2),
                    (time + length, note - bar_width/2),
                    (time, note - bar_width/2)
                ]
                codes = [
                    Path.MOVETO,
                    Path.LINETO,
                    Path.LINETO,
                    Path.LINETO,
                    Path.CLOSEPOLY,
                ]
                path = Path(verts, codes)
                patch = patches.PathPatch(path, facecolor='#CD853F', lw=1)
                self.axes.add_patch(patch)

        # self.axes.plot(times, notes)


class SegmentWindow(QMainWindow):
    def __init__(self, music_segment):
        super().__init__()
        self.music_segment = music_segment

        self.maximized = False
        self.btn_style = \
            'QPushButton{background: #EEDD82; color: #8B4513; border: 3px outset #CDAA7D; border-radius: 3px;}' \
            'QPushButton:hover{background: #8B6914; color: #FFF68F; border: 3px outset 	#CDBE70; border-radius: 3px;}' \
            'QPushButton:pressed{background: #F4A460; color: #FFD39B; border: 3px inset #8B4513; border-radius: 3px;}'

        self.initUI()

    def initUI(self):

        self.graphic_view = QGraphicsView()
        self.graphic_view.setObjectName('graphic_view')

        self.segment_canvas = SegmentCanvas()
        self.segment_canvas.plot(self.music_segment.msgs)
        graphic_scene = QGraphicsScene()
        graphic_scene.addWidget(self.segment_canvas)
        self.graphic_view.setScene(graphic_scene)
        self.graphic_view.show()
        # self.graphic_view.setFixedSize(400, 700)
        self.graphic_window = QMainWindow()
        self.graphic_window.setCentralWidget(self.graphic_view)

        self.maximizeBtn = QPushButton('Expand / Shrink View')
        self.btnFont = QFont('Times', 12, QFont.DemiBold)
        self.btnFont.setStyleHint(QFont.OldEnglish)

        self.maximizeBtn.setFont(self.btnFont)
        self.maximizeBtn.setStyleSheet(self.btn_style)
        self.maximizeBtn.setMinimumHeight(30)
        # self.maximizeBtn.setMaximumWidth(800)
        self.maximizeBtn.clicked.connect(self.change_window_size)

        self.scrollArea = QScrollArea()
        self.scrollAreaContent = QMainWindow()
        # self.scrollAreaContent.setGeometry(QRect(0, 0, 400, 700))
        self.scrollLayout = QVBoxLayout()
        # self.scrollLayout.setSpacing(5)
        # self.scrollLayout.setContentsMargins(5, 10, 5, 0)

        self.scrollLayout.addWidget(self.maximizeBtn)
        self.scrollLayout.addWidget(self.graphic_window)

        self.scrollAreaContent.setLayout(self.scrollLayout)

        self.scrollArea.setLayout(self.scrollLayout)
        self.setCentralWidget(self.scrollArea)
        self.setWindowIcon(QIcon(resource_path('icon/gramophone.png')))
        self.setWindowTitle('MusicCritique Notes Display')
        self.setWindowFlags(Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint)

        self.move(1505, 125)
        self.resize(400, 770)
        self.show()

    def replot(self, music_segment):
        self.music_segment = music_segment
        self.graphic_view = QGraphicsView()
        self.graphic_view.setObjectName('graphic_view')

        self.segment_canvas = SegmentCanvas()
        self.segment_canvas.plot(self.music_segment.msgs)
        graphic_scene = QGraphicsScene()
        graphic_scene.addWidget(self.segment_canvas)
        self.graphic_view.setScene(graphic_scene)
        self.graphic_view.show()
        # self.graphic_view.setFixedSize(400, 700)
        self.graphic_window.setCentralWidget(self.graphic_view)

        self.show()

    def closeEvent(self, e):
        self.music_segment.window_on = False

    def change_window_size(self):
        if self.maximized == False:
            self.move(300, 125)
            self.resize(1000, 770)
            self.scrollLayout.setAlignment(Qt.AlignHCenter)
            self.maximized = True
        else:
            self.move(1505, 125)
            self.resize(400, 770)
            self.scrollLayout.setAlignment(Qt.AlignHCenter)
            self.maximized = False

