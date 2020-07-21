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

def actualizar_atril(atril, window):
    """se encarga de las actualizacines a la GUI de un atril"""

    for k in atril.fichas.keys():
        window.FindElement(k).Update(image_filename=atril.imagen(k))


def actualizar_tablero(marcar, borrar, window, tablero):
    """se encarga de las actualizaciones a la GUI del tablero"""

    try:
        for casilla in borrar:
            imagen = tablero.getcasilla(casilla).getimagen()
            window.FindElement(casilla).Update(
                image_filename=imagen)
    except:
        pass
    try:
        for casilla in marcar:
            imagen=tablero.getcasilla(casilla).getimagen(True)
            window.FindElement(casilla).Update(
                image_filename=imagen)
    except:
        pass

