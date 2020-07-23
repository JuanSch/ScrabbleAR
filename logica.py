import platform
import operator
import random
import json
import PySimpleGUI as sg
from functools import reduce
from itertools import chain
from bisect import insort

def top10(dificultad = None):
    with open('valores_puntajes.json','r', encoding='UTF-8') as f:
        dic = json.load(f)
        if dificultad == None:
            top = dic['top10']
        else: 
            top = dic['top10'][dificultad]
    if dificultad == None:
        texto_facil = ""
        texto_medio = ""
        texto_dificil = ""
        i = 1
        for elemento in top['Facil']: #Forma el string por la dificultad
            if elemento[0] != "None":
                texto_facil += str(i)+'° puesto: ' + elemento[0] + ' con ' + str(elemento[1]) + 'punto/s' + '\n'
                i += 1

        i = 1
        for elemento in top['Medio']: #Forma el string por la dificultad
            if elemento[0] != "None":
                texto_medio += str(i)+'° puesto: ' + elemento[0] + ' con ' + str(elemento[1]) + 'punto/s' + '\n'
                i += 1

        i = 1
        for elemento in top['Dificil']: #Forma el string por la dificultad
            if elemento[0] != "None":
                texto_dificil += str(i)+'° puesto: ' + elemento[0] + ' con ' + str(elemento[1]) + 'punto/s' + '\n'
                i += 1

        layout = [[sg.Text('TOP 10')],
            [sg.Output(size=(35,10), key='-OUTPUT-')],
            [sg.Button('Facil'),sg.Button('Medio'),sg.Button('Dificil')],
            [sg.Button('Volver')]]
        window = sg.Window('', layout)

        while True:
            event, _ = window.read()
            if event in [None, 'Volver']:
                break
            if event in 'Facil':
                window['-OUTPUT-'].update(texto_facil)
            if event in 'Medio':
                window['-OUTPUT-'].update(texto_medio)
            if event in 'Dificil':
                window['-OUTPUT-'].update(texto_dificil)                
        window.close()

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
        self.letra = letra
        self.valor = valor
        self.select = False

    def getimagen(self):
        if self.select:
            return f'imagenes{ruta()}{self.letra.upper()}click.png'
        else:
            return f'imagenes{ruta()}{self.letra.upper()}.png'

    def cambiarselect(self):
        self.select = not self.select

    def getvalor(self):
        return self.valor

#####################################################################
#                          FIN CLASE FICHA                          #
#####################################################################


#####################################################################
#                        INICIO CLASE CASILLA                       #
#####################################################################

class Casilla:
    """Clase correspondiente a una casilla de tablero, puede contener
    o no a una ficha de juego, devolver el valor y la imagen que contiene
    (en función de la existencia o no de una ficha y el modificador
    de la casilla)."""

    valores={'': lambda x: x,
             '2L': lambda x: x*2,
             '3L': lambda x: x*3,
             '-3': lambda x: x-3,
             '3P': 3,
             '2P': 2
             }

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

    def ocupar(self, ficha):
        """Una casilla no se da por ocupada hasta que no se concreta
        la jugada"""
        self.ocupado = True
        self.ficha = ficha
        self.ficha.cambiarselect()

    def valor(self):
        """Esta función devuelve el valor que contiene la casilla
        y el modificador de palabra (si no multiplica por 2 o 3,
        siempre multiplica por 1)"""
        try:
            valor = Casilla.valores[self.tipo](self.ficha.getvalor())
            return (valor, 1)
        except:
            valor = self.ficha.getvalor()
            return (valor, Casilla.valores[self.tipo])


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
        """Busca si el valor de atril que recibe está entre los que conforman
        la palabra en curso. Si lo está devuelve la posición de la ficha
        en el tablero, en caso contrario devuelve None"""
        pos = None
        for k, v in self.fichas.items():
            if v[1] == atril:
                pos = k
        return pos

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

    def vaciar(self):
        self.min=None
        self.max=None
        self.eje=None
        self.fichas={}

    def probar(self):
        ok = False
        cant = len(self.fichas)
        if cant > 1 and self.max[self.eje] + 1 - self.min[self.eje] == cant:
            ok = True
        return ok

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

    def __init__(self, columnas, filas, casillas):
        self.xy = (columnas, filas)
        matriz = []
        for x in range(columnas):
            linea = []
            for y in range(filas):
                pos = [x, y]
                ok = False
                for key in list(Casilla.valores.keys())[1:]:
                    if pos in casillas[key]:
                        casilla = Casilla(tuple(pos), key)
                        ok = True
                        break
                if not ok:
                    casilla = Casilla(tuple(pos))
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

    def getvalidos(self):
        validos = []
        for linea in self.matriz:
            for casilla in linea:
                if not casilla.ocupado:
                    validos.append(casilla)
        return validos

    def jugada(self, palabra, pos, turno, origen=None, ficha=None):
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
            if turno == 0:
                self.posibles = self.inicio
            else:
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
        # Con esto garantizamos que no se marquen como posibles
        # casillas en las que hay una ficha
        # de la palabra en construcción
        for k, _v in palabra.fichas.items():
            if k in marcar:
                marcar.remove(k)
        return marcar, borrar, devolver

    def valor_palabra(self, palabra):
        puntos_base = 0
        multiplicador = 1
        for key in palabra.keys():
            casilla = self.getcasilla(key)
            puntos_base += casilla.valor()[0]
            multiplicador *= casilla.valor()[1]
        return puntos_base*multiplicador

    def fijar_palabra(self, palabra):

        def calcular(tupla1, tupla2):
            valor = tupla1[0] + tupla2[0]
            multi = tupla1[1] * tupla2[1]
            return (valor, multi)

        valores = []
        for k, v in palabra.fichas.items():
            ficha = v[0]
            casilla = self.getcasilla(k)
            casilla.ocupar(ficha)
            valores.append(casilla.valor())
        valor = reduce(lambda x, y: x*y, reduce(calcular, valores))
        self.posibles = self.getvalidos()
        return valor

