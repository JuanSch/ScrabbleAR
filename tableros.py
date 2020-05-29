import PySimpleGUI as sg
import string
import random
import platform


class Ficha:
    def __init__(self, letra, valor):
        self.letra = letra
        self.valor = valor
        if platform.system() != "Windows":
            self.img = f'imagenes/{letra.upper()}.png'
            self.img_click = f'imagenes/{letra.upper()}click.png'
        else:
            self.img = f'imagenes\\{letra.upper()}.png'
            self.img_click = f'imagenes\\{letra.upper()}click.png'
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
    valores = {'2L': lambda x: x*2,
               '3L': lambda x: x*3,
               '-3': -3,
               '3P': 3,
               '2P': 2}

    def __init__(self, pos, tipo=''):
        self.pos = pos
        self.tipo = tipo
        if platform.system() != "Windows":
            self.img = f'imagenes/casilla{tipo}'
        else: 
            self.img = f'imagenes\\casilla{tipo}'
        self.estado = False
        self.ficha = None

    def getimagen(self):
        if self.estado:
            return self.ficha.getimagen()
        else:
            return self.img

    def setficha(self, ficha):
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
    def __init__(self, columnas, filas):
        self.matriz = [[sg.Button(key=f'({x}, {y})', pad=(0,0),
                                  image_filename=tablero[f'({x}, {y})']['img'],
                                  image_size=(50,50), border_width=0,
                                  button_color=('#DDDDDD', '#DDDDDD'))
                        for x in range(columnas)] for y in range(filas)]

    def getmatriz(self):
        return self.matriz


def armar_tablero(columnas, filas):
    botones = {}
    for x in range(columnas):
        for y in range(filas):
            if platform.system() != "Windows":
                botones[f'({x}, {y})'] = {'img': 'imagenes/casilla.png',
                                          'click': False, 'val': 1}
            else:
                botones[f'({x}, {y})'] = {'img': 'imagenes\\casilla.png',
                                          'click': False, 'val': 1}
    return botones


def armar_fichas(letras):
    fichas = []
    for y in range(7):
        letra = letras[random.randrange(len(letras))]
        valor = 1
        ficha = Ficha(letra, valor)
        fichas.append(ficha)
    return fichas


letras = [char for char in string.ascii_uppercase]


filas = columnas = 15

dim_boton = (50,50)

tablero = armar_tablero(columnas, filas)

mesa = Tablero(columnas, filas)

fichas = armar_fichas(letras)

for y in range(len(fichas)):
    print(fichas[y].getimagen())


#interfaz
layout = mesa.getmatriz()

layout.append([sg.T('')])

layout.append([sg.Button(key=f'F{y}', pad=(0, 0),
                         image_filename=fichas[y].getimagen(),
                         image_size=dim_boton, border_width=0,
                         button_color=('#DDDDDD', '#DDDDDD'))
           for y in range(len(fichas))])

#inicializacion
window = sg.Window('Ventana de juego').Layout(layout)

#bucle

pasar = []

while True:
    event, values = window.Read()

    if event is None:
        break

    elif 'F' in event:
        pos = int(event[1])
        ficha = fichas[pos]
        if ficha.select == False:
            pasar.append((ficha, pos))
        ficha.cambiarselect()
        window.FindElement(event).Update(image_filename=ficha.getimagen())

    elif '(' in event:
        if pasar == []:
            pass
        elif tablero[event]['click'] == False:
            window.FindElement(event).Update(image_filename
                                             = pasar[-1][0].getimagen())
            tablero[event]['click'] = not tablero[event]['click']
            window.FindElement(f'F{pasar[-1][1]}').Update(visible=False)



#cierre
window.Close()