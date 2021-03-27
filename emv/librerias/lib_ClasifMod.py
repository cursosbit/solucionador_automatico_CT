
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import confusion_matrix

from nltk.corpus import stopwords # version: 0.19.2
import matplotlib.pyplot as plt
import numpy as np
import itertools
from keras import utils
from keras.preprocessing import text

from keras.layers.noise import AlphaDropout
from keras.layers import Dense, Activation, Dropout
from keras.models import Sequential

# Se importa las librerias propias
from librerias.lib_IdVar import detectar_vars, dividir_datos

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
    

def clasificador(data):
    
    # Parámetros
    max_words = 40
    batch_size = 3
    epochs = 8
    #plot = True
    
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
    
    #enunciadosdesordenados2.csv
    #data = pd.read_csv('dataset/enunciados124.csv',sep='|',encoding = "ISO-8859-1")
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
    
    plt.figure(2)
    plt.plot(range(epochs), history.history['loss'], 'g--', label='Loss')
    plt.plot(range(epochs), history.history['val_loss'], 'g-', label='Val Loss')
    plt.plot(range(epochs), history.history['acc'], 'b--', label='Acc')
    plt.plot(range(epochs), history.history['val_acc'], 'b-', label='Val Acc')
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.legend()
    plt.twinx()
    plt.ylabel('acc')
    
        