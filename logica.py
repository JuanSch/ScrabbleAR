import platform
import operator


def ruta():
    """Retorna el caracter que el sistema operativo en el que se está
    ejecutando el programa emplea como separador de jerarquía en
    las rutas de archivos"""

    if platform.system()!="Windows":
        char='/'
    else:
        char='\\'
    return char


#####################################################################
#                         INICIO CLASE FICHA                        #
#####################################################################

class Ficha:
    """El parámetro valor está definido por la dificultad seleccionada.
    La clase incluye un indicador de selección (si/no),
    y los métodos necesarios para acceder a o modificar estos argumentos,
    así como devolver presentar la ruta de imagen que corresponda"""

    def __init__(self, letra, valor):
        self.letra=letra
        self.valor=valor
        self.select=False

    def getimagen(self):
        if self.select:
            return f'imagenes{ruta()}{self.letra.upper()}click.png'
        else:
            return f'imagenes{ruta()}{self.letra.upper()}.png'

    def cambiarselect(self):
        self.select=not self.select

    def getvalor(self):
        return self.valor


#####################################################################
#                       INICIO CLASE CASILLA                        #
#####################################################################

class Casilla:
    """Clase correspondiente a una casilla de tablero, puede contener
    o no a una ficha de juego, devolver el valor y la imagen que contiene
    (en función de la existencia o no de una ficha y el modificador
    de la casilla)."""

    valores={'2L': lambda x: x*2,
             '3L': lambda x: x*3,
             '-3': lambda x: x-3,
             '3P': 3,
             '2P': 2}

    def __init__(self, pos, tipo=''):
        self.pos=pos
        self.tipo=tipo
        self.ocupado=False
        self.ficha=None

    def getpos(self):
        return self.pos

    def getestado(self):
        return self.ocupado

    def getimagen(self, resalte=False):

        try:
            return self.ficha.getimagen()
        except:
            if resalte:
                return f'imagenes{ruta()}casilla{self.tipo}P.png'
            else:
                return f'imagenes{ruta()}casilla{self.tipo}.png'

    def marcar(self, ficha):
        """Una casilla sólo Sólo debería recibir fichas 'en proceso'
        mientras el jugador o la IA definen la palabra"""
        self.ficha=ficha

    def ocupar(self):
        """Una casilla no se da por ocupada hasta que no se concreta
        la jugada"""
        self.ocupado=True
        self.ficha.cambiarselect()

    def valor(self):
        """Esta función devuelve el valor que contiene la casilla
        y el modificador de palabra (si no multiplica por 2 o 3,
        siempre multiplica por 1"""
        try:
            valor=Casilla.valores[self.tipo](self.ficha.getvalor())
            puntos=(valor, 1)
        except:
            valor=self.ficha.getvalor()
            puntos=(valor, Casilla.valores[self.tipo])
        return puntos


#####################################################################
#                          FIN CLASE CASILLA                        #
#####################################################################


#####################################################################
#                         INICIO CLASE PALABRA                      #
#####################################################################

