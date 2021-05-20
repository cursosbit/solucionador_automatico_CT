"""
Created on Sun Dec 17 22:40:58 2017

@author: bolivar

"""

# Se importa las librerias requeridas

import pandas as pd

from librerias.lib_ClasifMod import clasificador
from librerias.lib_IdVar import detectar_vars

# This code was tested with matplotlib 2.1.0, numpy 1.16.5
# pandas 1.0.3, keras 2.1.2, sklearn 0.24.1

# print("numpy version", np.__version__)
# print("pandas version", pd.__version__)

data = pd.read_csv('dataset/enunciadosCT.csv',sep='|')

# clasificador(data)

dfvar = pd.read_csv('dataset/listadevariables2.csv', sep='|')

data2=data.copy()

detectar_vars(data2, dfvar)