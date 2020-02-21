from PyQt5.QtWidgets import QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize, Qt

class RecordBtn(QPushButton):
    def __init__(self, icon_path, tool_tip, short_cut):
        super().__init__()
        self.icon_path = icon_path
        self.tool_tip = tool_tip
        self.short_cut = short_cut
        self.initUI()

    def initUI(self):

        self.setIcon(QIcon(self.icon_path))
        self.setToolTip(self.tool_tip)
        self.setIconSize(QSize(45, 45))
        self.setFixedSize(QSize(60, 60))
        self.setStyleSheet('QPushButton{background: #FFEFDB; border: 3px outset #8B8378; border-radius: 15px;}' 
                           'QPushButton:hover{background: #CDC9C9; border: 3px outset #8B8378; border-radius: 15px;}' 
                           'QPushButton:pressed{background: #8B8682; border: 3px inset #8B8378; border-radius: 15px;}'
                           )
        self.setCursor(Qt.PointingHandCursor)
        self.setShortcut(self.short_cut)