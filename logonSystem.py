import sys
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QTextEdit, QAction, QApplication
from PyQt5.QtGui import QIcon

class ChildWindow(QMainWindow):
    def __init__(self, parent):
        super(ChildWindow, self).__init__(parent)
    
       
        
class MainWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()
        
        self.initUI()
    
    def open_new_window(self):
        self.window_to_open = ChildWindow(self)
        self.window_to_open.show()
        
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

        recogAct = QAction(QIcon('images/face-recognition.png'), 'Recognition', self)
        recogAct.setShortcut('Ctrl+F')
        recogAct.setStatusTip('Face recognition')
        recogAct.triggered.connect(self.open_new_window)
        
        trainingAct = QAction(QIcon('images/face-training.png'), 'Training', self)
        trainingAct.setShortcut('Ctrl+T')
        trainingAct.setStatusTip('Face training')
        trainingAct.triggered.connect(self.faceTraining)
        
        reportAct = QAction(QIcon('images/report.png'), 'Report', self)
        reportAct.setShortcut('Ctrl+R')
        reportAct.setStatusTip('Report')
        reportAct.triggered.connect(self.report)
        
        quitAct = QAction(QIcon('images/quit.png'), 'Quit', self)
        quitAct.setShortcut('Ctrl+Q')
        quitAct.setStatusTip('Quit')
        quitAct.triggered.connect(self.close)

        self.statusBar()
        toolbar = self.addToolBar('MainToolbar')
        toolbar.addAction(recogAct)
        toolbar.addAction(trainingAct)
        toolbar.addAction(reportAct)
        toolbar.addAction(quitAct)
        
        self.setGeometry(300, 300, 640, 480)
        self.setWindowTitle('Logonsystem')    
        self.show()
  
        
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())