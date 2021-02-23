# Importar módulos
import numpy as np
from sympy import symbols, solve

def main():
    # Lectura de datos
    fe = open('Ec_Cinematica.txt', 'r')
    lista_ec = []
    for line in fe.readlines():
        line = line.strip('\n')
        lista_ec.append(line)
    unidades = np.genfromtxt('Unidades.txt', dtype = 'str')

    # Obtención del número de variables y ecuaciones
    dim = np.shape(unidades)
    n_var = dim[0]
    n_ec = len(lista_ec)

    # Conversión de variables en variables simbólicas
    variables = list(unidades[:, 0])
    variables = symbols(variables)

    # Creación e inicialización de la matriz
    matriz = np.zeros((n_ec+8,n_var+2))
    # dimensiones = matriz.shape
    # filas = range(1, dimensiones[0])
    # columnas = range(1, dimensiones[1])

    # Conversión de la matriz numérica en matriz de cadenas
    matriz = matriz.astype(dtype = str)

    # Asignación de variables, ecuaciones y unidades
    matriz[0, 1: n_var + 1] = unidades[:, 0].T
    matriz[1: n_ec+1, 0] = lista_ec
    matriz[n_ec + 2: n_ec + 5, 1: n_var + 1] = unidades[:, 1: 4].T

    # Asignación del resto de celdas de cadenas
    matriz[0, 0] = 'Relación'
    matriz[n_ec + 1, 0] = 'Ocurrencias de v'
    matriz[n_ec + 2, 0] = 'Unidades de trabajo'
    matriz[n_ec + 3, 0] = 'Unidades SI'
    matriz[n_ec + 4, 0] = 'Símbolo estándar'
    matriz[n_ec + 5, 0] = 'Valor'
    matriz[n_ec + 6, 0] = 'Secuencia de dato'
    matriz[n_ec + 7, 0] = 'Nº de relación'
    matriz[0, n_var + 1] = 'Variables desconocidas'
    matriz[n_ec + 2: n_ec + 8, n_var + 1] = ''

    # Asignar uno si la variable está presente en una ecuación determinada
    f1(matriz, n_ec, n_var)

    # Extracción de la submatriz superior e inferior
    submat = f2(matriz, 1, 1, n_ec + 1, n_var + 1)
    submat2 = f2(matriz, n_ec + 5, 1, n_ec + 7, n_var)


    # Ciclo para obtener la columna de variables desconocidas
    for i in range(0, n_ec):
        submat = f3(submat, i, n_var - 1)

    # Ciclo para obtener las ocurrencias de variables desconocidas
    for i in range(0, n_var):
        submat = f4(submat, i, n_ec - 1)

    # Inicialización de variables
    cvc = 1
    col_var = []
    fila_ec = []
    secuencia = 0
    lista_indices = []
    var_no_disp_user = []
    lista_val = []
    lista_ind = []
    pares = 1
    contador = 0
    edicion = False

    # Ejecutar el ciclo mientras existan variables desconocidas (cvc es el contador de variables desconocidas)
    while cvc > 0:
        hay_uno = False

        # Determinar si existe una ecuación que posea sólo una incógnita, y, de existir, determinar además el índice de dicha incógnita
        for i in range(0, n_ec):
            if submat[i, n_var] == 1:
                hay_uno = True
                fila_ec = i
                for j in range(0, n_var):
                    if submat[i, j] == 1:
                        col_var = j;

        # Despeje de una incógnita de una ecuación determinada
        if hay_uno:

            # Crear una lista de variables independientes y una lista de valores de variables independientes de una ecuación determinada
            lista_var, lista_val = [], []
            for i in range(0, n_var):
                if unidades[i, 0] in lista_ec[fila_ec]:
                    if not (col_var == i):
                        lista_var.append(variables[i])
                        lista_val.append(submat2[0, i])
            diccionario = dict(zip(lista_var, lista_val))

            # Obtener una ecuación en función de la variable dependiente
            expr = solve(lista_ec[fila_ec],variables[col_var])

            # Sustitución de los valores de las variables independientes en la expresión anterior
            submat2[0, col_var] = expr[0].evalf(subs=diccionario)

            # Actualizar submat una vez calculada una variable dependiente
            f5(submat, col_var, n_ec)
            f4(submat, col_var, n_ec - 1)
            for i in range(0, n_ec):
                submat = f3(submat, i, n_var - 1)

            # Contador para asignar la secuencia del dato (calculado por el programa)
            secuencia = secuencia + 1
            submat2[1, col_var] = secuencia

            # Asigna el número de la ecuación empleada para el cálculo a la fila "Número de relación"
            submat2[2, col_var] = fila_ec + 1

            # Actualizar la lista de índices de variables conocidas (suministradas por el usuario o calculadas)
            lista_indices.append(col_var)
            
        else:

            # Modo de recepción de datos
            if (pares == 1) and (edicion == False):
            
                # Lectura de datos
                datos = leer_datos(unidades, n_var, lista_indices, var_no_disp_user, submat2)

                # Si se produjo un error al leer los datos, solicitarlos nuevamente hasta que no se produzca ningún error
                while datos[1] == False:
                    datos = leer_datos(unidades, n_var, lista_indices, var_no_disp_user, submat2)

                # Almacenamiento de la variable booleana que indica si hubo o no edicion de datos en una variable temporal
                edicion = datos[4]
                    
                # Número de pares de datos (un par está constituído por el índice de una variable y su respectivo valor)
                pares = len(datos[5])
                pares_iniciales = len(datos[5])

                # Lista de valores e índices de las variables correspondientes
                lista_val = datos[6]
                lista_ind = datos[5]

                # Actualizar la lista de variables introducidas por el usuario (no disponibles)
                if edicion == False:
                    var_no_disp_user.append(unidades[lista_ind[0], 0])

                # Eliminar el índice de una variable de la lista de índices
                if datos[7] == True:
                    lista_indices.remove(datos[2])

                # Introducir la variable suministrada por el usuario y actualizar las submatrices
                if edicion == False:
                    submat2[0, lista_ind[0]] = lista_val[0]
                    f5(submat, lista_ind[0], n_ec)
                    f4(submat, lista_ind[0], n_ec - 1)
                    for i in range(0, n_ec):
                        submat = f3(submat, i, n_var - 1)

                    # Contador para asignar la secuencia del dato (suministrado por el usuario)
                    secuencia = secuencia + 1
                    submat2[1, lista_ind[0]] = secuencia

                    # Actualizar la lista de índices de variables conocidas (suministradas por el usuario o calculadas)
                    if edicion == False:
                        lista_indices.append(lista_ind[0])

            # Modo de edición de datos
            if edicion == True:

                # Inicializar la matriz principal y las submatrices. Sólo se hace cuando se comienza a procesar un conjunto de datos
                if pares == pares_iniciales:
                    secuencia = 0
                    contador = 0

                    matriz[1 : n_ec + 8, 1 : n_var + 2] = 0
                    matriz[n_ec + 2: n_ec + 5, 1: n_var + 1] = unidades[:, 1: 4].T
                    matriz[n_ec + 2: n_ec + 8, n_var + 1] = ''

                    f1(matriz, n_ec, n_var)
                    submat = f2(matriz, 1, 1, n_ec + 1, n_var + 1)
                    submat2 = f2(matriz, n_ec + 5, 1, n_ec + 7, n_var)

                    # Ciclo para obtener la columna de variables desconocidas
                    for i in range(0, n_ec):
                        submat = f3(submat, i, n_var - 1)

                    # Ciclo para obtener las ocurrencias de variables desconocidas
                    for i in range(0, n_var):
                        submat = f4(submat, i, n_ec - 1)
                    
                # Lista de valores e índices de las variables correspondientes    
                lista_val = datos[6]
                lista_ind = datos[5]

                # Actualización de submatrices
                submat2[0, lista_ind[contador]] = lista_val[contador]
                f5(submat, lista_ind[contador], n_ec)
                f4(submat, lista_ind[contador], n_ec - 1)
                for i in range(0, n_ec):
                    submat = f3(submat, i, n_var - 1)

                # Contador para asignar la secuencia del dato (suministrado por el usuario)
                secuencia = secuencia + 1
                submat2[1, lista_ind[contador]] = secuencia

                # Control de la salida del modo de edición
                if pares == 1:
                    edicion = False

                # Actualización del número de pares
                if pares > 1:
                    pares = pares - 1

                # Actualización del contador de pares
                contador = contador + 1
            
        # Actualizar la última columna (sumatoria de variables)
        f4(submat, n_var, n_ec - 1)
        cvc = submat[n_ec, n_var]

    # Actualización de la matriz principal
    matriz[1 : n_ec + 2, 1: n_var + 2] = submat
    matriz[n_ec + 5: n_ec + 8, 1: n_var + 1] = submat2

    # Muestra de resultados
    print('', 'La matriz final es: ', sep='\n')
    print(matriz,'\n')

# Colocar 1 si la ecuación contiene a la variable y 0 en caso contrario
def f1(matriz, n_ec, n_var):
    for i in range(1, n_ec + 1):
        for j in range(1, n_var + 1):
            if matriz[0, j] not in matriz[i, 0]:
                matriz[i, j] = 0
            else:
                matriz[i, j] = 1
    return(matriz)

# Obtener submatriz de cadenas y convertirla a tipo real
def f2(matriz, start_row, start_col, m, n):
    submatriz = matriz[start_row : m + 1, start_col : n + 1]
    submatriz = submatriz.astype(dtype = float)
    return(submatriz)

# Sumar fila de variables desconocidas
def f3(submatriz, row, n):
    submatriz[row, n + 1] = submatriz[row, 0: n + 1].sum()
    return(submatriz)

# Sumar columna de variables desconocidas
def f4(submatriz, col, m):
    submatriz[m + 1, col] = submatriz[0: m + 1, col].sum()
    return(submatriz)

# Restar 1 a una columna
def f5(submatriz, col, m):
    for i in range(0, m):
        if submatriz[i, col] > 0:
            submatriz[i, col]= submatriz[i, col] - 1
    return(submatriz)

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
                        if not(j == indice):
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

if __name__ == '__main__': main()
