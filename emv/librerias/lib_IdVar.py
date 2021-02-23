'''
Biblioteca para la identificación de variables dependientes e independientes en una oración

'''

def analizar_oracion(oracion, unidades_trab, descripción, unidades_si, variable, dep, indep):

    '''
    input:
        oracion: oración del enunciado a revisar
        unidades_trab: unidades de trabajo de las variables según el enunciado
        descripción: nombre de trabajo de la variable
        unidades_si: unidad según el SI
        variable: nombre de la variable según el SI

    output:
        dep: lista de variables dependientes conformada por     [simbolo_si,simbolo_trab,unidad_si]
        indep: lista de variables independientes conformada por [simbolo_si,simbolo_trab,valor,unidad_trab,unidad_si]

    funciones:
        es_numero
        es_var_independiente
        get_indice_simbolo_trab
        get_indice_unidad_trab
        llenarlistadatos
        set_var_indep
        set_var_dep

    '''
    # global caso

    # oracion=enunciado[contoracion].split() # Oración del enunciado

    contpalabra = 0

    # print(oracion)
    # input()
    while (contpalabra <= len(oracion)-1):
        # print(oracion[contpalabra])
        
        if (get_indice_simbolo_trab(oracion[contpalabra].replace('.',''), descripción) != -1 or 
            (contpalabra < len(oracion)-1 and get_indice_simbolo_trab(oracion[contpalabra] + ' ' + oracion[contpalabra+1].replace('.',''), descripción) != -1) or
            (es_numero(oracion[contpalabra]) and (oracion[contpalabra-1] != 'figura' and oracion[contpalabra-1] != 'tabla') and 
            (contpalabra<len(oracion)-1 and get_indice_unidad_trab(oracion[contpalabra+1].replace('.', ''), unidades_trab) != -1))):

            lstDatos = ['','','','','','']
            lstDatos = llenarlistadatos(lstDatos, oracion, contpalabra, descripción)
            # print(contpalabra,len(oracion),oracion)
            # print(lstDatos)
            caso = es_var_independiente(lstDatos, unidades_trab, descripción)
            # print(caso)

            if caso != -1: # Variable independiente
                set_var_indep(caso, contpalabra, lstDatos, unidades_trab, oracion, variable, unidades_si, indep, descripción)
            else: # Variable dependiente
                set_var_dep(dep, oracion, contpalabra, descripción, unidades_si, variable)

            # print(oracion)
            contpalabra -= 1
        # else:
            #print('Descartada...')
        contpalabra += 1 # Cuenta cada palabra de la lista oración
    # contoracion=contoracion+1 # Cuenta cada oración del enunciado


def conteo(lst1, lst2):
    '''
    conteo, devuelve la cantidad de elementos que son comunes en ambas listas.
    Input:
        lst1, lista anidada de variables de referencia
        lst2, lista anidada de variables identificadas
    Output
        c: cantidad de coincidencias entre las listas
    '''
    
    #Referencia lst1
    #Identificado lst2
    #if len(lst2)>len(lst1):
        #print('Identificación en exceso')
    #elif len(lst2)<len(lst1):
        #print('Identificación deficiente')
    
    c = 0 # Cantidad de elementos que son comunes en ambas listas
    i = 0
    # nl1=len(lst1)
    while i < len(lst1): # Referencia
        j = i
                
        while j < len(lst2):
     
            if lst1[i] == lst2[j]:
                lst1.pop(i)
                lst2.pop(j)
                c += 1
                i -= 1
                break

            j += 1

        i += 1
    # if c==len(lst1):
        # print('Todos acertados')
    # else:
        #print(nl1-c,' desaciertos')
    # print(c, ' aciertos')
    return c


