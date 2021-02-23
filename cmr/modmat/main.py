#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Este programa gestiona el archivo de datos modelos.csv

author: Alejandro Bolívar
email: bolivara@gmail.com
last edited: marzo 2018
"""

__author__ = 'Alejandro Bolívar'
__version__ = "1.0"

import pandas as pd

from PyQt5.QtCore import pyqtSignal, QEvent, QObject

from PyQt5 import QtCore, uic, QtWidgets
from PyQt5.QtCore import (QTranslator, QLibraryInfo,
                          QLocale)
from PyQt5.QtWidgets import QMessageBox, QDesktopWidget

qtCreatorFile = "modelos_ui.ui" # Nombre del archivo aquí.

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)


def actualizaModelo(self):

    model = PandasModel(self.ui.data)

    self.ui.tableView.setModel(model)
    self.ui.tableView.update()


def clickable(widget):

    class Filter(QObject):

        clicked = pyqtSignal()

        def eventFilter(self, obj, event):

            if obj == widget:
                if event.type() == QEvent.MouseButtonRelease:
                    if obj.rect().contains(event.pos()):
                        self.clicked.emit()
                        # The developer can opt for .emit(obj) to get the object within the slot.
                        return True
            return False

    filter = Filter(widget)
    widget.installEventFilter(filter)
    return filter.clicked


class PandasModel(QtCore.QAbstractTableModel):

    def __init__(self, data, parent=None):
        QtCore.QAbstractTableModel.__init__(self, parent)
        self._data = data

    def rowCount(self, parent=None):
        return len(self._data.values)

    def columnCount(self, parent=None):
        return self._data.columns.size

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if index.isValid():
            if role == QtCore.Qt.DisplayRole:
                return QtCore.QVariant(str(
                    self._data.values[index.row()][index.column()]))
        return QtCore.QVariant()

class Modelo(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self):

        super(Modelo, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.center()
        self.setWindowTitle('Gestor de Modelos Matemáticos')

        self.ui.data = pd.read_csv('modelos.csv', sep=';', encoding="ISO-8859-1")
        self.ui.sel = 0

        clickable(self.ui.txtMod).connect(self.limpiarTexto)

        self.ui.btnAgregar.clicked.connect(self.agregarDatos)
        self.ui.btnModificar.clicked.connect(self.modificarDatos)
        self.ui.btnEliminar.clicked.connect(self.eliminarDatos)
        self.ui.tableView.clicked.connect(self.click_table)

        actualizaModelo(self)

        self.ui.btnAgregar.setEnabled(False)
        self.ui.btnModificar.setEnabled(False)
        self.ui.btnEliminar.setEnabled(False)

    def limpiarTexto(self):

        if self.ui.txtMod.text() == 'Introduzca el Modelo Matemático y pulse Aceptar':
            self.ui.txtMod.setText('')

        self.ui.btnAgregar.setEnabled(True)

    def agregarDatos(self):

        self.ui.data = self.ui.data.append({'modelos':self.ui.txtMod.text()}, ignore_index=True)

        actualizaModelo(self)
        self.ui.data.to_csv('modelos.csv', sep=';', encoding="ISO-8859-1", header=True, index=False)

        self.ui.btnAgregar.setEnabled(False)
        self.ui.txtMod.setText('Introduzca el Modelo Matemático y pulse Aceptar')

        self.ui.txtMod.setFocus()

    def center(self):

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def closeEvent(self, event):

        reply = QMessageBox.question(self, 'Mensaje', "¿Esta seguro de salir?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def click_table(self):

        index = self.ui.tableView.selectedIndexes()[0]

        self.ui.sel = index.row()

        self.ui.txtMod.setText(self.ui.data['modelos'][index.row()])

        self.ui.btnModificar.setEnabled(True)
        self.ui.btnEliminar.setEnabled(True)

    def eliminarDatos(self):

        self.ui.data = self.ui.data.drop(self.ui.sel)

        actualizaModelo(self)
        self.ui.data.to_csv('modelos.csv', sep=';', encoding="ISO-8859-1", header=True, index=False)

        self.ui.btnAgregar.setEnabled(True)
        self.ui.btnModificar.setEnabled(False)
        self.ui.btnEliminar.setEnabled(False)

        self.ui.txtMod.setText('')
        self.ui.txtMod.setFocus()

    def getCSV(self):

        '''
        Esta función abre el archivo CSV
        '''

        filePath, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', '/home')
        if filePath != "":
            print("Dirección", filePath) #Opcional imprimir la dirección del archivo
            self.ui.df = pd.read_csv(str(filePath))

    def modificarDatos(self):

        self.ui.data.loc[self.ui.sel, 'modelos'] = self.ui.txtMod.text()

        actualizaModelo(self)
        self.ui.data.to_csv('modelos.csv', sep=';', encoding="ISO-8859-1", header=True, index=False)

        self.ui.btnAgregar.setEnabled(True)
        self.ui.btnModificar.setEnabled(False)
        self.ui.btnEliminar.setEnabled(False)

        self.ui.txtMod.setText('')

        self.ui.txtMod.setFocus()

if __name__ == '__main__':

    import sys

    app = QtWidgets.QApplication(sys.argv)
    
    qt_traductor = QTranslator()
    qt_traductor.load("qtbase_" + QLocale.system().name(),
                      QLibraryInfo.location(QLibraryInfo.TranslationsPath))
    app.installTranslator(qt_traductor)
    window = Modelo()
    window.show()
    sys.exit(app.exec_())
    