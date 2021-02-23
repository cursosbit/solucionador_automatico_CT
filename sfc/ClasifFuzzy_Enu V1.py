
"""
Este programa determina la dificultad de enunciados de texto

author: Alejandro Bolívar
email: bolivara@gmail.com
last edited: mayo 2018
"""

__author__ = 'Alejandro Bolívar'
__version__="1.0"


"""
========================================================
Fuzzy Control Systems: Dificultad de enunciados de texto
========================================================

We would formulate this problem as:

* Antecedents (Inputs)
   - `service`
      * Universe (ie, crisp value range): How good was the service of the wait
        staff, on a scale of 0 to 10?
      * Fuzzy set (ie, fuzzy value range): poor, acceptable, amazing
   - `food quality`
      * Universe: How tasty was the food, on a scale of 0 to 10?
      * Fuzzy set: bad, decent, great
* Consequents (Outputs)
   - `tip`
      * Universe: How much should we tip, on a scale of 0% to 25%
      * Fuzzy set: low, medium, high
* Rules
   - IF the *service* was good  *or* the *food quality* was good,
     THEN the tip will be high.
   - IF the *service* was average, THEN the tip will be medium.
   - IF the *service* was poor *and* the *food quality* was poor
     THEN the tip will be low.
* Usage
   - If I tell this controller that I rated:
      * the service as 9.8, and
      * the quality as 6.5,
   - it would recommend I leave:
      * a 20.2% tip.


Creating the Tipping Controller Using the skfuzzy control API
-------------------------------------------------------------

We can use the `skfuzzy` control system API to model this.  First, let's
define fuzzy variables
"""

from PyQt5.QtCore import pyqtSignal,QEvent,QObject
from PyQt5 import uic, QtWidgets
from PyQt5.QtCore import (QTranslator, QLibraryInfo, QLocale)
from PyQt5.QtWidgets import QMessageBox, QDesktopWidget