def convertir_str_list(cad,n):
    '''
    convertir_str_list, Convierte una cadena cad en una lista de listas, donde 
    cada lista interna esta conformada por n elementos.
    Input:
        cad, cadena a convertir en una lista de listas.
        n, cantidad de elemntos de la lista interna.
    '''
    cad=cad.replace('[', '')
    cad=cad.replace(']', '')
    cad=cad.replace('\'', '')
    cad=cad.replace(' ', '')
    l = cad.split(',')
    l3 = []
    j = 0
    # print(l)
    for i in range(len(l) // n):
        l2 = []
        while j < (i + 1) * n:
            l2.append(l[j])
            j += 1
        l3.append(l2)

    # print(l3)
    return(l3)


def dividir_datos(porc_train, data):

    # División de los datos para entrenamiento y prueba
    '''
    Input:
        porc_train: porcentaje de división de datos
        data: dataframe panda con los datos de los enunciados
    Output:
        train_size
        test_size
        enunciado_train
        modelo_train
        enunciado_test
        modelo_test
    ''' 
    train_size = int(len(data) * porc_train)
    test_size = len(data) - train_size
    print ("Train size: %d" % train_size)
    print ("Test size: %d" % test_size)
    enunciado_train = data['enunciados'][:train_size]
    modelo_train = data['modelos'][:train_size]
    enunciado_test = data['enunciados'][train_size:]
    modelo_test = data['modelos'][train_size:]
    return train_size, test_size, enunciado_train, modelo_train, enunciado_test, modelo_test


def es_numero(cad):
    '''
    es_numero, verifica si s es un número o no
    Input:
        cad, es la cadena a verificar si es un número válido.
    Output:
        True, es un número.
        False, no es un número
    '''
    try:
        float(cad) # for int, long and float
    except ValueError:
        try:
            complex(cad) # for complex
        except ValueError:
            return False
    return True


def es_unidad_simbtrab(unidad, UnidadSimbTrab):
    '''
    es_unidad_simbtrab, verifica si el parámetro unidad es una unidad válida 
    buscándola en la lista Lista_unidad_simb_trab que contiene todas las unidades
    de medida relaciondas al identificador de la variable.

    Input:
        unidad, es la unidad a buscar.
        Lista_unidad_simb_trab, lista de unidades de trabajo válidas.
    Output:
        True: es una unidad válida
    '''
    
    return unidad in UnidadSimbTrab
    
'''
    # print(lstUnidadSimbTrab)
    print(unidad)
    print(UnidadSimbTrab)
    
    for u in UnidadSimbTrab.split(','):
        print(UnidadSimbTrab)
        if u == unidad:
            return True
    return False
'''

def es_var_independiente(lstDatos,unidades_trab,descripción):
    '''
    es_var_independiente, verifica si la lista lstDatos corresponde a la 
    estructura de una variable independiente.
    Parámetro:
        lstDatos, es una lista que contiene los probables elementos de una 
        variable independiente nombre,nombre,valor,unidad,nombre,nombre.
    '''
    caso = -1
    if es_numero(lstDatos[2]) and get_indice_unidad_trab(lstDatos[3], unidades_trab) != -1:        
        if (get_indice_simbolo_trab(lstDatos[0] + ' ' + lstDatos[1], descripción) != -1):            
            if (es_unidad_simbtrab(lstDatos[3],unidades_trab[get_indice_simbolo_trab(lstDatos[0] + ' ' + lstDatos[1], descripción)])):
                caso = 0
        elif get_indice_simbolo_trab(lstDatos[1], descripción) != -1:
            if (es_unidad_simbtrab(lstDatos[3], unidades_trab[get_indice_simbolo_trab(lstDatos[1], descripción)])):
                caso = 1
        else:            
            if get_indice_simbolo_trab(lstDatos[4] + ' ' + lstDatos[5], descripción) != -1 and (es_unidad_simbtrab(lstDatos[3], unidades_trab[get_indice_simbolo_trab(lstDatos[4] + ' ' + lstDatos[5], descripción)])):
                caso = 2
            elif get_indice_simbolo_trab(lstDatos[4], descripción) != -1 and (es_unidad_simbtrab(lstDatos[3], unidades_trab[get_indice_simbolo_trab(lstDatos[4], descripción)])):
                caso = 3
            else:
                caso = 4
    return caso


def filtros2(e): #Reemplaza símbolos, caracteres especiales y palabras compuestas
    dict = {'tiempo tarda':' tiempo ','tiempo tardo':' tiempo',
          'cuánto tiempo':' tiempo','cuanto tardo':' tiempo',
          'cuánto demora':' tiempo ','cuanto demora':' tiempo ',
          'distancia recorre':' distancia ','distancia recorrido':' distancia',
          'distancia recorrida':' distancia','cuán lejos':' distancia',
          'desplazamiento realizado':' distancia','cuánto desplaza':' distancia ',
          'máxima altura':' altura máxima',
          'rapidez':'velocidad',
          'máxima velocidad':' velocidad máxima',
          'm/s cada segundo':'m/s²','metros por segundo':'m/s','segundos':' s ',' seg':' s ',
          'metros':'m',
          'alcanzar reposo':'velocidad final 0 m/s',
          'hasta detenerse':'velocidad final 0 m/s',
          'detenerse completo':'velocidad final 0 m/s',
          'detiene completo':'velocidad final 0 m/s',
          'reposo':'velocidad inicial 0 m/s',
          'velocidad uniformemente':'velocidad',
          'aceleración debida':'aceleración',
          'aceleración permanece constante':'aceleración',
          'x10^':'E',
          ' dos ':' 2 ','tres':'3','cuatro':'4','cinco':'5','seis':'6','siete':'7',
          'ocho':'8','nueve':'9','diez':'10','duodécimo':'12',
          'º':' º ',
          'cuántos radianes':'ángulo',
          'ángulo inclinación':'ángulo',
          'cuántas revoluciones':'número revoluciones',
          'número vueltas':'número revoluciones',
          'qué tan rápido gira':'w',
          'cuánto pesará':'masa'
          }
    for i in range(len(e['enunciados'])):
        for key, val in dict.items():
            e['enunciados'][i] = e['enunciados'][i].replace(key, val)
    #print ('Simplificación ortografica\n',e['enunciados'][0])
    #print("\n")
    

def get_indice_simbolo_trab(cad_descripcionvartrab, descripción):
    '''
    get_indice_simbolo_trab, Devuelve el índice donde se encuentra 
    cad_descripcionvartrab en el pandas.core.series.Series descripción o -1 
    si no lo encuentra.
    
    Parámetro:
        cad_descripcionvartrab, es una cadena conformada por uno o dos nombres 
        de una posible variable.
        descripción, es una lista que contiene nombrevar_simbolotrab extraído de listadevariables2.csv
        
    '''

    for i in range(len(descripción)):
        for j in range(len(descripción[i].split(','))):
            if cad_descripcionvartrab == descripción[i].split(',')[j].split(':')[0]:
                return i
    return -1


def get_indice_unidad_trab(unid, unidades_trab):
    '''
    get_indice_unidad_trab, devuelve el indice según la unidad de trabajo unid, 
    o -1 si no la encuentra.
    Parámetro:
        unid, es la unidad de medida que se verifica si es una unidad de 
        trabajo válida
    '''
    for i in range(len(unidades_trab)):
        for u in unidades_trab[i].split(','):
            if unid == u.lower():
                return i
    return -1


def get_simbolo_trab(cad_descripcionvartrab, descripción):
    '''
    get_simbolo_trab, Devuelve el símbolo de la variable de trabajo,
    dada la descripción de la variable cad_descripcionvartrab, o -1 si no 
    lo encuentra.
    Parámetro:
        cad_descripcionvartrab, es el nombre de la posile variable a la cual se le 
        busca el símbolo de trabajo respectivo.
    '''
    for i in range(len(descripción)):
        for j in range(len(descripción[i].split(','))):
            if cad_descripcionvartrab == descripción[i].split(',')[j].split(':')[0]:
                return descripción[i].split(',')[j].split(':')[1]
    return -1

def llenarlistadatos(lstDatos, oracion, contpalabra, descripción):
    '''
    llenarlistadatos, devuelve una lista con los elementos corresdpondientes para identificar a una variable independiente.
    Parámetros:
        lstDatos, lista con los elementos de una posible variable independiente
        oracion, segmento del enunciado para buscar posibles variables independientes
        contpalabra, contador de palabras
    '''
    if contpalabra < len(oracion)-3 and (get_indice_simbolo_trab(oracion[contpalabra] + ' ' + oracion[contpalabra+1], descripción) != -1):# Caso 0
        lstDatos = [oracion[contpalabra], oracion[contpalabra+1], oracion[contpalabra+2], oracion[contpalabra+3].replace('.', ''), '', '']
    elif contpalabra < len(oracion)-2 and (get_indice_simbolo_trab(oracion[contpalabra], descripción) != -1):
        lstDatos = ['', oracion[contpalabra], oracion[contpalabra+1], oracion[contpalabra+2].replace('.',''), '','']
    elif contpalabra < len(oracion)-3 and (es_numero(oracion[contpalabra])):
        lstDatos = ['', '', oracion[contpalabra], oracion[contpalabra+1].replace('.', ''), oracion[contpalabra+2], oracion[contpalabra+3]]
    elif contpalabra < len(oracion)-2 and (es_numero(oracion[contpalabra])):
        lstDatos = ['', '', oracion[contpalabra], oracion[contpalabra+1].replace('.', ''), oracion[contpalabra+2],'']
    elif contpalabra < len(oracion)-1 and (es_numero(oracion[contpalabra])):
        lstDatos = ['', '', oracion[contpalabra], oracion[contpalabra+1].replace('.', ''), '', '']
    return lstDatos


def print_resultados_enunciados(contninguno, conttotal, contindep, contdep, contambos, lstNinguno, lstFallaIndep, lstFallaDep):    
    print("\nAnálisis por enunciado")
    print('Desacierto en ambos y porcentaje=\t %d \t %.2f ' % (contninguno, (contninguno / conttotal * 100)),'%')
    print('Porcentaje Aciertos Var Indep =\t %d \t %.2f ' % (contindep, (contindep / conttotal * 100)),'%')
    print('Porcentaje Aciertos Var Dep =\t %d \t %.2f ' % (contdep, (contdep / conttotal * 100)),'%')
    print('Total de aciertos en ambos y porcentaje=\t %d \t %.2f' % (contambos, (contambos / conttotal * 100)),'%')
    print('Total de enunciados=\t' , conttotal)
    print('Falla en ambos=\t', lstNinguno)
    print('Falla en Independientes=\t', lstFallaIndep)
    print('Falla en Dependientes=\t', lstFallaDep)
    
    
def print_resultados_variables(contaciertosindep, conttotalvarindep, contaciertosdep, conttotalvardep):
    print("\nAnálisis por variable")
    print('Variable independientes acertadas, Total y porcentaje=\t %d \t %d \t %.2f ' % (contaciertosindep, conttotalvarindep, (contaciertosindep * 100 / conttotalvarindep)), '%')
    print('Variable dependientes acertadas, Total y porcentaje=\t %d \t %d \t %.2f ' % (contaciertosdep, conttotalvardep, (contaciertosdep * 100 / conttotalvardep)),'%')
    print('Total de variables analizadas=\t ' , conttotalvarindep + conttotalvardep)
    print('Total de variables acertadas y porcentaje=\t %d \t %.2f ' % ((contaciertosindep + contaciertosdep), ((contaciertosindep + contaciertosdep) * 100 / (conttotalvarindep + conttotalvardep))), '%')


def set_simbolo_trab(lstDatos, caso, contpalabra, oracion, descripción):
    '''
    asignarsimbolo_trab, devuelve el simbolo de trabajo correspondiente a la variable.
    Parámetros:
        caso: depende de la estructura de la variable
        simbolo_trab: es el símbolo de trabajo de la variable según se refiere en el enunciado
        oracion, segmento del enunciado para buscar posibles variables independientes
        contpalabra, contador de palabras
        lstDatos, lista con los elementos de una posible variable independiente
    '''
            
    if caso == 0:
        simbolo_trab = get_simbolo_trab(lstDatos[0] + ' ' + lstDatos[1], descripción)
        oracion.pop(contpalabra + 3)
        oracion.pop(contpalabra + 2)
        oracion.pop(contpalabra + 1)
        oracion.pop(contpalabra)
    elif caso == 1:
        simbolo_trab = get_simbolo_trab(lstDatos[1],descripción)
        oracion.pop(contpalabra + 2)
        oracion.pop(contpalabra + 1)
        oracion.pop(contpalabra)
    elif caso == 2:
        simbolo_trab = get_simbolo_trab(lstDatos[4] + ' ' + lstDatos[5], descripción)
        oracion.pop(contpalabra + 3)
        oracion.pop(contpalabra + 2)
        oracion.pop(contpalabra + 1)
        oracion.pop(contpalabra)
    elif caso == 3:
        simbolo_trab = get_simbolo_trab(lstDatos[4],descripción)
        oracion.pop(contpalabra + 2)
        oracion.pop(contpalabra + 1)
        oracion.pop(contpalabra)
    else: # sin  símbolo de trabajo, se asigna el símbolo del SI
        simbolo_trab = ''
        oracion.pop(contpalabra + 1)
        oracion.pop(contpalabra)
    return simbolo_trab


def set_var_dep(dep, oracion, contpalabra, descripción, unidades_si, variable):
    # Se verifica que el identificador de dos palabras corresponda a una variable válida
    if contpalabra < len(oracion)-1 and get_indice_simbolo_trab(oracion[contpalabra] + ' ' + oracion[contpalabra+1].replace('.',''), descripción) != -1:
        simbolo_trab = get_simbolo_trab(oracion[contpalabra] + ' ' + oracion[contpalabra+1].replace('.',''), descripción)
        unidad_si = unidades_si[get_indice_simbolo_trab(oracion[contpalabra] + ' ' + oracion[contpalabra+1].replace('.',''), descripción)]
        simbolo_si = variable[get_indice_simbolo_trab(oracion[contpalabra] + ' ' + oracion[contpalabra+1].replace('.',''), descripción)]
        oracion.pop(contpalabra + 1)
        oracion.pop(contpalabra)
    else:
        simbolo_trab = get_simbolo_trab(oracion[contpalabra].replace('.',''), descripción)
        unidad_si = unidades_si[get_indice_simbolo_trab(oracion[contpalabra].replace('.',''), descripción)]
        simbolo_si = variable[get_indice_simbolo_trab(oracion[contpalabra].replace('.',''), descripción)]
        oracion.pop(contpalabra)
    dep.append([simbolo_si, simbolo_trab, unidad_si])
    #print(simbolo_si, ' ', simbolo_trab,' =?',' ', unidad_si,'\n')


def set_var_indep(caso, contpalabra, lstDatos, unidades_trab, oracion, variable, unidades_si,indep, descripción):
    # print(' Buscar Ind ', valor, '  ' , unidad_trab)
    # Verificar si en verdad tiene unidad de trabajo
    
    # global simbolo_trab
        
    unidad_trab = lstDatos[3]
    valor = lstDatos[2]
    simbolo_si = variable[get_indice_unidad_trab(unidad_trab, unidades_trab)]
    unidad_si = unidades_si[get_indice_unidad_trab(unidad_trab, unidades_trab)]
    simbolo_trab = ''
    
    if unidad_trab == unidad_si.lower():
        unidad_trab = unidad_si          
    # print(caso)
    # print(contpalabra)
    simbolo_trab = set_simbolo_trab(lstDatos, caso, contpalabra, oracion, descripción)
    indep.append([simbolo_si, simbolo_trab, valor, unidad_trab, unidad_si])
    # print(simbolo_si, ' ', simbolo_trab, ' =', valor, ' ', unidad_trab,' ',unidad_si,'\n')