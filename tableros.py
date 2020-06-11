import PySimpleGUI as sg
import logica as lg
import string
import random


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

def armar_atril(atril, dim_boton):
    fichas = [sg.Button(key=k, pad=(0, 0), image_filename=v.getimagen(),
               image_size=dim_boton, border_width=0,
               button_color=('#DDDDDD', '#DDDDDD'))
            for k,v in atril.fichas.items()]
    return fichas

def simular_bolsa(letras):
    """Genera la lista de fichas disponibles para el jugador, es sólo
    la lógica subyacente a la GUI. Esta es la sección menos desarrollada
    por el momento, debería estar vinculada a la 'bolsa de fichas'
    y directamente recibir una lista de fichas"""

    fichas=[]
    for _y in range(7):
        #pylint: disable=unused-argument
        letra=letras[random.randrange(len(letras))]
        ficha=(letra, 1)
        fichas.append(ficha)
    return fichas

def actualizar_atril(window, atril):
    for k, v in atril.fichas.items():
        window.FindElement(k).Update(image_filename=v.getimagen())

def jugar():

    def deseleccionar_ficha(marcar, borrar, devolver, pos):
        """se encarga de las actualizaciones a la GUI en el caso
        de suceder una deselección de ficha"""

        nonlocal window
        nonlocal tablero
        nonlocal atriljugador
        imagen = tablero.getcasilla(pos).getimagen()
        window.FindElement(pos).Update(image_filename=imagen)
        ficha = atriljugador.fichas[devolver]
        ficha.cambiarselect()
        window.FindElement(devolver).Update(image_filename=
                                            ficha.getimagen())
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


    letras = [char for char in string.ascii_uppercase]
    #Temporalmente se generó una lista de letras a-z(salvo ñ) para operar
    #sobre ellas

    filas = columnas = 15

    dim_boton = (40,40)

    tablero = lg.Tablero(columnas, filas)

    atriljugador = lg.Atril()

    atriljugador.recibirfichas(simular_bolsa(letras))
    atriljugador.setestado(1)

    palabra=lg.Palabra()

    #interfaz
    columna1 = armar_botones(tablero, dim_boton)

    columna1.append([sg.T('')])

    linea_inferior = armar_atril(atriljugador, dim_boton)

    botones_jugador = [sg.T('      '),
                       sg.Button('JUGAR', key = '-JUGAR-', size = (12, 2)),
                       sg.T(''),
                       sg.Button('CAMBIAR', key = '-CAMBIAR-', size = (12, 2))]

    for item in botones_jugador:
        linea_inferior.append(item)

    columna1.append(linea_inferior)

    columna2 = [[sg.Button('COMENZAR', key = '-COMENZAR-', size = (12, 2))],
                [sg.T('')],
                [sg.T('TIEMPO')],
                [sg.T('20:00', font = ('Arial', '18'))]]

    layout = [[sg.Column(columna1), sg.Column(columna2, element_justification='center')]]

    #inicializacion
    window=sg.Window('Ventana de juego').Layout(layout)

    #bucle
    while True:
        event, _values = window.Read()
        #pylint: disable=unused-argument
        if event is None:
            break

        elif 'F' in event:  #el click sucede en el atril
            atriljugador.click(event)
            actualizar_atril(window, atriljugador)

        elif type(event) == tuple: #el click sucede en el tablero
            #si estado == PASAR hay una ficha seleccionada
            #para colocar en el tablero
            if atriljugador.estado == 'PASAR': 
                posibles, borrar, devolver = tablero.jugada(
                    palabra, event, atriljugador.cambiar[0],
                    atriljugador.cambiar[1])
                if (posibles, borrar, devolver) == (None, None, None):
                    pass
                else:
                    if devolver != None:
                        ficha=atriljugador.fichas[devolver]
                        ficha.cambiarselect()
                        window.FindElement(devolver).Update(
                            image_filename=ficha.getimagen())
                    else:
                        for pos in posibles:
                            imagen = tablero.getcasilla(pos).getimagen(True)
                            window.FindElement(pos).Update(
                                image_filename=imagen)
                        for pos in borrar:
                            imagen = tablero.getcasilla(pos).getimagen()
                            window.FindElement(pos).Update(
                                image_filename=imagen)
                    for k, v in palabra.fichas.items():
                        posicion = k
                        imagen = v[0].getimagen()
                        window.FindElement(posicion).Update(
                            image_filename=imagen)
                    atriljugador.setestado(1)

            elif event in palabra.getposiciones():
                marcar, borrar, devolver=tablero.jugada(palabra, event)
                deseleccionar_ficha(marcar, borrar, devolver, event)


    #cierre
    window.Close()


if __name__ == '__main__':
    jugar()