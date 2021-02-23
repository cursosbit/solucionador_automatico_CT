''' Clase para definir ls variable mediante sus atributos'''
class Unidad():
    '''Clase para definir las unidades mediante sus atributos'''
    def __init__(self, simbolo, nombre, lstunidades):
        '''simbolo, símbolo asigndo a la unidad
        nombre, identificador de la unidad
        lstunidades, unidades posibles
        '''
        self.simbolo = simbolo
        self.nombre = nombre
        self.lstunidades = lstunidades
    
    def print_unid(self):
        ''' Imprime la variable '''
        print(self.simbolo + ', ' + str(self.nombre) + ', ' + self.lstunidades)
        
class Variable():
    '''Clase para definir las variable mediante sus atributos'''
    def __init__(self, simbolo, nombre, valor, unidad):
        '''simbolo, símbolo asigndo a la variable
        nombre, identificador de la variable
        valor, valor asignado a la variable
        unidad, unidad de medida de la variable
        '''
        self.simbolo = simbolo
        self.nombre = nombre
        self.valor = valor
        self.unidad = unidad

    def print_var(self):
        ''' Imprime la variable '''
        print(self.simbolo + ' = ' + str(self.valor) + ' [' + self.unidad + ']')

class Enunciado():
    '''Clase para definir las variable mediante sus atributos'''
    def __init__(self, enunciado, modelo, lstvarindep, lstvardep, ref, pag, nro):
        '''simbolo, símbolo asigndo a la variable
        nombre, identificador de la variable
        valor, valor asignado a la variable
        unidad, unidad de medida de la variable
        '''
        self.enunciado = enunciado
        self.modelo = modelo
        self.lstvarindep = lstvarindep
        self.lstvardep = lstvardep
        self.ref = ref
        self.pag = pag
        self.nro = nro
        
    def print_enunc(self):
        ''' Imprime la variable '''
        print(self.enunciado + ', ' + str(self.modelo) + ', ' +
              self.lstvarindep + ', ' + ', ' + self.lstvardep + ', ' +
              str(self.ref) + ', ' + str(self.pag) + ', ' + str(self.nro))

if __name__ == '__main__':
    simb = 'vi'
    nomb = 'Velocidad Inicial'
    val = 20
    unid = 'm/s'
    vi = Variable(simb, nomb, val, unid)
    vi.print_var()
    
    simb = 'd'
    nomb = 'distancia'
    unid = '[m, pie, pulg, km, milla, yarda]'
    
    un = Unidad(simb, nomb, unid)
    un.print_unid()

    enunciado = 'Un automóvil mantiene una aceleración constante de 8 m/s2. Si su velocidad inicial era de 20 m/s al norte,  cuál será  su velocidad después de 6 s?'
    modelo = 'distancia'
    varindep = '[m, pie, pulg, km, milla, yarda]'
    vardep = '[m, pie, pulg, km, milla, yarda]'
    ref = 1
    pag = 1
    nro = 1
    
    enunc = Enunciado(enunciado, modelo, varindep, vardep, ref, pag, nro)
    enunc.print_enunc()
    
    