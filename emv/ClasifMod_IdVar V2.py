"""
Created on Sun Dec 17 22:40:58 2017

@author: bolivar

"""

# Se importa las librerias requeridas

import matplotlib.pyplot as plt

import numpy as np  # para el manejo de arrays
import pandas as pd

from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import confusion_matrix

from keras import utils
from keras.layers import Dropout
from keras.preprocessing import text

# Se importa las librerias propias

from librerias.lib_ClasifMod import filtros1, plot_confusion_matrix, create_network
from librerias.lib_IdVar import filtros2, conteo, convertir_str_list, print_resultados_enunciados, print_resultados_variables, dividir_datos, analizar_oracion


# Parámetros
max_words = 40
batch_size = 3
epochs = 8
plot = True
#Prueba
network = {
    'n_dense': 1,
    'dense_units': 256,
    'activation': 'relu',
    'dropout': Dropout,
    'dropout_rate': 0.5,
    'kernel_initializer': 'glorot_uniform',
    'optimizer': 'adam'
}

# This code was tested with matplotlib 2.1.0, numpy 1.14.5
# pandas 0.23.1, keras 2.1.2, sklearn 0.19.2

print("numpy version", np.__version__)
print("pandas version", pd.__version__)

#enunciadosdesordenados2.csv
data = pd.read_csv('dataset/enunciados124.csv',sep='|',encoding = "ISO-8859-1")
print('Modelos                             Cantidad')
print(data['modelos'].value_counts())
filtros1(data)

enunciado_train = []
modelo_train = []
enunciado_test = []
modelo_test = []
test_size = 0
train_size = 0

# Creación de los arrays de entrada y salida
train_size,test_size,enunciado_train,modelo_train,enunciado_test,modelo_test=dividir_datos(0.9,data)

# Vectorizar los enunciados en un tensor de enteros 2D
#print("Preparando el Tokenizer...")
tokenize = text.Tokenizer(num_words=max_words, char_level=False )
tokenize.fit_on_texts(enunciado_train) # only fit on train
# summarize what was learned
#print('\ntokenize.word_counts', tokenize.word_counts)
#print('\ntokenize.document_count', tokenize.document_count)
#print('\ntokenize.word_index', tokenize.word_index)
#print('\ntokenize.word_docs', tokenize.word_docs)
#print('\nVectorizando datos en secuencia...')
# Convert a list of texts to a Numpy matrix.
x_train = tokenize.texts_to_matrix(enunciado_train)
x_test = tokenize.texts_to_matrix(enunciado_test)
# Utiliza sklearn para convertir las cadenas de los modelos en índices numerados
encoder = LabelEncoder()
encoder.fit(modelo_train)
y_train = encoder.transform(modelo_train)
y_test = encoder.transform(modelo_test)
print('encoder.transform')
print('y_train shape:', y_train.shape)
print('y_test shape:', y_test.shape)
print('y_train:', y_train)
print('y_test:', y_test)
#print('\n')

# Convierte los modelos en una representación one-hot
num_classes = np.max(y_train) + 1 # Cantidad de modelos
y_train = utils.to_categorical(y_train, num_classes)
y_test = utils.to_categorical(y_test, num_classes)

# Inspeccione las dimensiones de los datos de entrenamiento y prueba (esto es útil para depurar)
print('Dimensiones de los datos de entrenamiento y prueba')
print('x_train shape:', x_train.shape)
print('x_test shape:', x_test.shape)
print('y_train shape:', y_train.shape)
print('y_test shape:', y_test.shape)
print('\n')
#print('x_train :', x_train[0])
#print (data['enunciados'][0])
#input()
#print('x_test :', x_test)
print('y_train :', y_train)
print('y_test :', y_test)
#print('\n')

