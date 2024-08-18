import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QSlider, QTextEdit, QHBoxLayout
from PyQt5.QtCore import Qt

class UFOControlPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Window settings
        self.setGeometry(300, 300, 500, 400)
        self.setWindowTitle('UFO Control Panel')

        # Main Layout
        mainLayout = QVBoxLayout()

        # Speed Control Slider
        self.speedSlider = QSlider(Qt.Horizontal)
        self.speedSlider.setMinimum(0)
        self.speedSlider.setMaximum(100)
        self.speedSlider.setValue(50)
        self.speedSlider.valueChanged.connect(self.speedChanged)

        mainLayout.addWidget(QLabel('Speed Control'))
        mainLayout.addWidget(self.speedSlider)

        # Navigation Buttons
        navLayout = QHBoxLayout()
        self.btnUp = QPushButton('Up')
        self.btnDown = QPushButton('Down')
        self.btnLeft = QPushButton('Left')
        self.btnRight = QPushButton('Right')

        self.btnUp.clicked.connect(lambda: self.moveUFO("up"))
        self.btnDown.clicked.connect(lambda: self.moveUFO("down"))
        self.btnLeft.clicked.connect(lambda: self.moveUFO("left"))
        self.btnRight.clicked.connect(lambda: self.moveUFO("right"))

        navLayout.addWidget(self.btnLeft)
        navLayout.addWidget(self.btnUp)
        navLayout.addWidget(self.btnDown)
        navLayout.addWidget(self.btnRight)

        mainLayout.addLayout(navLayout)

        # Status Display
        self.statusDisplay = QLabel('Status: Ready')
        mainLayout.addWidget(self.statusDisplay)

        # Radar Display (Placeholder)
        self.radarDisplay = QLabel('Radar Display Here')
        self.radarDisplay.setFixedSize(250, 250)
        self.radarDisplay.setStyleSheet("background-color: black;")
        mainLayout.addWidget(self.radarDisplay)

        # Command Log
        self.commandLog = QTextEdit()
        self.commandLog.setReadOnly(True)
        mainLayout.addWidget(self.commandLog)

        # Set the layout on the application's window
        self.setLayout(mainLayout)

    def speedChanged(self, value):
        self.updateStatus(f"Speed set to {value}%")

    def moveUFO(self, direction):
        self.commandLog.append(f"UFO moving {direction}")
        self.updateStatus(f"Moving {direction}")

    def updateStatus(self, message):
        self.statusDisplay.setText(f'Status: {message}')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = UFOControlPanel()
    ex.show()
    sys.exit(app.exec_())
