#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Este programa gestiona el archivo de datos enunciados.csv

author: Alejandro Bolívar
email: bolivara@gmail.com
last edited: marzo 2018
"""

__author__ = 'Alejandro Bolívar'
__version__ = "1.0"

import pandas as pd

from PyQt5.QtCore import pyqtSignal, QEvent, QObject

from PyQt5 import QtCore, uic, QtWidgets
from PyQt5.QtCore import (QTranslator, QLibraryInfo, QLocale)
from PyQt5.QtWidgets import QMessageBox, QDesktopWidget

QTCREATORFILE = "enunciados_ui.ui" # Nombre del archivo aquí.

Ui_MainWindow, QtBaseClass = uic.loadUiType(QTCREATORFILE)


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
        self.setWindowTitle('Gestor de Enunciados')

        self.ui.data = pd.read_csv('enunciados124.csv', sep=';', encoding="ISO-8859-1")
        self.ui.sel = 0

        clickable(self.ui.txtEnunc).connect(self.limpiartxtenunc)
        clickable(self.ui.txtMod).connect(self.limpiartxtmod)
        clickable(self.ui.txtListVarIndep).connect(self.limpiartxtlistvarindep)
        clickable(self.ui.txtListVarDep).connect(self.limpiartxtlistvardep)
        clickable(self.ui.txtRef).connect(self.limpiartxtref)
        clickable(self.ui.txtPag).connect(self.limpiartxtpag)
        clickable(self.ui.txtNro).connect(self.limpiartxtnro)

        self.ui.btnAgregar.clicked.connect(self.agregardatos)
        self.ui.btnModificar.clicked.connect(self.modificardatos)
        self.ui.btnEliminar.clicked.connect(self.eliminardatos)
        self.ui.tableView.clicked.connect(self.click_table)

        actualizaModelo(self)

        self.ui.btnAgregar.setEnabled(False)
        self.ui.btnModificar.setEnabled(False)
        self.ui.btnEliminar.setEnabled(False)
        print(self.ui.txtEnunc.toPlainText())

    def limpiartxtenunc(self):
        print(self.ui.txtEnunc.toPlainText())
        if self.ui.txtEnunc.toPlainText() == 'Enunciado':
            self.ui.txtEnunc.clear()

    def limpiartxtmod(self):

        if self.ui.txtMod.toPlainText() == 'Modelo':
            self.ui.txtMod.clear()

    def limpiartxtlistvarindep(self):

        if self.ui.txtListVarIndep.toPlainText() == 'Lista de Variables Independientes':
            self.ui.txtListVarIndep.clear()

    def limpiartxtlistvardep(self):

        if self.ui.txtListVarDep.toPlainText() == 'Lista de Variables Dependientes':
            self.ui.txtListVarDep.clear()

    def limpiartxtref(self):

        if self.ui.txtRef.toPlainText() == 'Referencia':
            self.ui.txtRef.clear()

    def limpiartxtpag(self):

        if self.ui.txtPag.text() == 'Página':
            self.ui.txtPag.clear()

    def limpiartxtnro(self):
        print(self.ui.txtNro.text())
        if self.ui.txtNro.text() == 'Número del Ejercicio':
            self.ui.txtNro.clear()

        self.ui.btnAgregar.setEnabled(True)

    def agregardatos(self):

        self.ui.data = self.ui.data.append({'enunc':self.ui.txtEnunc.toPlainText(),
                                            'mod':self.ui.txtMod.toPlainText(),
                                            'listvarindep':self.ui.txtListVarIndep.toPlainText(),
                                            'listvardep':self.ui.txtListVarDep.toPlainText(),
                                            'ref':self.ui.txtRef.toPlainText(),
                                            'pag':self.ui.txtPag.Text(),
                                            'nro':self.ui.txtNro.Text(),
                                           }, ignore_index=True)

        actualizaModelo(self)
        self.ui.data.to_csv('modelos.csv', sep=';', encoding="ISO-8859-1", header=True, index=False)

        self.ui.btnAgregar.setEnabled(False)

        self.ui.txtEnunc.setPlainText('Enunciado')
        self.ui.txtMod.setPlainText('Modelo')
        self.ui.txtListVarIndep.setPlainText('Lista de Variables Independientes')
        self.ui.txtListVarDep.setPlainText('Lista de Variables Dependientes')
        self.ui.txtRef.setPlainText('Referencia')
        self.ui.txtPag.setText('Página')
        self.ui.txtNro.setText('Número del Ejercicio')

        self.ui.txtMod.setFocus()

    def center(self):

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def closeEvent(self, event):

        reply = QMessageBox.question(self, 'Mensaje', "¿Esta seguro de salir?", QMessageBox.Yes |
            QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def click_table(self):

        index = self.ui.tableView.selectedIndexes()[0]

        self.ui.sel = index.row()

        self.ui.txtEnunc.setPlainText(self.ui.data['enunc'][index.row()])
        self.ui.txtMod.setPlainText(self.ui.data['mod'][index.row()])
        self.ui.txtListVarIndep.setPlainText(self.ui.data['listvarindep'][index.row()])
        self.ui.txtListVarDep.setPlainText(self.ui.data['listvardep'][index.row()])
        self.ui.txtRef.setPlainText(self.ui.data['ref'][index.row()])
        self.ui.txtPag.setText(self.ui.data['pag'][index.row()])
        self.ui.txtNro.setText(self.ui.data['nro'][index.row()])

        self.ui.btnModificar.setEnabled(True)
        self.ui.btnEliminar.setEnabled(True)

    def eliminardatos(self):

        self.ui.data = self.ui.data.drop(self.ui.sel)

        actualizaModelo(self)
        self.ui.data.to_csv('modelos.csv', sep=';', encoding="ISO-8859-1", header=True, index=False)

        self.ui.btnAgregar.setEnabled(True)
        self.ui.btnModificar.setEnabled(False)
        self.ui.btnEliminar.setEnabled(False)

        self.ui.txtEnunc.clear()
        self.ui.txtMod.clear()
        self.ui.txtListVarIndep.clear()
        self.ui.txtListVarDep.clear()
        self.ui.txtRef.clear()
        self.ui.txtPag.clear()
        self.ui.txtNro.clear()

        self.ui.txtEnunciado.setFocus()

    def getCSV(self):

        '''
        Esta función abre el archivo CSV
        '''

        filePath, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', '/home')
        if filePath != "":
            print("Dirección", filePath) #Opcional imprimir la dirección del archivo
            self.ui.df = pd.read_csv(str(filePath))

    def modificardatos(self):

        self.ui.data.loc[self.ui.sel, 'enunc'] = self.ui.txtEnunciado.toPlainText()
        self.ui.data.loc[self.ui.sel, 'mod'] = self.ui.txtMod.toPlainText()
        self.ui.data.loc[self.ui.sel, 'listvarindep'] = self.ui.txtListVarIndep.toPlainText()
        self.ui.data.loc[self.ui.sel, 'listvardep'] = self.ui.txtListVarDep.toPlainText()
        self.ui.data.loc[self.ui.sel, 'ref'] = self.ui.txtRef.toPlainText()
        self.ui.data.loc[self.ui.sel, 'pag'] = self.ui.txtPag.Text()
        self.ui.data.loc[self.ui.sel, 'nro'] = self.ui.txtNro.Text()

        actualizaModelo(self)
        self.ui.data.to_csv('modelos.csv', sep=';', encoding="ISO-8859-1", header=True, index=False)

        self.ui.btnAgregar.setEnabled(True)
        self.ui.btnModificar.setEnabled(False)
        self.ui.btnEliminar.setEnabled(False)

        self.ui.txtEnunc.clear()
        self.ui.txtMod.clear()
        self.ui.txtListVarIndep.clear()
        self.ui.txtListVarDep.clear()
        self.ui.txtRef.clear()
        self.ui.txtPag.clear()
        self.ui.txtNro.clear()

        self.ui.txtEnunc.setFocus()

if __name__ == '__main__':

    import sys

    APP = QtWidgets.QApplication(sys.argv)

    QT_TRADUCTOR = QTranslator()
    QT_TRADUCTOR.load("qtbase_" + QLocale.system().name(),
                      QLibraryInfo.location(QLibraryInfo.TranslationsPath))
    APP.installTranslator(QT_TRADUCTOR)
    WINDOW = Modelo()
    WINDOW.show()
    sys.exit(APP.exec_())
    