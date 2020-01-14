import sqlite3
from PyQt5.QtWidgets import QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout


class Report(QWidget):

    def __init__(self):
        super().__init__()
        self.tableWidget = QTableWidget()
        self.layout = QVBoxLayout()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Report - Belepesek')
        self.setGeometry(300, 300, 640, 480)


        self.createTable()

        # Add box layout, add table to box layout and add box layout to widget
        self.layout.addWidget(self.tableWidget)
        self.setLayout(self.layout)

        # Show widget
        self.show()

    def createTable(self):
        # Create table
        conn = sqlite3.connect('database/logonSystem.db')
        cur = conn.cursor()
        cur.execute('SELECT * FROM userLogon')
        rows = cur.fetchall()
        conn.close()

        currentRow = 0
        self.tableWidget.setRowCount(len(rows))
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setHorizontalHeaderLabels(['Név', 'Belépés dátuma'])

        for row in rows:
            self.tableWidget.setItem(currentRow, 0, QTableWidgetItem(row[0]))
            self.tableWidget.setItem(currentRow, 1, QTableWidgetItem(row[1]))
            currentRow = currentRow + 1
        self.tableWidget.move(0, 0)