#####################################################################
#                         FIN CLASE TABLERO                         #
#####################################################################


#####################################################################
#                         INICIO CLASE ATRIL                        #
#####################################################################

class Atril:
    estados = {0:'APAGADO', 1:'ELEGIR', 2:'PASAR', 3:'CAMBIAR'}

    def __init__(self, inicio='F'):
        fichas = {}
        vacias = []
        for i in range(7):
            nombre = f'{inicio}{i}'
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

    def imagen(self, espacio):
        if self.fichas[espacio] is None:
            return f'imagenes{ruta()}Atril.png'
        else:
            return self.fichas[espacio].getimagen()

    def click(self, evento):
        ficha = self.fichas[evento]
        if self.estado == 'CAMBIAR':
            # Se seleccionarán tantas fichas como se desee intercambiar
            # con la bolsa
            if not ficha.select:
                self.cambiar.append(ficha)
            else:
                self.cambiar.pop(ficha)
            ficha.cambiarselect()
        elif self.estado == 'ELEGIR':
            # Se seleccionará una ficha para colocar en el tablero
            # o se deselccionará una ya colocada
            if not ficha.select:
                # Si la ficha no estaba seleccionada, siginifica que se eligió
                # una para colocar en el tablero, se cambia el estado
                # del atril a 'PASAR'
                self.setestado(2)
            ficha.cambiarselect()
            self.cambiar = (evento, ficha)
        elif self.estado == 'PASAR':
            # Se deseleccionará la ficha en curso, o se seleccionará otra
            # en este estado no se pueden sacar fichas del tablero
            if evento == self.cambiar[0]:
                # Se hizo click en la ficha que ya estaba seleccionada
                # para colocar en el tablero
                self.cambiar = None
                ficha.cambiarselect()
                self.setestado(1)
            elif not ficha.select: #$%Cuando haces click en una ficha usada se rompe
                # Se decidió cambiar qué ficha se iba a colocar en el tablero
                self.cambiar[1].cambiarselect()
                self.cambiar = (evento, ficha)
                ficha.cambiarselect()


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
                self.fichas[k] = None
                self.vacias.append(k)
        return entregar

    def eliminar(self, palabra):
        for _k, v in palabra.fichas.items():
            self.fichas[v[1]] = None

class AtrilIA(Atril):
    def __init__(self):
        Atril.__init__(self, inicio='IA')

    def imagen(self, espacio):
        if self.fichas[espacio] is None:
            return f'imagenes{ruta()}Atril.png'
        else:
            return f'imagenes{ruta()}FichaIA.png'

#####################################################################
#                           FIN CLASE ATRIL                         #
#####################################################################


#####################################################################
#                         INICIO CLASE BOLSA                        #
#####################################################################
class Bolsa:
    """
    Clase de control de bolsa de fichas, contiene una lista de letras
    con tantas letras como fichas por letra haya disponibles
    y otra con un diccionario letra: valor.
    El formato de salida de las fichas es [(letra, valor)*letras a entregar]
    """

    def __init__(self, letras, valores):
        fichas = list(map(lambda x: [x[0]]*x[1], letras))
        self.fichas = list(chain.from_iterable(fichas))
        self.valores = valores

    def entregar_fichas(self, cant):
        """
        Recibe una cantidad (int) de fichas a entregar.
        Genera [(letra, valor)*cantidad] seleccionando letras al azar
        de la bolsa y eliminándolas.
        Si hay menos letras en la bolsa que cant, devolverá una lista
        vacía.
        """

        entregar = []
        if len(self.fichas) >= cant:
            for _i in range(cant):
                pos = random.randrange(len(self.fichas))
                letra = self.fichas[pos]
                self.fichas.pop(pos)
                valor = self.valores[letra]
                ficha = (letra, valor)
                entregar.append(ficha)
        return entregar

    def intercambiar_fichas(self, fichas):
        """
        Recibe una lista de fichas [(letra, valor)*cant].
        Reincorpora las letras a la bolsa, y entrega nuevamente
        tantas como haya recibido.
        Para la reincorporación se emplea bisect.insort()
        (inserción ordenada) para evitar la posible acumulación
        de letras indseadas al final de la lista que surgirían
        de un lista.append()
        """

        lista = list(map(lambda x: x[0], fichas))
        for letra in lista:
            insort(self.fichas, letra)
        return self.entregar_fichas(len(lista))


#####################################################################
#                           FIN CLASE BOLSA                         #
#####################################################################