# Creación de la arquitectura de la red neuronal
print('\nCreando la Red...')
model = create_network(max_words,num_classes,**network)
# model.fit Entrena el modelo
# The validation_split param tells Keras what % of our training data should be used in the validation set
# You can see the validation loss decreasing slowly when you run this
# Because val_loss is no longer decreasing we stop training to prevent overfitting
# Para entrenar la red, se indicas las entradas, sus salidas y la cantidad de 
# iteraciones de aprendizaje (epochs) de entrenamiento
history = model.fit(x_train, y_train, batch_size=batch_size, epochs=epochs,
                    verbose=1, validation_split=0.1)
# Evalúa la precisión del modelo entrenado
score = model.evaluate(x_test, y_test, batch_size=batch_size, verbose=1)
print('\n')
print('Hyperparameters:', network)
print('Test score:', score[0])
print('Test accuracy:', score[1])
print('\n')
# Here's how to generate a prediction on individual examples
text_labels = encoder.classes_ 
for i in range(test_size):
    prediction = model.predict(np.array([x_test[i]]))
    predicted_label = text_labels[np.argmax(prediction)]
    print(str(i) + ' ' + enunciado_test.iloc[i][:50], '...')
    print('Actual modelo:' + modelo_test.iloc[i])
    print("Predicted modelo: " + predicted_label + "\n")

#enunciado='¿Cuánto tiempo tarda un auto en acelerar desde el reposo hasta 22.2 m/s si la aceleración es constante y el auto avanza 243 m durante el periodo de aceleración?'
#enunciado=input('Enunciado:')
#z =[{'enunciado':enunciado}]
#dataz=pd.DataFrame(z)
#e_test = dataz['enunciado'][:]
#x_t = tokenize.texts_to_matrix(e_test)
#pred = model.predict(np.array([x_t[0]]))
#pred_label = text_labels[np.argmax(pred)]
#print("modelo sugerido: " + pred_label + "\n")

#pred_label = 'MovimientoUniformementeAcelerado'
#print('El modelo matemático a aplicar es: ',pred_label,'\n')
#resp=input('¿Está de acuerdo con el modelo a aplicar [S/N]:?')
#if resp.upper()=='N':
#    pred_label=input('Introduzca el Modelo que Ud sugiere')

#z =[{'enunciado':enunciado,'modelo':pred_label}]
#dataz=pd.DataFrame(z)
#dataz.to_csv('salida.csv',mode='a', index=False, header=False,sep='|')

#data_modelos = pd.read_csv('modelos.csv',sep='|',encoding = "ISO-8859-1")
#for i in range(0, len(data_modelos)):
#    if (pred_label==data_modelos.iloc[i]['modelo']):
#        print(data_modelos.iloc[i]['variables'])
#input()

y_softmax = model.predict(x_test)
y_test_1d = []
y_pred_1d = []
for i in range(len(y_test)):
    probs = y_test[i]
    index_arr = np.nonzero(probs)
    one_hot_index = index_arr[0].item(0)
    y_test_1d.append(one_hot_index)
for i in range(0, len(y_softmax)):
    probs = y_softmax[i]
    predicted_index = np.argmax(probs)
    y_pred_1d.append(predicted_index)
cnf_matrix = confusion_matrix(y_test_1d, y_pred_1d)

plt.figure(figsize=(6,5))
plot_confusion_matrix(cnf_matrix, classes=text_labels, title="Confusion matrix")
plt.savefig('networks.png')

fig2 = plt.figure(2)
plt.plot(range(epochs), history.history['loss'], 'g--', label='Loss')
plt.plot(range(epochs), history.history['val_loss'], 'g-', label='Val Loss')
plt.plot(range(epochs), history.history['acc'], 'b--', label='Acc')
plt.plot(range(epochs), history.history['val_acc'], 'b-', label='Val Acc')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()
plt=plt.twinx()
plt.set_ylabel('acc')

################## Detección de Variables ################################

#data = pd.read_csv('enunciados.csv',sep='|',encoding = "ISO-8859-1")
#print ('Texto Original\n',data['enunciados'][0])
#print("\n")