class Palabra:
    """Clase de transferencia de datos para el desarrollo del juego,
    contiene la posición de los extremos de la palabra que el jugador está
    escribiendo y las fichas que la componen con sus respectivas posiciones
    y botones de origen. Conoce su orientación y tiene la capacidad de
    retornar un string con la palabra que sus elementos forman"""

    def __init__(self):
        self.min=None
        self.max=None
        self.eje=None
        self.fichas={}

    def getposiciones(self):
        return list(self.fichas.keys())

    def posficha(self, atril):
        encontre = False
        pos = None
        for k, v in self.fichas.items():
            if v[1] == atril:
                encontre = True
                pos = k
        return encontre, pos

    def agregarletra(self, pos, origen, ficha):
        """Sólo permite agregar letras en posiciones nuevas"""

        self.fichas[pos]=(ficha, origen)
        longitud=len(self.fichas)
        if longitud==1:
            self.min=self.max=pos
        else:
            posiciones=self.getposiciones()
            # con sólo 2 posiciones ya se puede definir el eje, y no es
            # necesario reevaluarlo por cada nuevo elemento
            if longitud==2:
                x=pos[0]
                # Si el valor de x en el elemento preexistente es igual
                # al del elemento insertado, significa que los desplazamientos
                # suceden a lo largo del eje y, el valor en la posición [1]
                # de la tupla de coordenadas, en caso contrario
                # puede asegurarse lo opuesto
                if posiciones[0][0] == x:
                    self.eje = 1
                else:
                    self.eje = 0
            # para facilitar operaciones, el diccionario siempre se ordena
            self.fichas = dict(sorted(self.fichas.items(),
                                    key=lambda kv: kv[0][self.eje]))
            evaluar = pos[self.eje]
            # se debe evaluar si hubo un cambio en la posición de min o max,
            # las precondiciones evitan que puedan suceder ambos a la vez
            if evaluar < self.min[self.eje]:
                self.min = pos
            elif evaluar > self.max[self.eje]:
                self.max = pos

    def cambiarletra(self, pos, origen, ficha):
        """Permite hacer tanto hacer un intercambio de fichas como simplemente
        cambiar una ficha por un espacio vacío, siempre devuelve la casilla
        de origen de esa ficha"""

        devolver = self.fichas[pos][1]
        if ficha == None:  # en este caso se elimina el elemento
            del self.fichas[pos]
            # debe evaluarse si la palabra quedó vacía, si es así vuelve
            # los valores posicionales a None
            if len(self.fichas) == 0:
                self.min = None
                self.max = None
                self.eje = None
            # en caso contrario debe revisarse si se eliminó alguno
            # de los extremos, en cuyo caso debe recalcularse
            else:
                claves = list(self.fichas.keys())
                if pos == self.max:
                    self.max = claves[-1]
                elif pos == self.min:
                    self.min=claves[0]
                # si la palabra pasó a tener un sólo elemento,
                # el valor de eje vuelve a None
                if len(self.fichas) == 1:
                    self.eje = None
        else:
            self.fichas[pos] = (ficha, origen)
        return devolver

    def modificar(self, pos, origen=None, ficha=None):
        if pos in self.fichas:
            devolver = self.cambiarletra(pos, origen, ficha)
            return devolver
        else:
            self.agregarletra(pos, origen, ficha)
            return None

    def __str__(self):
        return ''.join(val[1][0].letra for val in self.fichas.items())


#####################################################################
#                          FIN CLASE PALABRA                        #
#####################################################################


#####################################################################
#                         INICIO CLASE TABLERO                      #
#####################################################################

