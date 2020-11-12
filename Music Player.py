import PyQt5.QtWidgets as qtw 
from PyQt5.QtGui import QIcon
import PyQt5.QtCore as core
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
import os

class MusicPlayer(qtw.QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(100,100,600,300)
        self.setWindowTitle('Music Player')
        self.setWindowIcon(QIcon('images/win_icon.jpg'))
        self.setLayout(qtw.QVBoxLayout())
        self.buttons()
        self.show()

    def buttons(self):
        song = qtw.QPushButton('Choose a song', self, clicked=self.open_file)
        # song.setGeometry(10,10,200,40)

        self.next_s = qtw.QPushButton(self)
        # self.next_s.setGeometry(360, 160, 90, 90)
        self.next_s.setIcon(QIcon('images/next.png'))
        self.next_s.setIconSize(core.QSize(80,80))
        self.prev_s = qtw.QPushButton(self)
        # self.prev_s.setGeometry(180, 160, 90, 90)
        self.prev_s.setIcon(QIcon('images/prev.png'))
        self.prev_s.setIconSize(core.QSize(80,80))
        self.play = qtw.QPushButton(self, clicked=self.play_music)
        # self.play.setGeometry(270, 160, 90, 90)
        self.play.setIcon(QIcon('images/play.png'))
        # self.play.setIcon(self.style().standardIcon(qtw.QStyle.SP_MediaVolume))
        self.play.setIconSize(core.QSize(80,80))
        self.play.setEnabled(False)

        self.slider = qtw.QSlider(core.Qt.Horizontal)
        self.slider.setRange(0,0)
        self.slider.sliderMoved.connect(self.set_position)
        print(self.slider.sliderPosition)
        self.label = qtw.QLabel()
        self.label.setSizePolicy(qtw.QSizePolicy.Preferred, qtw.QSizePolicy.Maximum)

        hBox1 = qtw.QWidget()
        hBox1.setLayout(qtw.QHBoxLayout())
        hBox1.setContentsMargins(0,0,0,0)
        hBox1.layout().addWidget(self.slider)
        hBox1.layout().addWidget(self.label)
        
        hBox2 = qtw.QWidget()
        hBox2.setLayout(qtw.QHBoxLayout())
        hBox2.setContentsMargins(0,0,0,0)
        hBox2.layout().addWidget(self.prev_s)
        hBox2.layout().addWidget(self.play)
        hBox2.layout().addWidget(self.next_s)

        self.layout().addWidget(song)
        self.layout().addWidget(hBox1)
        self.layout().addWidget(hBox2)

        
        self.player = QMediaPlayer()
        self.player.positionChanged.connect(self.position_changed)
        self.player.durationChanged.connect(self.duration_changed)
   
    def open_file(self):
        filename, _ = qtw.QFileDialog.getOpenFileName(self, 'Open File', 'D:', 'Audio files (*.mp3)')
        if filename != '':
            self.player.setMedia(QMediaContent(core.QUrl.fromLocalFile(filename)))
            self.player.setVolume(50)
            self.player.play()
            self.play.setEnabled(True)

    def play_music(self):
        if self.player.state() == QMediaPlayer.PlayingState:
            self.player.pause()
            print(self.slider.sliderPosition)
            self.play.setIcon(QIcon('images/pause.png'))
        else:
            self.player.play()
            self.play.setIcon(QIcon('images/play.png'))

    def position_changed(self, position):
        self.slider.setValue(position)
    
    def duration_changed(self, duration):
        self.slider.setRange(0, duration)
    
    def set_position(self, position):
        self.player.setPosition(position)

app = qtw.QApplication([])
win = MusicPlayer()
app.exec_()
