from nltk.corpus import stopwords # version: 0.19.2
import matplotlib.pyplot as plt
import numpy as np
import itertools
from keras.layers.noise import AlphaDropout
from keras.layers import Dense, Activation, Dropout
from keras.models import Sequential


def create_network(max_words,num_classes,n_dense=1,dense_units=256,activation='selu',dropout=AlphaDropout,dropout_rate=0.5,kernel_initializer='lecun_normal',optimizer='adam'):
    """Generic function to create a fully-connected neural network.
    # Arguments
        n_dense: int > 0. Number of dense layers.
        dense_units: int > 0. Number of dense units per layer.
        dropout: keras.layers.Layer. A dropout layer to apply.
        dropout_rate: 0 <= float <= 1. The rate of dropout.
        kernel_initializer: str. The initializer for the weights.
        optimizer: str/keras.optimizers.Optimizer. The optimizer to use.
        num_classes: int > 0. The number of classes to predict.
        max_words: int > 0. The maximum number of words per data point.
    # Returns
        A Keras model instance (compiled).
    """
    # This model trains very quickly and 10 epochs are already more than enough
    # Training for more epochs will likely lead to overfitting on this dataset
    # You can try tweaking these hyperparamaters when using this model with your own data
    #Creación del modelo con keras
    model = Sequential()
    #1 Capa - Agrega una capa de entrada de arreglo de salida de forma (*, dense_units)
    # y arreglo de entrada  de forma (*, max_words)
    model.add(Dense(dense_units, input_shape=(max_words,),
                    kernel_initializer=kernel_initializer))
    #2 Capa - Agrega una capa relu
    model.add(Activation('relu')) # Aplica la función de activación relu
    #3 Capa - Agrega una capa Dropout con dropout_rate porcentaje de neuronas
    model.add(Dropout(dropout_rate)) # establecer´ıa entradas a 0 en el dropout_rate % de los casos.
    for i in range(n_dense - 1):
        model.add(Dense(dense_units, kernel_initializer=kernel_initializer))
        model.add(Activation(activation))
        model.add(dropout(dropout_rate))
    #4 Capa - Agrega una capa completamente conectada, con dimensión num_classes de salida
    model.add(Dense(num_classes))
    #5 Capa - Agrega una capa de activación de tipo softmax
    model.add(Activation('softmax')) # Aplica la función de activación softmax
    # Se le indica al modelo el tipo de pérdida (loss), el optimizador de los 
    # pesos de las conexiones de las neuronas y las metricas a obtener
    model.compile(loss='categorical_crossentropy', # Entropía cruzada
                  optimizer=optimizer, # Optimizador
                  metrics=['accuracy'])
    model.summary()
    return model


def filtros1(e): # Filtros aplicados a los enunciados
    #Convierte el texto en minúsculas
    e['enunciados'] = e['enunciados'].str.lower()
    # print ('Convertido en minúsculas\n', e['enunciados'][0])
    # print("\n")
    e['enunciados']=e['enunciados'].str.replace('[:,¿?()=]²', ' ')
    #Elimina las palabras vacías en español
    stop = stopwords.words('spanish')
    e['enunciados'] = e['enunciados'].apply(lambda x: ' '.join([word for word in x.split() if word not in (stop)]))
    # print ('Eliminando las palabras vacías\n', e['enunciados'][0])
    # print("\n")
    #Elimina varios espacios seguidos por uno solo
    e['enunciados']=e['enunciados'].str.replace('\s+', ' ')
    # print('Elimina varios espacios seguidos\n', e['enunciados'][0])
    # print("\n")


def plot_confusion_matrix(cm, classes, title='Confusion matrix',
                          cmap=plt.cm.Blues):
    # This utility function is from the sklearn docs: http://scikit-learn.org/stable/auto_examples/model_selection/plot_confusion_matrix.html
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title, fontsize=20)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=30, fontsize=10)
    plt.yticks(tick_marks, classes, fontsize=10)
    fmt = '.2f'
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], fmt), horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")
    plt.ylabel('True label', fontsize=12)
    plt.xlabel('Predicted label', fontsize=12)    
    
    