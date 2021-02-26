import sys
from random import randint

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QTableWidgetItem, QAbstractScrollArea
from PyQt5.QtWidgets import QWidget
import sqlite3

from PyQt5.uic.properties import QtWidgets

conn = sqlite3.connect("coffee.sqlite")  # или :memory: чтобы сохранить в RAM
cursor = conn.cursor()

# Создание таблицы
cursor.execute("CREATE TABLE IF NOT EXISTS `coffee` (`id` INTEGER  PRIMARY KEY AUTOINCREMENT NOT "
               "NULL, `Name` varchar(255) NOT NULL, RawState varchar(255) NOT NULL, DType varchar("
               "255) NOT NULL, Desc varchar(255) NOT NULL, Cost INTEGER, V INTEGER)")


class Widget(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("main.ui", self)
        cursor = conn.cursor()
        a = conn.execute("SELECT * FROM coffee").fetchall()
        for i in a:
            self.addRow(i[0], i[1], i[2], i[3], i[4], i[5], i[6])
        self.tableWidget.resizeColumnsToContents()

        s = 0
        for i in range(self.tableWidget.columnCount()):
            s += self.tableWidget.columnWidth(i)

        self.tableWidget.setFixedWidth(s + 30)
        self.setFixedSize(self.tableWidget.width(), self.height())

    def addRow(self, ID, Name, RawState, DType, Desc, Cost, V):
        rowPosition = self.tableWidget.rowCount()
        self.tableWidget.insertRow(rowPosition)
        self.tableWidget.setItem(rowPosition, 0, QTableWidgetItem(str(ID)))
        self.tableWidget.setItem(rowPosition, 1, QTableWidgetItem(Name))
        self.tableWidget.setItem(rowPosition, 2, QTableWidgetItem(RawState))
        self.tableWidget.setItem(rowPosition, 3, QTableWidgetItem(DType))
        self.tableWidget.setItem(rowPosition, 4, QTableWidgetItem(Desc))
        self.tableWidget.setItem(rowPosition, 5, QTableWidgetItem(str(Cost) + " руб"))
        self.tableWidget.setItem(rowPosition, 6, QTableWidgetItem(str(V) + " г"))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Widget()
    ex.show()
    sys.exit(app.exec_())
