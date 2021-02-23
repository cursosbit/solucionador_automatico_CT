#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Este programa gestiona el archivo de datos ecuaciones.csv

author: Alejandro Bolívar
email: bolivara@gmail.com
last edited: marzo 2018
"""
__author__ = 'Alejandro Bolívar'
__version__ = "1.0"

import pandas as pd
from listvar import list_var

from PyQt5.QtCore import pyqtSignal, QEvent, QObject

from PyQt5 import QtCore, uic, QtWidgets
from PyQt5.QtCore import (QTranslator, QLibraryInfo,
                          QLocale)
from PyQt5.QtWidgets import QMessageBox, QDesktopWidget

qtCreatorFile = "ecuaciones_ui.ui" # Nombre del archivo aquí.

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

list_Ec = []


def actualizaModelo(self):

    model = PandasModel(self.ui.dataEc)

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
        self.setWindowTitle('Gestor de Ecuaciones')

        self.ui.dataMod = pd.read_csv('..\modmat\modelos.csv', sep=';', encoding="ISO-8859-1")
        for itemEc in self.ui.dataMod['modelos']:
            self.ui.comboBox.addItem(itemEc)

        self.ui.dataEc = pd.read_csv('ecuaciones.csv', sep=';', encoding="ISO-8859-1")
        self.ui.sel = 0

        clickable(self.ui.txtEc).connect(self.limpiarTexto)

        self.ui.btnAceptar.clicked.connect(self.aceptarEc)
        self.ui.btnAgregar.clicked.connect(self.agregarDatos)
        self.ui.btnModificar.clicked.connect(self.modificarDatos)
        self.ui.btnEliminar.clicked.connect(self.eliminarDatos)
        self.ui.tableView.clicked.connect(self.click_table)

        actualizaModelo(self)

        self.ui.btnAceptar.setEnabled(False)
        self.ui.btnAgregar.setEnabled(False)
        self.ui.btnModificar.setEnabled(False)
        self.ui.btnEliminar.setEnabled(False)


    def limpiarTexto(self):

        if self.ui.txtEc.text() == 'Introduzca la Ecuación y pulse Aceptar':
            self.ui.txtEc.setText('')
            self.ui.lblListVar.setText('')

        self.ui.btnAceptar.setEnabled(True)


    def aceptarEc(self):
        # Lista de  variables de la ecuación
        lv = ', '.join(list_var([self.ui.txtEc.text()]))
        # Muestra la lista de variables en la etiqueta
        self.ui.lblListVar.setText(lv)
        
        if lv == 'Por favor, verifique los paréntesis':
            self.ui.txtEc.setFocus()
        else:
            self.ui.btnAceptar.setEnabled(False)
            print(self.ui.lblListVar.text())
            if self.ui.btnEliminar.isEnabled() == False:
                self.ui.btnAgregar.setEnabled(True)
                self.ui.btnAgregar.setFocus()


    def agregarDatos(self):

        self.ui.dataEc = self.ui.dataEc.append({'modelos':self.ui.comboBox.currentText(),
                                                'ecuaciones':self.ui.txtEc.text(),
                                                'variables':self.ui.lblListVar.text()}, ignore_index=True)

        actualizaModelo(self)
        self.ui.dataEc.to_csv('ecuaciones.csv', sep=';', encoding="ISO-8859-1",
                              header=True, index=False)

        self.ui.btnAgregar.setEnabled(False)
        self.ui.txtEc.setText('Introduzca la Ecuación y pulse Aceptar')
        self.ui.lblListVar.setText('')
        self.ui.txtEc.setFocus()


    def center(self):

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


    def closeEvent(self, event):

        reply = QMessageBox.question(self, 'Mensaje', "¿Esta seguro de salir?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


    def click_table(self):

        index = self.ui.tableView.selectedIndexes()[0]

        self.ui.sel = index.row()

        self.ui.txtEc.setText(self.ui.dataEc['ecuaciones'][index.row()])
        self.ui.lblListVar.setText(self.ui.dataEc['variables'][index.row()])

        self.ui.btnAceptar.setEnabled(False)
        self.ui.btnModificar.setEnabled(True)
        self.ui.btnEliminar.setEnabled(True)


    def eliminarDatos(self):

        self.ui.dataEc = self.ui.dataEc.drop(self.ui.sel)

        actualizaModelo(self)
        self.ui.dataEc.to_csv('ecuaciones.csv', sep=';', encoding="ISO-8859-1",
                              header=True, index=False)

        self.ui.btnAceptar.setEnabled(True)
        self.ui.btnModificar.setEnabled(False)
        self.ui.btnEliminar.setEnabled(False)

        self.ui.txtEc.setText('')
        self.ui.lblListVar.setText('')
        self.ui.txtEc.setFocus()


    def getCSV(self):

        '''
        Esta función abre el archivo CSV
        '''

        filePath, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', '/home')
        if filePath != "":
            print("Dirección", filePath) #Opcional imprimir la dirección del archivo
            self.ui.df = pd.read_csv(str(filePath))


    def modificarDatos(self):

        self.ui.dataEc.loc[self.ui.sel, 'modelos'] = self.ui.comboBox.currentText()
        self.ui.dataEc.loc[self.ui.sel, 'ecuaciones'] = self.ui.txtEc.text()
        self.ui.dataEc.loc[self.ui.sel, 'variables'] = self.ui.lblListVar.text()

        actualizaModelo(self)
        self.ui.dataEc.to_csv('ecuaciones.csv', sep=';',
                              encoding="ISO-8859-1", header=True, index=False)

        self.ui.btnAceptar.setEnabled(True)
        self.ui.btnModificar.setEnabled(False)
        self.ui.btnEliminar.setEnabled(False)

        self.ui.txtEc.setText('')
        self.ui.lblListVar.setText('')

        self.ui.txtEc.setFocus()


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
    