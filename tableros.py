import PySimpleGUI as sg
import time as t
import logica as lg
import string
import random
import json


def temporizador(tiempo, inicio, corriendo):
    transcurrido = int(t.time())-inicio
    actual = tiempo - transcurrido
    print(actual)
    if actual > 0:
        reloj = f'{divmod(actual, 60)[0]:02}:{divmod(actual, 60)[1]:02}'
    else:
        corriendo = False
        reloj = 'FIN'
    return reloj, corriendo


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


def jugar():

    def actualizar_atril(atril):
        """se encarga de las actualizacines a la GUI de un atril"""

        nonlocal window
        for k, v in atril.fichas.items():
            window.FindElement(k).Update(image_filename=v.getimagen())


    def actualizar_tablero(marcar, borrar):
        """se encarga de las actualizaciones a la GUI del tablero"""

        nonlocal window
        nonlocal tablero
        nonlocal atriljugador
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

    def estado_botones(estado):
        nonlocal window

        window.FindElement('-JUGAR-').Update(disabled=not estado)
        window.FindElement('-CAMBIAR-').Update(disabled=not estado)


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

    turno = 0
    eval_turno = lambda x,y: (x % 2) == y
    turno_jugador = random.randrange(0,2)

    #interfaz
    columna1 = armar_botones(tablero, dim_boton)

    columna1.append([sg.T('')])

    linea_inferior = armar_atril(atriljugador, dim_boton)

    botones_jugador = [sg.T('      '),
                       sg.Button('JUGAR', key='-JUGAR-', size=(12, 2),
                                 disabled=True),
                       sg.T(''),
                       sg.Button('CAMBIAR', key='-CAMBIAR-', size=(12, 2),
                                 disabled=True)]

    for item in botones_jugador:
        linea_inferior.append(item)

    columna1.append(linea_inferior)

    ###############
    with open('configuraciones.json','r', encoding='UTF-8') as f:
        configs =json.load(f)
        tiempo = int(configs['tiempo']) * 60 #conversion a minutos
        #tiempo = 20 * 60 #por si no  queres usar el tiempo de la config solo descomentas la linea
        reloj = f'{divmod(tiempo, 60)[0]:02}:{divmod(tiempo, 60)[1]:02}'
    ###############

    columna2 = [[sg.Button('COMENZAR', key='-INI/PAUSA-', size=(12, 2))],
                [sg.T('')],
                [sg.T('TIEMPO')],
                [sg.T(reloj, key='-RELOJ-', font=('Arial', '18'))]]

    layout = [[sg.Column(columna1), sg.Column(columna2)]]

    #inicializacion
    window = sg.Window('Ventana de juego').Layout(layout)

    #bucle
    corriendo = False
    fin = False
    inicio = 0
    while not fin:
        event, _values = window.Read(timeout= 500)
        if corriendo:
            reloj, corriendo = temporizador(tiempo, inicio, corriendo)
            window.FindElement('-RELOJ-').Update(reloj)
            if reloj == 'FIN':
                corriendo = False
                fin = True

        if (event is None):
            break
        
        if event == '-INI/PAUSA-':
            if not corriendo:
                window.FindElement(event).Update('Pausar')
                #$% 'Pausar' es un término ambiguo, debería ser claro que
                #$% al hacer click se está decidiendo SALIR para retomar
                #$% en otro momento
                corriendo = True
                inicio = int(t.time())
            else:
                corriendo = False
                sg.Popup('Partida guardada, podrá retomarla\n'
                         'la próxima vez que acceda a ScrabbleAr')
                #$% Debería generarse una ventana NO POPUP que permita volver
                #$% al menú principal o cerrar el juego ("Volver al escritorio")
                window.FindElement(event).Update('Comenzar')

        elif event in atriljugador.fichas.keys():  # el click sucede en el atril
            atriljugador.click(event)
            actualizar_atril(atriljugador)
            if (atriljugador.estado == 'ELEGIR'
                and atriljugador.cambiar is not None):
                # si esto sucede significa que el click fue una deselección
                    pos = palabra.posficha(atriljugador.cambiar[0])
                    if pos is not None:
                        marcar, borrar, devolver = tablero.jugada(palabra, pos)
                        actualizar_tablero(marcar, borrar)

        # chequea si el click sucede en una posición válida del tablero
        elif event in tablero.getposibles(palabra, turno):
            # si estado == PASAR hay una ficha seleccionada
            # para colocar en el tablero
            if atriljugador.estado == 'PASAR':
                marcar, borrar, devolver = tablero.jugada(
                    palabra, event, atriljugador.cambiar[0],
                    atriljugador.cambiar[1])
                actualizar_tablero(marcar, borrar)
                imagen = palabra.fichas[event][0].getimagen()
                window.FindElement(event).Update(image_filename=imagen)
                atriljugador.setestado(1)

            elif event in palabra.getposiciones():
                marcar, borrar, devolver = tablero.jugada(palabra, event)
                actualizar_tablero(marcar, borrar)

            if devolver is not None:
                atriljugador.click(devolver)
                actualizar_atril(atriljugador)


    #cierre
    window.Close()

    if fin:
        sg.Popup('Puntajes')

if __name__ == '__main__':
    jugar()