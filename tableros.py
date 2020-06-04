import PySimpleGUI as sg
from logica import Ficha, Casilla, Palabra, Tablero, Atril
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

def deseleccionar_ficha(window, tablero, fichas, marcar, borrar, devolver, pos):
    """se encarga de las actualizaciones a la GUI en el caso
    de suceder una deselección de ficha"""

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


def jugar():

    def deseleccionar_ficha(marcar, borrar, devolver, pos):
        """se encarga de las actualizaciones a la GUI en el caso
        de suceder una deselección de ficha"""

        nonlocal window
        nonlocal tablero
        nonlocal fichas
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


    letras = [char for char in string.ascii_uppercase]
    #Temporalmente se generó una lista de letras a-z(salvo ñ) para operar
    #sobre ellas

    filas = columnas = 15

    dim_boton = (40,40)

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
                    #si no hay fichas selecionadas
                    #el evento es una selección
                    pasar=(event, ficha)
                    pasando=True
                    ficha.cambiarselect()
                    window.FindElement(event).Update(image_filename=
                                                     ficha.getimagen())
                else:
                    #si la ficha ya está seleccionada,
                    #se toma como una deselección
                    pos=None
                    for k,v in palabra.fichas.items():
                        if v[1] == event:
                            pos=k
                            break
                    #se simula un click en el tablero en donde está
                    #colocada la ficha
                    marcar, borrar, devolver=tablero.jugada(palabra, pos)
                    #se actualiza la GUI
                    deseleccionar_ficha(marcar, borrar, devolver, pos)
                    

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

        elif type(event) == tuple:
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
                deseleccionar_ficha(marcar, borrar, devolver, event)


    #cierre
    window.Close()


if __name__ == '__main__':
    jugar()