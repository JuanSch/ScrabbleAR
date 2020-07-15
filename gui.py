import PySimpleGUI as sg
import random

def temporizador(tiempo, inicio, corriendo):
    transcurrido = int(t.time())-inicio
    actual = tiempo - transcurrido
    if actual > 0:
        reloj = f'{divmod(actual, 60)[0]:02}:{divmod(actual, 60)[1]:02}'
    else:
        corriendo = False
        reloj = 'FIN'
    return reloj, corriendo


def armar_tablero(tablero, dim_boton):
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

def armar_atril(atril, dim_boton):
    fichas = [sg.Button(key=k, pad=(0, 0), image_filename=atril.imagen(k),
                        image_size=dim_boton, border_width=0,
                        button_color=('#DDDDDD', '#DDDDDD'))
              for k in atril.fichas.keys()]
    return fichas

def generar_bolsa(cant_letras):
    bolsa = []
    for item in cant_letras:
        for _i in range(item[1]):
            bolsa.append(item[0])
    return bolsa

def simular_bolsa(bolsa, puntos):
    """Genera la lista de fichas disponibles para el jugador, es sólo
    la lógica subyacente a la GUI. Esta es la sección menos desarrollada
    por el momento, debería estar vinculada a la 'bolsa de fichas'
    y directamente recibir una lista de fichas"""

    fichas=[]
    for _i in range(7):
        pos = random.randrange(len(bolsa))
        letra = bolsa[pos]
        bolsa.pop(pos)
        valor = puntos[letra]
        ficha=(letra, valor)
        fichas.append(ficha)
    return fichas