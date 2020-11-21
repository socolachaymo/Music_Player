import PyQt5.QtWidgets as qtw 
from PyQt5.QtGui import QIcon
import PyQt5.QtCore as core
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QMediaMetaData
import os

class MusicPlayer(qtw.QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(100,100,600,300)
        self.setWindowTitle('Music Player')
        self.setWindowIcon(QIcon('images/win_icon.jpg'))
        self.setLayout(qtw.QVBoxLayout())
        self.current_volume = 30
        self.buttons()
        self.lay_out('')
        self.show()

    def buttons(self):
        self.song = qtw.QPushButton('Choose a song', self, clicked=self.open_file)
        self.label = qtw.QLabel('')

        self.volume = qtw.QPushButton(self, clicked=self.mute)
        self.volume.setIcon(QIcon('images/volume.png'))
        
        self.next_s = qtw.QPushButton(self, clicked=self.next_song)
        self.next_s.setIcon(QIcon('images/next.png'))
        self.next_s.setIconSize(core.QSize(70,70))
        self.next_s.setEnabled(False)
        self.prev_s = qtw.QPushButton(self, clicked=self.pre_song)
        self.prev_s.setIcon(QIcon('images/prev.png'))
        self.prev_s.setIconSize(core.QSize(70,70))
        self.prev_s.setEnabled(False)
        self.play = qtw.QPushButton(self, clicked=self.play_music)
        self.play.setIcon(QIcon('images/play.png'))
        self.play.setIconSize(core.QSize(70,70))
        self.play.setEnabled(False)

        self.slider1 = qtw.QSlider(core.Qt.Horizontal)
        self.slider1.setRange(0,0)
        self.slider1.sliderMoved.connect(self.set_position)

        self.slider2 = qtw.QSlider(core.Qt.Horizontal)
        self.slider2.setRange(0, 100)
        self.slider2.sliderMoved.connect(self.value_changed)
        self.slider2.valueChanged.connect(self.volume_changed)

        self.hBox1 = qtw.QWidget()
        self.hBox1.setLayout(qtw.QHBoxLayout())
        self.hBox1.setContentsMargins(0,0,0,0)
        self.hBox1.layout().addWidget(self.volume)
        self.hBox1.layout().addWidget(self.slider2)

        self.hBox2 = qtw.QWidget()
        self.hBox2.setLayout(qtw.QHBoxLayout())
        self.hBox2.setContentsMargins(0,0,0,0)
        self.hBox2.layout().addWidget(self.prev_s)
        self.hBox2.layout().addWidget(self.play)
        self.hBox2.layout().addWidget(self.next_s)
        
        self.player = QMediaPlayer()
        self.player.positionChanged.connect(self.position_changed)
        self.player.durationChanged.connect(self.duration_changed)

    def lay_out(self, song_name):
        self.layout().addWidget(self.song)
        self.label.setText(song_name)
        self.label.setAlignment(core.Qt.AlignHCenter)
        self.layout().addWidget(self.label)
        self.layout().addWidget(self.slider1)
        self.layout().addWidget(self.hBox1)
        self.layout().addWidget(self.hBox2)

    def open_file(self):
        filename, _ = qtw.QFileDialog.getOpenFileName(self, 'Open File', 'D:/Music', 'Audio files (*.mp3 *.wav)')
        if filename != '':
            self.player.setMedia(QMediaContent(core.QUrl.fromLocalFile(filename)))
            self.volume_changed(self.current_volume)
            self.value_changed(self.current_volume)
            self.player.play()
            self.play.setEnabled(True)
            self.next_s.setEnabled(True)
            self.prev_s.setEnabled(True)
            sub_file = filename.split('/')
            self.dir_path = '/'.join(sub_file[:-1])
            self.song_list = [x for x in os.listdir(self.dir_path) if x[-3:] == 'mp3' or x[-3:] == 'wav']
            self.indx = self.song_list.index(sub_file[-1])
            self.song_name = self.song_list[self.indx]
            self.lay_out(self.song_name)
        else:
            self.lay_out('Not an audio file')

    def pre_song(self):
        if self.indx == 0:
            self.indx = len(self.song_list) - 1
            print(len(self.song_list), self.indx)
        else:
            self.indx -= 1
        self.song_name = self.song_list[self.indx]
        self.player.setMedia(QMediaContent(core.QUrl.fromLocalFile(self.dir_path + '/' + self.song_name)))
        self.volume_changed(self.current_volume)
        self.value_changed(self.current_volume)
        self.player.play()
        self.lay_out(self.song_name)
    
    def next_song(self):
        if self.indx == len(self.song_list) - 1:
            self.indx = 0
        else:
            self.indx += 1
        self.song_name = self.song_list[self.indx]
        self.player.setMedia(QMediaContent(core.QUrl.fromLocalFile(self.dir_path + '/' + self.song_name)))
        self.volume_changed(self.current_volume)
        self.value_changed(self.current_volume)
        self.player.play()
        self.lay_out(self.song_name)

    def play_music(self):
        if self.player.state() == QMediaPlayer.PlayingState:
            self.player.pause()
            self.play.setIcon(QIcon('images/pause.png'))
        else:
            self.player.play()
            self.play.setIcon(QIcon('images/play.png'))

    def set_position(self, position):
        self.player.setPosition(position)

    def position_changed(self, position):
        self.slider1.setValue(position)
    
    def duration_changed(self, duration):
        self.slider1.setRange(0, duration)
    
    def volume_changed(self, vol):
        self.current_volume = vol
        self.player.setVolume(vol)

    def value_changed(self, value):
        self.slider2.setValue(value)
    
    def mute(self):
        if self.player.isMuted():
            self.volume.setIcon(QIcon('images/volume.png'))
            self.player.setMuted(False)
        else:
            self.volume.setIcon(QIcon('images/mute.png'))
            self.player.setMuted(True)

app = qtw.QApplication([])
win = MusicPlayer()
app.exec_()