class Tablero:
    """Es una matriz de casillas, y la interfaz entre la GUI y la lógica
    subyacente a los eventos que sucedan en el tablero. La distribución de
    tipos de casilla aún no está implementada, pero debería estar
    definida por el tipo de tablero"""

    def __init__(self, columnas, filas):
        self.xy = (columnas, filas)
        matriz = []
        for x in range(columnas):
            linea = []
            for y in range(filas):
                pos = tuple([x, y])
                if x == y or x+y == filas-1:
                    casilla = Casilla(pos, '2L')
                else:
                    casilla = Casilla(pos)
                linea.append(casilla)
            matriz.append(linea)
        self.matriz = matriz
        self.inicio = [(7,7)]
        self.posibles = list(self.inicio)

    def getmatriz(self):
        return self.matriz

    def getxy(self):
        return self.xy

    def getposibles(self, palabra, turno):
        if turno == 0 and palabra.min == None:
            return self.inicio
        else:
            return self.posibles


    def getcasilla(self, pos):
        x = pos[0]
        y = pos[1]
        casilla = self.matriz[y][x]
        return casilla

    def setcasilla(self, pos, ficha):
        x = pos[0]
        y = pos[1]
        casilla = self.matriz[y][x]
        casilla.marcar(ficha)

    def getvalidos(self):
        validos = []
        for linea in self.matriz:
            for casilla in linea:
                if not casilla.ocupado:
                    validos.append(casilla)
        return validos

    def jugada(self, palabra, pos, origen=None, ficha=None):
        """Método principal de lógica interna del tablero, debe recibir
        un objeto tipo palabra, y manejará las actualizaciones
        correspondientes a los estados de las casillas"""

        def limite(pos, posibles, eje, borde, dir, ciclo=0):
            if ciclo == 6:
                return posibles
            else:
                nueva = list(pos)
                coord = dir(pos[eje], 1)
                nueva[eje] = coord
                if nueva[eje] == borde or self.getcasilla(nueva).ocupado == True:
                        return posibles
                else:
                    posibles.append(tuple(nueva))
                    return limite(nueva, posibles, eje,
                                      borde, dir, ciclo+1)

        def habilitados(posibles, eje, izquierda, derecha):
            direcciones = {'+': operator.add, '-': operator.sub}
            bordes = self.getxy()
            limite(derecha, posibles, eje, -1, direcciones['-'])
            limite(izquierda, posibles, eje, bordes[eje], direcciones['+'])


        devolver = palabra.modificar(pos, origen, ficha)
        anteriores = list(self.posibles)
        if devolver is not None and palabra.min is None:
            borrar = anteriores
            self.posibles = []
        else:
            posibles = []
            eje = palabra.eje
            min = palabra.min
            if eje is None:
                habilitados(posibles, 0, min, min)
                habilitados(posibles, 1, min, min)
                posibles.append(min)
            else:
                max = palabra.max
                habilitados(posibles, eje, min, max)
            self.posibles = set(posibles)
            borrar = list(set(anteriores)-(self.posibles))
        marcar = list(self.posibles)
        #Con esto garantizamos que no se marquen como posibles
        #casillas en las que hay una ficha
        #de la palabra en construcción
        for k, v in palabra.fichas.items():
                if k in marcar:
                    marcar.remove(k)
        return marcar, borrar, devolver

#####################################################################
#                         FIN CLASE TABLERO                         #
#####################################################################


#####################################################################
#                         INICIO CLASE ATRIL                        #
#####################################################################

class Atril:
    estados = {0:'APAGADO', 1:'ELEGIR', 2:'PASAR', 3:'CAMBIAR'}

    def __init__(self):
        fichas = {}
        vacias = []
        for i in range(7):
            nombre = f'F{i}'
            fichas[nombre] = None
            vacias.append(nombre)
        self.vacias = vacias
        self.fichas = fichas
        self.cambiar = None
        self.estado = Atril.estados[0]

    def setestado(self, valor):
        self.estado = Atril.estados[valor]
        if valor == 3:
            self.cambiar = []

    def click(self, evento):
        ficha = self.fichas[evento]
        if self.estado == 'CAMBIAR':
            if not ficha.select:
                self.cambiar.append(ficha)
            else:
                self.cambiar.pop(ficha)
            ficha.cambiarselect()
        elif self.estado == 'ELEGIR':
            if not ficha.select:
                self.setestado(2)
                ficha.cambiarselect()
                self.cambiar = (evento, ficha)
            else:
                pass
        elif self.estado == 'PASAR':
            if evento == self.cambiar[0]:
                self.cambiar = None
                ficha.cambiarselect()
                self.setestado(1)
            elif not ficha.select:
                self.cambiar[1].cambiarselect()
                self.cambiar = (evento, ficha)
                ficha.cambiarselect()
            else:
                pass

    def pedirfichas(self):
        return len(self.vacias)

    def recibirfichas(self, lista):
        """Lista debe ser una lista de tuplas (letra,valor) -el formato
        de salida de la clase 'bolsa'-, las convierte en fichas
        y las almacena en los casilleros libres. La función asume
        que siempre se recibirá la cantidad requerida de fichas para
        llenar el atril. Esto implica que la condición de fin 'no hay
        fichas suficientes' debe resolverse antes de esta instancia"""

        for i in range(len(lista)):
            letra = lista[i][0]
            valor = lista[i][1]
            ficha = Ficha(letra, valor)
            self.fichas[self.vacias[i]]=ficha
        self.vacias = []

    def entregarfichas(self):
        """Devuelve una lista con las fichas que el usuario desea cambiar"""

        entregar = []
        for k,v in self.fichas.items():
            if v.select:
                entregar.append(v)
                self.vacias.append(k)
        return entregar


