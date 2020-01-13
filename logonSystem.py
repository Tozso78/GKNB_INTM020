import sys
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QTextEdit, QAction, QApplication
from PyQt5.QtGui import QIcon


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def faceRecognition(self):
        QMessageBox.information(self, 'Message',
                                "FaceRecognition", QMessageBox.Ok)

    def faceTraining(self):
        QMessageBox.information(self, 'Message',
                                "FaceTraining", QMessageBox.Ok)

    def report(self):
        QMessageBox.information(self, 'Message',
                                "Report", QMessageBox.Ok)

    def initUI(self):
        textEdit = QTextEdit()
        self.setCentralWidget(textEdit)

        # Arcfelismerés menü
        recogAct = QAction(QIcon('images/face-recognition.png'), 'Felismerés', self)
        recogAct.setShortcut('Ctrl+F')
        recogAct.setStatusTip('Arc felismerés')
        recogAct.triggered.connect(self.faceRecognition)

        # Traning menü
        trainingAct = QAction(QIcon('images/face-training.png'), 'Új személy hozzáadása', self)
        trainingAct.setShortcut('Ctrl+T')
        trainingAct.setStatusTip('Új személy hozzáadása')
        trainingAct.triggered.connect(self.faceTraining)

        # Riportok menü
        reportAct = QAction(QIcon('images/report.png'), 'Riport', self)
        reportAct.setShortcut('Ctrl+R')
        reportAct.setStatusTip('Riport')
        reportAct.triggered.connect(self.report)

        # Kilépés menü
        quitAct = QAction(QIcon('images/quit.png'), 'Kilépés', self)
        quitAct.setShortcut('Ctrl+Q')
        quitAct.setStatusTip('Kilépés')
        quitAct.triggered.connect(self.close)

        self.statusBar()
        toolbar = self.addToolBar('MainToolbar')
        toolbar.addAction(recogAct)
        toolbar.addAction(trainingAct)
        toolbar.addAction(reportAct)
        toolbar.addAction(quitAct)

        self.setGeometry(300, 300, 640, 480)
        self.setWindowTitle('Beléptető rendszer')
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())
