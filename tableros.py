import PySimpleGUI as sg
import string
import random
import platform
import operator


def ruta():
    """Retorna el caracter que el sistema operativo en el que se está
    ejecutando el programa emplea como separador de jerarquía en
    las rutas de archivos"""

    if platform.system() != "Windows":
        char = '/'
    else:
        char = '\\'
    return char


class Ficha:
    """El parámetro valor está definido por la dificultad seleccionada.
    La clase incluye la ruta a las imágenes correspondientes a la letra,
    tanto para el caso de estar seleccionada como no, un indicador
    de selección (si/no), y los métodos necesarios para acceder
    o modificar estos argumentos"""

    def __init__(self, letra, valor):
        self.letra = letra
        self.valor = valor
        self.img = f'imagenes{ruta()}{letra.upper()}.png'
        self.img_click = f'imagenes{ruta()}{letra.upper()}click.png'
        self.select = False

    def getimagen(self):
        if self.select:
            return self.img_click
        else:
            return self.img

    def cambiarselect(self):
        self.select = not self.select

    def getvalor(self):
        return self.valor


class Casilla:
    """Clase correspondiente a una casilla de tablero, puede contener
    o no a una ficha de juego, devolver el valor que contiene
    (en función de la existencia o no de una ficha y el modificador
    de la casilla). Tiene una imagen asociada independiente de la existencia
    o no de una ficha"""

    valores = {'2L': lambda x: x*2,
               '3L': lambda x: x*3,
               '-3': lambda x: x-3,
               '3P': 3,
               '2P': 2}

    def __init__(self, pos, tipo=''):
        self.pos = pos
        self.tipo = tipo
        self.img = f'imagenes{ruta()}casilla{tipo}.png'
        self.ocupado = False
        self.ficha = None

    def getpos(self):
        return self.pos

    def getestado(self):
        return self.ocupado

    def getimagen(self):
        try:
            return self.ficha.getimagen()
        except:
            return self.img

    def marcar (self, ficha):
        """Una casilla sólo Sólo debería recibir fichas 'en proceso'
        mientras el jugador o la IA definen la palabra"""
        self.ficha = ficha

    def ocupar(self):
        """Una casilla no se da por ocupada hasta que no se concreta
        la jugada"""
        self.ocupado = True
        self.ficha.cambiarselect()

    def valor(self):
        """Esta función devuelve el valor que contiene la casilla
        y el modificador de palabra (si no multiplica por 2 o 3,
        siempre multiplica por 1"""
        try:
            valor = Casilla.valores[self.tipo](self.ficha.getvalor())
            puntos = (valor, 1)
        except:
            valor = self.ficha.getvalor()
            puntos = (valor, Casilla.valores[self.tipo])
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

    def agregarletra(self, pos, origen, ficha):
        """Sólo permite agregar letras en posiciones nuevas"""

        self.fichas[pos] = (ficha, origen)
        longitud=len(self.fichas)
        if longitud == 1:
            self.min = self.max = pos
        else:
            posiciones=self.getposiciones()
            #con sólo 2 posiciones ya se puede definir el eje, y no es
            #necesario reevaluarlo por cad nuevo elemento
            if longitud == 2:
                x = pos[0]
                #Si el valor de x en el elemento preexistente es igual
                #al del elemento insertado, significa que los desplazamientos
                #suceden a lo largo del eje y, el valor en la posición [1]
                #de la tupla de coordenadas, en caso contrario
                #puede asegurarse lo opuesto
                if posiciones[0][0] == x:
                    self.eje=1
                else:
                    self.eje=0
            #para facilitar operaciones, el diccionario siempre se ordena
            self.fichas=dict(sorted(self.fichas.items(),
                             key=lambda kv: kv[0][self.eje]))
            evaluar = pos[self.eje]
            #se debe evaluar si hubo un cambio en la posición de min o max,
            #las precondiciones evitan que puedan suceder ambos a la vez
            if evaluar < self.min[self.eje]:
                self.min = pos
            elif evaluar > self.max[self.eje]:
                self.max = pos

    def cambiarletra(self, pos, origen, ficha):
        """Permite hacer tanto hacer un intercambio de fichas como simplemente
        cambiar una ficha por un espacio vacío, siempre devuelve la casilla
        de origen de esa ficha"""

        devolver = self.fichas[pos][1]
        if ficha == None: #en este caso se elimina el elemento
            del self.fichas[pos]
            #debe evaluarse si la palabra quedó vacía
            if len(self.fichas) == 0:
                self.min=None
                self.max=None
                self.eje=None
            #en caso contrario debe revisarse si se eliminó alguno
            #de los extremos, en cuyo caso debe recalcularse
            else:
                claves = list(self.fichas.keys())
                if pos == self.max:
                    self.max = claves[-1]
                    print(self.max)
                if pos == self.min:
                    self.max = claves[0]
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

    def getpalabra(self):
        palabra = ''
        for k, v in self.fichas.items():
            palabra+=v[0].letra
        palabra.lower()
        return palabra


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
                pos = tuple([x,y])
                if x == y or x+y==filas-1:
                    casilla = Casilla(pos, '2L')
                else:
                    casilla = Casilla(pos)
                linea.append(casilla)
            matriz.append(linea)
        self.matriz = matriz
        self.posibles = []

    def getmatriz(self):
        return self.matriz

    def getxy(self):
        return self.xy

    def getcasilla(self, pos):
        x=pos[0]
        y=pos[1]
        casilla=self.matriz[y][x]
        return casilla

    def setcasilla(self, pos, ficha):
        x = pos[0]
        y = pos[1]
        casilla = self.matriz[y][x]
        casilla.ocupar(ficha)

    def getvalidos(self):
        validos=[]
        for linea in self.matriz:
            for casilla in linea:
                if not casilla.ocupado:
                    validos.append(casilla)
        return validos

    def jugada(self, palabra, pos, origen=None, ficha=None):
        """Método principal de lógica interna del tablero, debe recibir
        un objeto tipo palabra, y manejará las actualizaciones
        correspondientes a los estados de las casillas"""

        def limite(pos, eje, dir):
            mov = {'+': operator.add, '-': operator.sub}
            max = self.getxy()[eje]
            lim = 0
            ok = True
            i = 0
            while ok and i < 6:
                nueva_coord = mov[dir](pos[eje], 1)
                pos[eje] = nueva_coord
                if pos[eje] < 0 or pos[eje] == max:
                    ok = False
                if ok:
                    nueva_pos = tuple(pos)
                    if self.getcasilla(nueva_pos).ocupado == False:
                        lim = nueva_pos
                        i += 1
                    else:
                        ok = False
            return lim

        if self.getcasilla(pos).ocupado:
            return None
        else:
            devolver = palabra.modificar(pos, origen, ficha)
            if devolver != None:
                borrar=None
                marcar=list(self.posibles)
                if palabra.min == None:
                    borrar=list(self.posibles)
                    self.posibles=[]
                else:
                    marcar=pos
                return marcar, borrar, devolver
            else:
                anteriores = list(self.posibles)
                self.posibles = []
                if palabra.eje == None:
                    x = palabra.min[0]
                    y = palabra.min[1]
                    min_x = limite([x, y], 0, '-')
                    max_x = limite([x, y], 0, '+')
                    min_y = limite([x, y], 1, '-')
                    max_y = limite([x, y], 1, '+')
                    for i in range(min_x[0], max_x[0]+1):
                        if i != x:
                            casilla = (i, y)
                            self.posibles.append(casilla)
                    for i in range(min_y[1], max_y[1]+1):
                        if i != y:
                            casilla = (x, i)
                            self.posibles.append(casilla)
                else:
                    min=palabra.min
                    max=palabra.max
                    max_eje = limite(list(min), palabra.eje, '+')
                    min_eje = limite(list(max), palabra.eje, '-')
                    for i in range(min_eje[palabra.eje],max_eje[palabra.eje]+1):
                        casilla = list(min_eje)
                        casilla[palabra.eje] = i
                        casilla = tuple(casilla)
                        if casilla not in palabra.getposiciones():
                            self.posibles.append(casilla)
                
                marcar=list(self.posibles)
                borrar=list(set(anteriores) - set(self.posibles))
                return list(self.posibles), borrar, None