qtCreatorFile = "ClasifFuzzy_Enu_ui.ui" # Nombre del archivo aquí. 

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl


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

       
class Dificultad(QtWidgets.QMainWindow, Ui_MainWindow):
    
    def __init__(self):
        super(Dificultad, self).__init__()
        
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.center()
        self.setWindowTitle('Raíces de una ecuación no lineal') 
        
        clickable(self.ui.txtEnunciado).connect(self.limpiartxtEnunciado)
        clickable(self.ui.txtIncognitas).connect(self.limpiartxtIncognitas)
        clickable(self.ui.txtVarConocidas).connect(self.limpiartxtVarConocidas)
        clickable(self.ui.txtCalcIntermedios).connect(self.limpiartxtCalcIntermedios)
        clickable(self.ui.txtTam).connect(self.limpiartxtTam)
        clickable(self.ui.txtOfuscacion).connect(self.limpiartxtOfuscacion)
        
        self.ui.btnLimpiar.clicked.connect(self.limpiar)
        self.ui.btnCalcular.clicked.connect(self.dificultad)
        self.ui.btnSalir.clicked.connect(self.salir)

    def center(self):
        
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

        
    def closeEvent(self, event):
        
        reply = QMessageBox.question(self, 'Mensaje', "¿Esta seguro de salir?", 
                                     QMessageBox.Yes | QMessageBox.No, 
                                     QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()     

    def limpiar(self):
        self.ui.txtEnunciado.setText('Enunciado')
        self.ui.txtIncognitas.setText('Incógnitas')
        self.ui.txtVarConocidas.setText('Variables Conocidas')
        self.ui.txtCalcIntermedios.setText('Cálclos Intermedios')
        self.ui.txtTam.setText('Tamaño')
        self.ui.txtOfuscacion.setText('Ofuscación')

    def limpiartxtEnunciado(self):
        
        if self.ui.txtEnunciado.text()=='Enunciado':
            self.ui.txtEnunciado.setText('')
            
            
    def limpiartxtIncognitas(self):
        
        if self.ui.txtIncognitas.text()=='Incógnitas':
            self.ui.txtIncognitas.setText('')


    def limpiartxtVarConocidas(self):
        
        if self.ui.txtVarConocidas.text()=='Variables Conocidas':
            self.ui.txtVarConocidas.setText('')


    def limpiartxtCalcIntermedios(self):
        
        if self.ui.txtCalcIntermedios.text()=='Cálculos Intermedios':
            self.ui.txtCalcIntermedios.setText('')

    def limpiartxtTam(self):
        
        if self.ui.txtTam.text()=='Tamaño':
            self.ui.txtTam.setText('')
            
    def limpiartxtOfuscacion(self):
        
        if self.ui.txtOfuscacion.text()=='Ofuscación':
            self.ui.txtOfuscacion.setText('')
            
    
    def dificultad(self):
        
                
        # New Antecedent/Consequent objects hold universe variables and membership
        # functions
        incógnitas = ctrl.Antecedent(np.arange(0, 11, 1), 'Incógnitas')
        varconocidas = ctrl.Antecedent(np.arange(0, 11, 1), 'Variables Conocidas')
        calculosinter= ctrl.Antecedent(np.arange(0, 11, 1), 'Cálculos Intermedios')
        tamaño = ctrl.Antecedent(np.arange(0, 11, 1), 'Tamaño')
        oraciones = ctrl.Antecedent(np.arange(0, 11, 1), 'Oraciones')
        ofuscación = ctrl.Antecedent(np.arange(0, 11, 1), 'Ofuscación')
        
        dificultad = ctrl.Consequent(np.arange(0, 101, 1), 'dificultad')
        
        # Auto-membership function population is possible with .automf(3, 5, or 7)
        incógnitas.automf(3,variable_type='quant',names=['pocas','normal','muchas'])
        varconocidas.automf(3,variable_type='quant',names=['pocas','normal','muchas'])
        calculosinter.automf(3,variable_type='quant',names=['pocos','normal','muchos'])
        tamaño.automf(3,variable_type='quant',names=['corto','normal','extenso'])
        oraciones.automf(3,variable_type='quant',names=['pocas','normal','muchas'])
        ofuscación.automf(3,variable_type='quant',names=['poca','normal','mucha'])
        
        dificultad.automf(5,variable_type='quant',names=['muy baja','baja','media','alta','muy alta'])
        
        # Custom membership functions can be built interactively with a familiar,
        # Pythonic API
        dificultad['muy baja'] = fuzz.sigmf(dificultad.universe,20,-0.3)
        dificultad['baja'] = fuzz.gaussmf(dificultad.universe, 30,9)
        dificultad['media'] = fuzz.gaussmf(dificultad.universe,50, 9)
        dificultad['alta'] = fuzz.gaussmf(dificultad.universe, 70,9)
        dificultad['muy alta'] = fuzz.sigmf(dificultad.universe,70,0.3)
        
        """
        To help understand what the membership looks like, use the ``view`` methods.
        """
        
        # You can see how these look with .view()
        

        incógnitas['normal'].view()
        varconocidas.view()
        calculosinter.view()
        tamaño.view()
        oraciones.view()
        ofuscación.view()
        
        """
        .. image:: PLOT2RST.current_figure
        
        Fuzzy rules
        -----------
        
        Now, to make these triangles useful, we define the *fuzzy relationship*
        between input and output variables. For the purposes of our example, consider
        three simple rules:
        
        1. If the food is poor OR the service is poor, then the tip will be low
        2. If the service is average, then the tip will be medium
        3. If the food is good OR the service is good, then the tip will be high.
        
        Most people would agree on these rules, but the rules are fuzzy. Mapping the
        imprecise rules into a defined, actionable tip is a challenge. This is the
        kind of task at which fuzzy logic excels.
        """
        
        rule1 = ctrl.Rule((varconocidas['pocas'] & calculosinter['muchos']) | calculosinter['pocos'], dificultad['alta'])
        rule2 = ctrl.Rule(varconocidas['muchas'] & calculosinter['muchos'], dificultad['muy alta'])
        rule3 = ctrl.Rule((tamaño['extenso'] & incógnitas['muchas']) & varconocidas['pocas'] , dificultad['muy alta'])
        rule4= ctrl.Rule((tamaño['extenso'] & varconocidas['normal']) & (incógnitas['muchas'] | incógnitas['normal']), dificultad['media'])
        rule5= ctrl.Rule(tamaño['extenso'] & varconocidas['muchas'] & incógnitas['muchas'] & ofuscación['poca'], dificultad['muy baja'])
        rule6= ctrl.Rule(ofuscación['mucha'] & tamaño['corto']  & varconocidas['normal'] & calculosinter['muchos'] & incógnitas['pocas'], dificultad['muy alta'])
        
        #rule1.view()
        #rule2.view()
        #rule3.view()
        #rule4.view()
        #rule5.view()
        #rule6.view()
        
        """
        .. image:: PLOT2RST.current_figure
        
        Control System Creation and Simulation
        ---------------------------------------
        
        Now that we have our rules defined, we can simply create a control system
        via:
        """
        
        tipping_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6])
        
        """
        In order to simulate this control system, we will create a
        ``ControlSystemSimulation``.  Think of this object representing our controller
        applied to a specific set of cirucmstances.  For tipping, this might be tipping
        Sharon at the local brew-pub.  We would create another
        ``ControlSystemSimulation`` when we're trying to apply our ``tipping_ctrl``
        for Travis at the cafe because the inputs would be different.
        """
        
        tipping = ctrl.ControlSystemSimulation(tipping_ctrl)
        
        """
        Ahora se puede simular el sistema de control simplemente especificando 
        las entradas y llamando al método `` compute``. Supongamos que se califica
        las Incógnitas 3.5 de 10, Variables Conocidas 9.8 de 10, Cálculos Intermedios 
        3.5 de 10, Tamaño 9.8 de 10, Oraciones 8.5 de 10, Ofuscación 9.8 de 10.
        """
        
        # Pass inputs to the ControlSystem using Antecedent labels with Pythonic API
        # Note: if you like passing many inputs all at once, use .inputs(dict_of_data)
        
        tipping.input['Incógnitas'] = float(self.ui.txtIncognitas.text()) #3.5
        tipping.input['Variables Conocidas'] = float(self.ui.txtVarConocidas.text()) # 9.8
        tipping.input['Cálculos Intermedios'] = float(self.ui.txtCalcIntermedios.text()) #3.5
        tipping.input['Tamaño'] = float(self.ui.txtTam.text()) #9.8
        #tipping.input['Oraciones'] = 8.5
        tipping.input['Ofuscación'] = float(self.ui.txtOfuscacion.text()) #9.8
        
        # Crunch the numbers
        tipping.compute()
        
        """
        Una vez calculado, se puede ver el resultado y graficarlo.
        """
        
        z=tipping.output['dificultad']
        print (z)
        self.ui.lblDificultad.setText('Dificultd= ' + str(z))
        dificultad.view(sim=tipping)


    def salir(self):
        sys.exit(app.exec_())

if __name__ == '__main__':
    
    import sys
    
    app = QtWidgets.QApplication(sys.argv)
    
    qt_traductor = QTranslator()
    qt_traductor.load("qtbase_" + QLocale.system().name(),
                      QLibraryInfo.location(QLibraryInfo.TranslationsPath))
    app.installTranslator(qt_traductor)
    window = Dificultad()
    window.show()
    sys.exit(app.exec_())