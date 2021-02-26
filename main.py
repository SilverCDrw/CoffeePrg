import sys
from random import randint

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QTableWidgetItem, QAbstractScrollArea, QComboBox, \
    QTableWidget, QLabel
from PyQt5.QtWidgets import QWidget
import sqlite3

from PyQt5.uic.properties import QtWidgets

conn = sqlite3.connect("coffee.sqlite")  # или :memory: чтобы сохранить в RAM
cursor = conn.cursor()

# Создание таблицы
cursor.execute("CREATE TABLE IF NOT EXISTS `coffee` (`id` INTEGER  PRIMARY KEY AUTOINCREMENT NOT "
               "NULL, `Name` varchar(255) NOT NULL, RawState varchar(255) NOT NULL, DType varchar("
               "255) NOT NULL, Desc varchar(255) NOT NULL, Cost INTEGER, V INTEGER)")


class SecondWidget(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("addEditCoffeeForm.ui", self)
        self.setWindowTitle("Edit")
        self.show()

    def getData(self, index):
        if index == "" or not self.IDlist.isEnabled():
            return
        a = conn.execute(f"SELECT * FROM coffee WHERE ID = {index}").fetchall()[0]
        self.SaveButton.setEnabled(True)
        self.DeleteButton.setEnabled(True)
        self.VV.setEnabled(True)
        self.VV.setValue(a[6])
        self.Cost.setEnabled(True)
        self.Cost.setValue(a[5])
        self.Desc.setEnabled(True)
        self.Desc.setText(a[4])
        self.Stepen.setEnabled(True)
        self.Stepen.setText(a[2])
        self.Name.setEnabled(True)
        self.Name.setText(a[1])
        self.Zern.setEnabled(True)
        self.Zern.setCurrentText(a[3])


class Widget(QWidget):

    def reloadDataBase(self):
        while self.tableWidget.rowCount() > 0:
            self.tableWidget.removeRow(0)
        self.second.IDlist.setEnabled(False)
        while self.second.IDlist.count() > 0:
            self.second.IDlist.removeItem(0)
        self.second.IDlist.setEnabled(True)
        a = conn.execute("SELECT * FROM coffee").fetchall()
        for i in a:
            self.addRow(i[0], i[1], i[2], i[3], i[4], i[5], i[6])
        self.tableWidget.resizeColumnsToContents()
        s = 0
        IDs = list(map(lambda x: str(x[0]), a))
        for i in range(self.tableWidget.columnCount()):
            s += self.tableWidget.columnWidth(i)
        self.second.IDlist.addItems(IDs)
        self.tableWidget.setFixedWidth(s + 30)
        self.setFixedSize(self.tableWidget.width(), self.height())

    def delete(self):
        conn.execute(f"DELETE FROM coffee WHERE ID={str(self.second.IDlist.currentText())}")
        conn.commit()
        self.second.SaveButton.setEnabled(False)
        self.second.DeleteButton.setEnabled(False)
        self.second.VV.setEnabled(False)
        self.second.Cost.setEnabled(False)
        self.second.Desc.setEnabled(False)
        self.second.Stepen.setEnabled(False)
        self.second.Name.setEnabled(False)
        self.second.Zern.setEnabled(False)
        self.reloadDataBase()

    def save(self):
        id = str(self.second.IDlist.currentText())
        name = self.second.Name.text()
        st = self.second.Stepen.text()
        zern = self.second.Zern.currentText()
        desc = self.second.Desc.text()
        cost = self.second.Cost.value()
        v = self.second.VV.value()
        self.delete()
        print(f"INSERT INTO coffee (id,Name,RawState,DType,Desc,Cost,V) VALUES ({id},'{name}'"
                     f",'{st}','{zern}','{desc}',{cost},{v})")
        conn.execute(f"INSERT INTO coffee (id,Name,RawState,DType,Desc,Cost,V) VALUES ({id},'{name}'"
                     f",'{st}','{zern}','{desc}',{cost},{v})")
        self.reloadDataBase()
        conn.commit()

    def add(self):
        conn.execute(f"INSERT INTO coffee (Name, RawState, DType, Desc, Cost, V) VALUES ('empty',"
                     f"'None','None','None',1,1)")
        conn.commit()
        self.reloadDataBase()

    def __init__(self):
        super().__init__()
        self.move(10, 10)
        uic.loadUi("main.ui", self)
        self.setWindowTitle("Coffee table")
        self.show()
        self.second = SecondWidget()
        self.second.IDlist.currentTextChanged.connect(self.second.getData)
        self.second.DeleteButton.clicked.connect(self.delete)
        self.second.SaveButton.clicked.connect(self.save)
        self.second.AddButton.clicked.connect(self.add)
        self.reloadDataBase()

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
    sys.exit(app.exec_())
