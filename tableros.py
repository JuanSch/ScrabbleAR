import PySimpleGUI as sg
import string
import random
import platform


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
     de la casilla. Tiene una imagen asociada independiente de la existencia
     o no de una ficha"""

    valores = {'2L': lambda x: x*2,
               '3L': lambda x: x*3,
               '-3': -3,
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

    def getimagen(self):
        if self.ocupado:
            return self.ficha.getimagen()
        else:
            return self.img

    def ocupar(self, ficha):
        self.ocupado = True
        self.ficha = ficha

    def valor(self):
        try:
            valor = self.ficha.getvalor() * Casilla.valores[self.tipo]
            puntos = (valor, 1)
        except:
            valor = self.ficha.getvalor()
            puntos = (valor, Casilla.valores[self.tipo])
        return puntos


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

#bucle

en_proceso = []
pasar = False
#variables de uso temporal para probar la lógica del programa

while True:
    event, values = window.Read()

    if event is None:
        break

    elif 'F' in event:  #sé que se está seleccionando una ficha
        pos = int(event[1])
        ficha = fichas[pos]
        if ficha.select == False:
            en_proceso.append(ficha)
            pasar = True
            ficha.cambiarselect()
            window.FindElement(event).Update(image_filename=ficha.getimagen())

    else:
        if pasar == True:
            casilla = tablero.getcasilla(event)
            if casilla.ocupado:
                sg.Popup('No puede cambiar fichas de lugar')
            else:
                tablero.setcasilla(event, en_proceso[-1])
                imagen = tablero.getcasilla(event).getimagen()
                window.FindElement(event).Update(image_filename=imagen)
                pasar = False


#cierre
window.Close()