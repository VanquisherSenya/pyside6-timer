# Timer (Minimum viable product) by VanquisherSenya
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QLabel,
    QWidget,
    QVBoxLayout,
    QTimeEdit,
    QMenu,
    QSystemTrayIcon,
)
from PySide6.QtCore import Qt, QTimer, QUrl, QTime
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtGui import QAction, QIcon, QFont
import sys


class Window(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initializeUI()

    def initializeUI(self):
        self.setUpMainWindow()
        self.setLayout()
        self.systemTray()
        self.show()

    def systemTray(self):
        self.tray_icon = QIcon('sources/icon.png')
        self.tray = QSystemTrayIcon()
        self.tray.setIcon(self.tray_icon)

        self.tray_menu = QMenu()
        self.tray.setContextMenu(self.tray_menu)

        self.show_action = QAction('Show')
        self.quit_action = QAction('Exit')
        self.quit_action.triggered.connect(sys.exit)
        self.show_action.triggered.connect(self.show)
        self.show_action.triggered.connect(self.tray.hide)
        self.tray_menu.addAction(self.show_action)
        self.tray_menu.addAction(self.quit_action)

    # configure layout of ui elements (widgets)
    def setLayout(self):
        layout = QVBoxLayout()
        layout.addWidget(self.timer_lbl)
        layout.addWidget(self.edit_time)
        layout.addWidget(self.start_stop_btn)
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def setUpMainWindow(self):
        self.setWindowTitle('Timer')
        # add timer to app and set update interval (1000 = 1 sec)
        self.timer = QTimer()
        # fixed size of app and window location on desktop
        self.setGeometry(960, 540, 0, 0)
        self.setFixedSize(150, 200)

        self.timer_lbl = QLabel('00:00')
        self.timer_lbl.setFont(QFont('', 30))
        self.timer_lbl.setAlignment(Qt.AlignCenter)
        # widget for input integers
        self.edit_time = QTimeEdit()
        self.edit_time.setMaximumTime(QTime(0, 61, 61, 0))
        self.edit_time.setDisplayFormat('mm:ss')
        # widget for start/stop button
        self.start_stop_btn = QPushButton('start')
        self.start_stop_btn.setCheckable(True)

        self.edit_time.timeChanged.connect(self.editTimeFunc)
        self.timer.timeout.connect(self.timerFunc)
        self.start_stop_btn.clicked.connect(self.startStop)

    # basic input entry
    def editTimeFunc(self, time):
        self.time = time
        self.counter = self.time.minute() * 60 + self.time.second()
        self.old_count = self.counter
        self.timer_lbl.setText('%02d:%02d' % (self.counter // 60, self.counter % 60))

    # main logic of app, a timer, which
    # can stop and play specific sound if time is out
    def timerFunc(self):
        self.sound()
        try:
            self.counter -= 1
            self.timer_lbl.setText('%02d:%02d' % (self.counter // 60, self.counter % 60))
            if self.counter == 0:
                self.show()
                self.tray.hide()
                self.start_stop_btn.toggle()
                self.start_stop_btn.setText('start')
                self.counter = self.old_count  # start old timer with no changes in QTimeEdit spinbox
                self.timer_lbl.setText('%02d:%02d' % (self.old_count // 60, self.old_count % 60))
                self.edit_time.setDisabled(False)
                self.ding.play()
                self.timer.stop()
            elif self.counter < 0:
                self.start_stop_btn.toggle()
                self.start_stop_btn.setText('start')
                self.counter = self.old_count  # start old timer with no changes in spinbox
                self.timer_lbl.setText('%02d:%02d' % (self.old_count // 60, self.old_count % 60))
                self.edit_time.setDisabled(False)
                self.ding.play()
                self.timer.stop()
        # if the user has not entered any values - stop timer
        except AttributeError:
            self.start_stop_btn.toggle()
            self.start_stop_btn.setText('start')
            self.edit_time.setDisabled(False)
            self.ding.play()
            self.timer.stop()

    # start/stop function for one button
    def startStop(self, checked):
        if checked:
            self.start_stop_btn.setText('stop')
            self.timer.start(1000)
            self.edit_time.setDisabled(True)
        else:
            self.start_stop_btn.setText('start')
            self.edit_time.setDisabled(False)
            self.timer.stop()

    # add ding.wav sound file to finish state of timer
    def sound(self):
        self.ding = QMediaPlayer()
        self.audioOutput = QAudioOutput()
        self.ding.setAudioOutput(self.audioOutput)
        self.ding.setSource(QUrl.fromLocalFile('sources/ding.wav'))

    def closeEvent(self, event):
        self.tray.setVisible(True)
        event.ignore()
        self.hide()


app = QApplication()
window = Window()
app.exec()