#####################################################################
#                         FIN CLASE TABLERO                         #
#####################################################################


def armar_botones(tablero, dim_boton):
    """Genera una matriz de botones con base en la matriz lógica del tablero,
    es esencialmente el layout del tablero en términos de GUI"""

    base = tablero.getmatriz()
    botones = []
    for fila in base:
        linea = []
        for casilla in fila:
            boton = sg.Button(key=casilla.getpos(), image_size=dim_boton,
                              image_filename=casilla.getimagen(), pad=(0, 0),
                              button_color=('#DDDDDD', '#DDDDDD'),
                              border_width=0)
            linea.append(boton)
        botones.append(linea)
    return botones


def armar_fichas(letras):
    """Genera la lista de fichas disponibles para el jugador, es sólo
    la lógica subyacente a la GUI. Esta es la sección menos desarrollada
    por el momento, debería estar vinculada a la 'bolsa de fichas'
    y directamente recibir una lista de fichas"""

    fichas = []
    for y in range(7):
        letra = letras[random.randrange(len(letras))]
        valor = 1
        ficha = Ficha(letra, valor)
        fichas.append(ficha)
    return fichas


def jugar():
    letras = [char for char in string.ascii_uppercase]
    #Temporalmente se generó una lista de letras a-z(salvo ñ) para operar
    #sobre ellas

    filas = columnas = 15

    dim_boton = (50,50)

    tablero = Tablero(columnas, filas)

    fichas = armar_fichas(letras)

    #interfaz
    layout = armar_botones(tablero, dim_boton)

    layout.append([sg.T('')])

    layout.append([sg.Button(key=f'F{y}', pad=(0, 0),
                            image_filename=fichas[y].getimagen(),
                            image_size=dim_boton, border_width=0,
                            button_color=('#DDDDDD', '#DDDDDD'))
            for y in range(len(fichas))])

    #inicializacion
    window = sg.Window('Ventana de juego').Layout(layout)

    pasar=()
    pasando = False
    #variables de uso temporal para probar la lógica del programa

    palabra=Palabra()

    #bucle
    while True:
        event, values = window.Read()

        if event is None:
            break

        elif 'F' in event:  #sé que se está seleccionando una ficha
            if not pasando:
                #si no estoy en proceso de pasar sé que estoy intentando
                #seleccionar o deseleccionar una ficha
                pos=int(event[1])
                ficha=fichas[pos]
                if ficha.select == False:
                    pasar=(event, ficha)
                    pasando=True
                    ficha.cambiarselect()
                    window.FindElement(event).Update(image_filename=
                                                     ficha.getimagen())
                else:
                    pos=None
                    for k,v in palabra.fichas.items():
                        if v[1] == event:
                            pos=k
                            break
                    marcar, borrar, devolver=tablero.jugada(palabra, pos)
                    imagen=tablero.getcasilla(pos).getimagen()
                    window.FindElement(pos).Update(image_filename=imagen)
                    pos=int(devolver[1])
                    ficha=fichas[pos]
                    ficha.cambiarselect()
                    window.FindElement(devolver).Update(image_filename=
                                                        ficha.getimagen())
                    try:
                        for casilla in borrar:
                            window.FindElement(casilla).Update(
                                button_color=('#DDDDDD', '#DDDDDD'))
                    except:
                        pass
                    try:
                        window.FindElement(marcar).Update(
                            button_color=('#0000FF', '#0000FF'))
                    except:
                        pass

            else:
                b_previo, f_previa = pasar[0], pasar[1]
                f_previa.cambiarselect()
                window.FindElement(b_previo).Update(image_filename=
                                                    f_previa.getimagen())
                if event == b_previo:
                    pasar = ()
                    pasando=False
                else:
                    pos=int(event[1])
                    ficha=fichas[pos]
                    origen=event
                    pasar=(origen, ficha)
                    pasando=True
                    ficha.cambiarselect()
                    window.FindElement(event).Update(image_filename=
                                                     ficha.getimagen())

        else:
            if pasando == True:
                posibles, borrar, devolver = tablero.jugada(
                    palabra, event, pasar[0], pasar[1])
                if devolver != None:
                    pos=int(devolver[1])
                    ficha=fichas[pos]
                    ficha.cambiarselect()
                    window.FindElement(devolver).Update(image_filename=
                                                        ficha.getimagen())
                else:
                    for casilla in posibles:
                        window.FindElement(casilla).Update(
                            button_color=('#0000FF','#0000FF'))
                    for casilla in borrar:
                        window.FindElement(casilla).Update(
                            button_color=('#DDDDDD', '#DDDDDD'))

                for k, v in palabra.fichas.items():
                    posicion = k
                    imagen = v[0].getimagen()
                    window.FindElement(posicion).Update(
                        image_filename=imagen)
                    pasando=False

            elif event in palabra.getposiciones():
                marcar, borrar, devolver=tablero.jugada(palabra, event)
                imagen=tablero.getcasilla(event).getimagen()
                window.FindElement(event).Update(image_filename=imagen)
                pos=int(devolver[1])
                ficha=fichas[pos]
                ficha.cambiarselect()
                window.FindElement(devolver).Update(image_filename=
                                                    ficha.getimagen())
                try:
                    for casilla in borrar:
                        window.FindElement(casilla).Update(
                            button_color=('#DDDDDD', '#DDDDDD'))
                except:
                    pass
                try:
                    window.FindElement(marcar).Update(
                        button_color=('#0000FF', '#0000FF'))
                except:
                    pass


    #cierre
    window.Close()


if __name__ == '__main__':
    jugar()