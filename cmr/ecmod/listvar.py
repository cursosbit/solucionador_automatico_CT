#Lista de variables en una ecuación
''' En este programa dada una ecuación, se verifica sus paréntesis,
y se extraen las variables que están involucradas.
Falta:
1.- verificar validez de los operadores
2.- identificar las constantes y funciones.
3.- crear otro programa que permita reemplazar los valores de las variables
y calcule la variable dependiente, en Python para resolver se requiere una
sola expresión sin igualdad. Esto se resuelve trabajando en forma símbolica.
'''

OPERATORS = ['**', '//', '+', '-', '*', '/', '=']

class Heap:
    def __init__(self):
        self.items = []

    def empty(self):
        return self.items == []

    def include(self, item):
        self.items.append(item)

    def extract(self):
        return self.items.pop()

    def inspect(self):
        return self.items[len(self.items)-1]

    def size(self):
        return len(self.items)


def del_repeated(lista):
    '''
    Borra los repetidos
    '''
    nueva = []
    for elemento in lista:
        if elemento not in nueva:
            nueva.append(elemento)
    return nueva


def del_numbers(lista):
    '''
    Borra los números
    '''
    nueva = []

    for elemento in lista:

        if not(elemento.strip().isdigit()):
            nueva.append(elemento)
    return nueva


def del_null(lista):
    '''
    Borra los nulos
    '''
    nueva = []
    for elemento in lista:
        if elemento != '':
            nueva.append(elemento)
    return nueva


def del_operators(lista):
    '''
    Borra los operadores
    '''
    nueva = []
    for elemento in lista:
        if elemento not in OPERATORS:
            nueva.append(elemento)
    return nueva


def del_parenthesis(lista):
    '''
    Borra los parentesis
    '''
    nueva = []
    for elemento in lista:
        elemento = elemento.replace('(', '')
        elemento = elemento.replace(')', '')
        nueva.append(elemento)
    return nueva

    
def get_list_variables(ecuacion):
    '''
    Obtiene la lista de veriables de la ecuación
    '''
    ter = 0
    operador = ''
    while ter < len(ecuacion):  # De este ciclo se obtiene cada elemento por separado de la ecuación
        for operador in OPERATORS:
            cad = "".join(ecuacion[ter])  # Convertir en cadena el término de la lista
            if cad.find(operador) != -1 and len(cad) > 1 and cad != '//' and cad != '**':
                cad = cad.replace(operador, '$'+operador+'$')  # Se marca el operador
                listaz = cad.split('$')  # Devuelve una lista de elementos de la expresión
                # Se recorre todos los elementos de z
                for i in range(len(listaz)):
                    # Se convierte en cadena el término de z
                    cadp = "".join(listaz[i])
                    # Inserta todos los elementos de la lista z en ecuacion
                    ecuacion.insert(ter+i+1, cadp)
                ecuacion.pop(ter)  #Se elimina el último término
        ter = ter+1   # Se pasa al siguiente termino
    
    ecuacion = del_parenthesis(ecuacion)
    ecuacion = del_numbers(ecuacion)
    ecuacion = del_operators(ecuacion)
    ecuacion = del_null(ecuacion)
    ecuacion = del_repeated(ecuacion)
    return ecuacion


def list_var(ecuacion):
    '''
    Retorna la lista de variables de la ecuación
    '''
    #ecuacion = ['x0+vo*t+a*t**2/2-x']
    if verify_parenthesis(ecuacion):
        variables = get_list_variables(ecuacion)
    else:
        variables = ['Por favor, verifique los paréntesis']
    return variables

def verify_parenthesis(cad_simbolos):
    '''
    verifica los parentesis de la ecuación
    '''
    pila = Heap()
    balanceados = True
    index = 0
    cad = "".join(cad_simbolos[0])
    while index < len(cad) and balanceados:
        simbolo = cad[index]
        if simbolo == "(":
            pila.include(simbolo)
        elif simbolo == ')':
            if pila.empty():
                balanceados = False
            else:
                pila.extract()

        index += 1

    return balanceados and pila.empty()