filtros2(data)
'''
La estructura del archivo  listadevariables2.csv, es la siguiente:
nombrevar_simbolotrab|unidad_trab|simbolo_si|unidad_si|
tiempo:t,tarda:t,tiempo vuelo:tv,tiempo máximo:tmax|s,min,h|t|s
...
De la misma forma se hace con las diversas variables.
'''
dfvar = pd.read_csv('dataset/listadevariables2.csv', sep='|', encoding = "ISO-8859-1")
descripción = dfvar['nombrevar_simbolotrab'] # Nombre de la variable
unidades_trab = dfvar['unidad_trab'] # Unidades de trabajo
variable = dfvar['simbolo_si'] # Símbolo según el SI
unidades_si = dfvar['unidad_si'] # Unidades según el SI

#dictdesc = {}
contdep = 0
contindep = 0
contambos = 0
conttotal = 0
contninguno = 0
contaciertosindep = 0
contaciertosdep = 0
conttotalvarindep = 0
conttotalvardep = 0
lst_ninguno = []
lst_fallaindep = []
lst_falladep = []
lst_enunciado = []  # Lista de oraciones en el enunciado
lst_oracion = []  # Lista de palabras de la oración en el enunciado

#for line in descripción:
#    for t in line.split(','):
        # diccionario con el nombre de la variable de trabajo y el símbolo de trabajo
#        dictdesc[t.split(":")[0]] = t.split(":")[1]  
        
#print(dictdesc)

#sys.exit()

for contenunciado in range(len(data['enunciados'])): # Recorre cada enunciado
    
    lst_enunciado = data['enunciados'][contenunciado].split('. ') # Enunciado
    #print(contenunciado,lst_enunciado)
    
    #contoracion=0
    lst_dep = []
    lst_indep = []
    for contoracion in range(len(lst_enunciado)): # Recorre cada oración del enunciado
        #print('Siguiente oración',contoracion)
        #input()
        lst_oracion = lst_enunciado[contoracion].split() # Oración del enunciado
        analizar_oracion(lst_oracion, unidades_trab, descripción, unidades_si, variable, lst_dep, lst_indep)

    #print('Referencia')
    #print(contenunciado,'Datos de Entrada:\n',data['varindep'][contenunciado])
    #print('Calcular:\n',data['vardep'][contenunciado])
    #print('Identificados')
    #print('Datos de Entrada:\n',lst_indep)
    #print('Calcular:\n',lst_dep)
    #input()
    #lista_estadisticas
    if str(lst_indep) != data['varindep'][contenunciado] and str(lst_dep) != data['vardep'][contenunciado]:
        contninguno += 1
        #print('No Acerto Ninguno', contninguno)
        lst_ninguno.append(contenunciado)
        lst_falladep.append(contenunciado)
        lst_fallaindep.append(contenunciado)
        #input()
    if str(lst_indep) == data['varindep'][contenunciado] and str(lst_dep) == data['vardep'][contenunciado]:
        contindep += 1
        contdep += 1
        contambos += 1
        #print('Acerto ambos',contambos)
        
    elif str(lst_indep) == data['varindep'][contenunciado]:
        contindep += 1
        #print('Acerto Var Ind', contindep)
        lst_falladep.append(contenunciado)
        #input()
    elif str(lst_dep) == data['vardep'][contenunciado]:
        contdep += 1
        #print('Acerto Var Dep', contdep)
        lst_fallaindep.append(contenunciado)
        #input()
    
    conttotal += 1
    conttotalvarindep += len(lst_indep)
    conttotalvardep += len(lst_dep)
    contaciertosindep += conteo(convertir_str_list(data['varindep'][contenunciado], 5), lst_indep)
    contaciertosdep += conteo(convertir_str_list(data['vardep'][contenunciado], 3), lst_dep)
    #input('Siguiente enunciado')
print_resultados_variables(contaciertosindep, conttotalvarindep, contaciertosdep, conttotalvardep)
print_resultados_enunciados(contninguno, conttotal, contindep, contdep, contambos, lst_ninguno, lst_fallaindep, lst_falladep)
