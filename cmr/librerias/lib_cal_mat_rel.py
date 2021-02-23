'''
Biblioteca de funciones para ser empleada en las operaciones de lectura
y cálculo de las variables en una matriz de relaciones.
'''
def init_mat(matriz, n_ec, n_var):
    '''
    Devuelve la matriz con celdas de valor 1 si la variable interviene en la ecuación y 0 en caso contrario
    matriz: es la matriz con las ecuaciones y las variables del modelo matemático en la columna 0 y fila 0 respectivamente
    n_ec: es la cantidad de ecuaciones del modelo matemático
    n_var: es el número de variables que interviene en el modelo matemático
    '''
    for i in range(1, n_ec + 1): # recorre las ecuaciones ubicadas en la columna 0
        for j in range(1, n_var + 1): # recorre los símbolos de las variables ubicadas en la fila 0
            if matriz[0, j] not in matriz[i, 0]:
                matriz[i, j] = 0 # la variable no está en la ecuación
            else:
                matriz[i, j] = 1 # la variable se encuentra en la ecuación
    return matriz


def conv_strtofloat(matriz, start_row, start_col, m, n):
    '''
    Convierte la submatriz del tipo de dato str a tipo float
    start_row: índice de la fila de inicio
    start_col: índice de la columna de inicio
    m: cantidad de filas de la submatriz
    n: cantidad de columnas de la submatriz
    '''
    submatriz = matriz[start_row : m + 1, start_col : n + 1] # obtiene la submatriz de matriz
    submatriz = submatriz.astype(dtype=float) # convierte al tipo de dato float la submatriz
    return submatriz


def total_row(submatriz, row, n):
    '''
    Sumar los valores de una fila y lo almacena al final de la fila.
    row: índice de la fila a sumar
    n: cantidad de elementos a sumar en la fila.
    '''
    # guarda en la última celda de la fila, la suma de los elementos de la fila
    # desde la posición 0 hasta la penúltima celda de la fila
    submatriz[row, n + 1] = submatriz[row, 0: n + 1].sum()
    return submatriz


def total_col(submatriz, col, m):
    '''
    Sumar los valores de una columna y lo almacena al final de la columna.
    col: índice de la columna a sumar
    m: cantidad de elementos a sumar en la columna.
    '''
    # guarda en la última celda de la columna, la suma de los elementos de la columna
    # desde la posición 0 hasta la penúltima celda de la columna
    submatriz[m + 1, col] = submatriz[0: m + 1, col].sum()
    return submatriz


def resta_unidad_col(submatriz, col, m):
    '''
    Devuelve una submatriz a la cual se le resta 1 a una columna determinada
    col: índice de la columna a restarle uno en cada celda
    m: cantidad de elementos en la fila
    '''
    for i in range(0, m): # recorre toda la columna
        if submatriz[i, col] > 0:
            submatriz[i, col] -= 1
    return submatriz


def leer_datos(unidades, n_var, lista_indices, var_no_disp_user, submat2):
    try:
        # Inicialización de variables
        valor = None
        sin_error = False
        indice = None
        var_disp = []
        var_dic = []
        val_dic = []
        edito = False
        elimino = False

        # Ciclo para recorrer los índices de todas las variables
        for i in range(0, n_var):
            esta = False

            # Ciclo para recorrer la lista de índices de las variables que se conocen, bien sea porque fueron
            # suministradas por el usuario o porque fueron calculadas por el programa
            if len(lista_indices) > 0:
                for j in range(0, len(lista_indices)):
                    if i == lista_indices[j]:
                        esta = True

            # Si una variable determinada no era conocida, agregarla a la lista de variables disponibles
            # Si una variable determinada es conocida, agregarla a la lista de variables sujetas a edición o eliminación (no disponibles)
            if esta == False:
                var_disp.append(unidades[i, 0])

        variable = input('\n' + 'Seleccione la variable: ' + str(var_disp) + ' ' + '\n' + 'Introduzca ''edit'' si desea editar una variable o ''delete'' si desea eliminarla.' + '\n')

        # Edición de variable
        if variable == 'edit':
            variable = input('\n' + 'Seleccione la variable que desea editar: ' + str(var_no_disp_user) + ' ')

            edito = True
            encontrada = False

            # Si la variable suministrada por el usuario se encuentra en la lista de variables disponibles para editar, buscarla
            # en la primera columna del vector unidades para determinar su índice
            if variable in var_no_disp_user:
                for i in range(0, n_var):
                    if variable == unidades[i, 0]:
                        encontrada = True
                        indice = i

            if encontrada == False:
                raise ValueError

            valor = float(input('Introduzca el nuevo valor de la variable: '))

            # Creación de lista de los índices de las variables suministradas por el usuario con los valores correspondientes y
            # que contiene el valor actualizado de la variable editada
            for i in range(0, len(var_no_disp_user)):
                for j in range(0, n_var):
                    if var_no_disp_user[i] == unidades[j, 0]:
                        var_dic.append(j)
                        if j == indice:
                            val_dic.append(valor)
                        else:
                            val_dic.append(submat2[0, j])

        # Eliminación de variable
        elif variable == 'delete':
            variable = input('\n' + 'Seleccione la variable que desea eliminar: ' + str(var_no_disp_user) + ' ')

            edito = True
            elimino = True
            encontrada = False

            # Si la variable suministrada por el usuario se encuentra en la lista de variables disponibles para editar, buscarla
            # en la primera columna del vector unidades para determinar su índice
            if variable in var_no_disp_user:
                for i in range(0, n_var):
                    if variable == unidades[i, 0]:
                        encontrada = True
                        indice = i

            if encontrada == False:
                raise ValueError

            # Actualización de la lista de variables suministradas por el usuario
            var_no_disp_user.remove(unidades[indice, 0])

            # Creación de lista de los índices de las variables suministradas por el usuario con los valores correspondientes y
            # que contiene el valor actualizado de la variable editada
            for i in range(0, len(var_no_disp_user)):
                for j in range(0, n_var):
                    if var_no_disp_user[i] == unidades[j, 0]:
                        if not j == indice:
                            var_dic.append(j)
                            val_dic.append(submat2[0, j])

        # Suministro de una variable por parte del usuario
        else:
            encontrada = False

            # Si la variable suministrada por el usuario se encuentra en la lista de variables disponibles, buscarla
            # en la primera columna del vector unidades para determinar su índice
            if variable in var_disp:
                for i in range(0, n_var):
                    if variable == unidades[i, 0]:
                        encontrada = True
                        indice = i

            if encontrada == False:
                raise ValueError

            valor = float(input('Introduzca su valor: '))

            # Creación de lista de los índices de las variables suministradas por el usuario con los valores correspondientes y
            # que contiene el valor actualizado de la variable editada
            var_dic.append(indice)
            val_dic.append(valor)

        # Variable booleana que indica que el usuario suministró correctamente un dato
        sin_error = True

    except:
        print('Introdujo una variable incorrecta o un valor incorrecto de la misma.', 'Por favor, introduzca nuevamente la variable.', sep='\n')
    return (valor, sin_error, indice, var_no_disp_user, edito, var_dic, val_dic, elimino)
