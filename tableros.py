import PySimpleGUI as sg
import string
import random


class Tablero:
    def __init__(self, columnas, filas):
        self.matriz = [[sg.Button(key=f'({x}, {y})', pad=(0,0),
                                  image_filename=tablero[f'({x}, {y})']['img'],
                                  image_size=(60,60), border_width=0,
                                  button_color=('#DDDDDD', '#DDDDDD'))
                        for x in range(columnas)] for y in range(filas)]

    def getmatriz(self):
        return self.matriz


def armar_tablero(columnas, filas):
    botones = {}
    for x in range(columnas):
        for y in range(filas):
            botones[f'({x}, {y})'] = {'img': 'imagenes/casilla.png',
                                      'click': False, 'val': 1}
    return botones


def armar_fichas(letras):
    fichas = []
    for y in range(7):
        letra = letras[random.randrange(len(letras))]
        imagen = f'imagenes/{letra}.png'
        ficha = {'letra': letra, 'img': imagen, 'click': False}
        fichas.append(ficha)
    return fichas


letras = [char for char in string.ascii_uppercase]


filas = columnas = 15

tablero = armar_tablero(columnas, filas)

mesa = Tablero(columnas, filas)

fichas = armar_fichas(letras)

#interfaz
layout = mesa.getmatriz()

layout.append([sg.T('')])

layout.append([sg.Button(key=f'F{y}', pad=(0, 0),
                         image_filename=fichas[y]['img'],
                         image_size=(60,60), border_width=0,
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
        if ficha['click'] == True:
            window.FindElement(event).Update(button_color=('#DDDDDD', '#DDDDDD'))
            pasar.pop(-1)
        else:
            pasar.append((ficha, pos))
            window.FindElement(event).Update(button_color=('#0000FF', '#0000FF'))
        ficha['click']=not ficha['click']

    elif '(' in event:
        if pasar is None:
            pass
        elif tablero[event]['click'] == False:
            window.FindElement(event).Update(image_filename = pasar[-1][0]['img'])
            tablero[event]['click'] = not tablero[event]['click']
            window.FindElement(f'F{pasar[-1][1]}').Update(visible=False)



#cierre
window.Close()