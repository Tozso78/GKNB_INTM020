import sys
from faceCapture import capture
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QInputDialog, QTextEdit, QAction, QApplication
from PyQt5.QtGui import QIcon


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def faceRecognition(self):
        QMessageBox.information(self, 'Message',
                                "FaceRecognition", QMessageBox.Ok)

    def faceTraining(self):
        name, ok = QInputDialog.getText(self,"Név megadása", "Név")
        if ok:
            capture(name)

    def report(self):
        QMessageBox.information(self, 'Message',
                                "Report", QMessageBox.Ok)

    def initUI(self):
        text_edit = QTextEdit()
        self.setCentralWidget(text_edit)

        # Arcfelismerés menü
        recog_act = QAction(QIcon('images/face-recognition.png'), 'Felismerés', self)
        recog_act.setShortcut('Ctrl+F')
        recog_act.setStatusTip('Arc felismerés')
        recog_act.triggered.connect(self.faceRecognition)

        # Traning menü
        training_act = QAction(QIcon('images/face-training.png'), 'Új személy hozzáadása', self)
        training_act.setShortcut('Ctrl+T')
        training_act.setStatusTip('Új személy hozzáadása')
        training_act.triggered.connect(self.faceTraining)

        # Riportok menü
        report_act = QAction(QIcon('images/report.png'), 'Riport', self)
        report_act.setShortcut('Ctrl+R')
        report_act.setStatusTip('Riport')
        report_act.triggered.connect(self.report)

        # Kilépés menü
        quit_act = QAction(QIcon('images/quit.png'), 'Kilépés', self)
        quit_act.setShortcut('Ctrl+Q')
        quit_act.setStatusTip('Kilépés')
        quit_act.triggered.connect(self.close)

        self.statusBar()
        toolbar = self.addToolBar('MainToolbar')
        toolbar.addAction(recog_act)
        toolbar.addAction(training_act)
        toolbar.addAction(report_act)
        toolbar.addAction(quit_act)

        self.setGeometry(300, 300, 640, 480)
        self.setWindowTitle('Beléptető rendszer')
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())
