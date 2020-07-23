import PySimpleGUI as sg
import random
import IA as ia
import time as t
import logica as lg
import json
import gui

def jugar():

    ###############
    # Apertura de archivos

    with open('configuraciones.json', 'r', encoding='UTF-8') as f:
        configs=json.load(f)
        nombre = configs['nombre']
        dificultad = configs['dificultad']
        tiempo=int(configs['tiempo'])*60  # conversion a minutos
        # tiempo = 20 * 60 #por si no  queres usar el tiempo de la config
        # solo descomentas la linea
        reloj=f'{divmod(tiempo, 60)[0]:02}:{divmod(tiempo, 60)[1]:02}'

    with open('valores_puntajes.json', 'r', encoding='UTF-8') as f:
        valores=json.load(f)
        if dificultad != "Personalizada":
            cant_letras = valores[f'{dificultad}']['bolsa']
            datos = valores[f'{dificultad}']['tablero']
        else:
            dificultad = valores['Personalizada']['dificultad_IA']
            dificultad_tablero = valores['Personalizada']['dificultad_Tablero']
            cant_letras = valores['Personalizada']['bolsa']
            datos = valores[dificultad_tablero]['tablero']
        casillas = {k: v for k, v in list(datos.items())[1:]}
        columnas, filas = datos['dimensiones']
        puntos = valores['puntos_letra']

    ###############

    dim_boton = (40, 40)

    tablero = lg.Tablero(columnas, filas, casillas)
    atril_jugador = lg.Atril()
    atril_IA = lg.AtrilIA()
    palabra = lg.Palabra()
    bolsa = lg.Bolsa(cant_letras, puntos)

    eval_turno = lambda x,y: (x % 2) == y

    # interfaz
    linea_superior = gui.armar_atril(atril_IA, dim_boton)
    botones_tablero = gui.armar_tablero(tablero, dim_boton)
    linea_inferior = gui.armar_atril(atril_jugador, dim_boton)
    botones_jugador = [sg.T('      '),
                       sg.Button('JUGAR', key='-JUGAR-', size=(12, 2),
                                 disabled=True),
                       sg.T(''),
                       sg.Button('CAMBIAR', key='-CAMBIAR-', size=(12, 2),
                                 disabled=True)]
    for item in botones_jugador:
        linea_inferior.append(item)

    columna1 = [[sg.T('FICHAS IA:')],
                linea_superior,
                [sg.T('')],
                *botones_tablero,
                [sg.T('')],
                [sg.T('FICHAS JUGADOR:')],
                linea_inferior]

    columna2 = [[sg.Button('COMENZAR', key='-INI/PAUSA-', size=(12, 2))],
                [sg.T('')],
                [sg.T('TIEMPO', font=('Arial', '11'))],
                [sg.T(reloj, key='-RELOJ-', font=('Arial', '18'))],
                [sg.T('')],
                [sg.T('JUEGA:', font=('Arial', '11'))],
                [sg.T('-', size=(8,1), key='-TURNO-', font=('Arial', '14'))],
                [sg.T('')],
                [sg.T('PUNTAJES', font=('Arial', '11'))],
                [sg.T('JUGADOR:', size=(15,1), key='-PJUGADOR-',
                      font=('Arial', '14'))],
                [sg.T('IA:', size=(15,1), key='-PIA-', font=('Arial', '14'))],
                [sg.T('')],
                [sg.T('BOLSA', font=('Arial', '11'))],
                [sg.T(f'QUEDAN {len(bolsa.fichas)} FICHAS',
                      key='-BOLSA-', font=('Arial', '14'))]
                ]

    layout = [[sg.Column(columna1), sg.Column(columna2)]]

    #inicializacion
    window = sg.Window('Ventana de juego').Layout(layout)

    #bucle
    corriendo = False
    fin = False
    turno = 0
    puntos_jugador = 0
    puntos_ia = 0
    turno_jugador = random.randrange(0, 2)
    while not fin:
        event, _values = window.Read(timeout=500)

        if event is None:
            break
        
        if event == '-INI/PAUSA-':
            if not corriendo:
                window.FindElement(event).Update('Posponer')
                #$% 'Pausar' es un término ambiguo, debería ser claro que
                #$% al hacer click se está decidiendo SALIR para retomar
                #$% en otro momento

                # Inicialización de los datos de reloj
                corriendo = True
                inicio = int(t.time())

                # Inicialización de atriles
                atril_jugador.recibirfichas(bolsa.entregar_fichas(
                    atril_jugador.pedirfichas()))
                atril_jugador.setestado(0)
                gui.actualizar_atril(atril_jugador, window)
                atril_IA.recibirfichas(bolsa.entregar_fichas(
                    atril_IA.pedirfichas()))
                gui.actualizar_atril(atril_IA, window)
                window.FindElement('-BOLSA-').Update(
                    f'QUEDAN {len(bolsa.fichas)} FICHAS')
                window.FindElement('-PJUGADOR-').Update(
                    f'JUGADOR: {puntos_jugador}')
                window.FindElement('-PIA-').Update(
                    f'IA: {puntos_ia}')

                # Inicia control de turnos
                if eval_turno(turno, turno_jugador):
                    window.FindElement('-TURNO-').Update('JUGADOR')
                    atril_jugador.setestado(1)
                    window.FindElement('-CAMBIAR-').Update(disabled=False)
                else:
                    window.FindElement('-TURNO-').Update('IA')

            else:
                sg.Popup('Partida guardada, podrá retomarla\n'
                         'la próxima vez que acceda a ScrabbleAr')
                #$% Debería generarse una ventana NO POPUP que permita
                #$% volver al menú principal o cerrar el juego
                #$% ("Exit to desktop")
                break

        if corriendo:
            #TURNO JUGADOR
            if eval_turno(turno, turno_jugador):
                if event in atril_jugador.fichas.keys(): # click en el atril
                    atril_jugador.click(event)
                    gui.actualizar_atril(atril_jugador, window)
                    if (atril_jugador.estado == 'ELEGIR'
                        and atril_jugador.cambiar is not None):
                        # si esto sucede significa que el click
                        # fue una deselección
                            pos = palabra.posficha(atril_jugador.cambiar[0])
                            if pos is not None:
                                marcar, borrar, devolver =\
                                    tablero.jugada(palabra, pos, turno)
                                gui.actualizar_tablero(marcar, borrar, window, tablero)
                                # Se deshabilita el boton de jugar
                                # si la palabra ya no es testeable
                                if not palabra.probar():
                                    window.FindElement('-JUGAR-').\
                                        Update(disabled=True)

                # Chequea si el click sucede en una posición válida del tablero
                elif event in tablero.getposibles(palabra, turno):
                    # si estado == PASAR hay una ficha seleccionada
                    # para colocar en el tablero
                    if atril_jugador.estado == 'PASAR':
                        marcar, borrar, _devolver = tablero.jugada(
                            palabra, event, turno, atril_jugador.cambiar[0],
                            atril_jugador.cambiar[1])
                        gui.actualizar_tablero(marcar, borrar, window, tablero)
                        imagen = palabra.fichas[event][0].getimagen()
                        window.FindElement(event).Update(image_filename=imagen)
                        atril_jugador.setestado(1)

                    # si estado != PASAR puede haberse deseleccionado una ficha
                    # ya colocada en el tablero
                    elif event in palabra.getposiciones():
                        marcar, borrar, devolver = tablero.jugada(palabra, event, turno)
                        gui.actualizar_tablero(marcar, borrar, window, tablero)
                        atril_jugador.click(devolver)
                        gui.actualizar_atril(atril_jugador, window)

                    if palabra.probar():
                        window.FindElement('-JUGAR-').Update(disabled=False)
                    else:
                        window.FindElement('-JUGAR-').Update(disabled=True)

                elif event == '-JUGAR-':
                    if ia.validar_palabra(palabra.__str__()):
                        # Actualizaciones a la lógica y valores de fondo
                        puntos_jugador += tablero.fijar_palabra(palabra)
                        atril_jugador.eliminar(palabra)
                        #Actualizaciones de GUI
                        gui.actualizar_tablero((), marcar, window, tablero)
                        # marcar siempre va a tener algún valor,
                        # aunque sea vacío, en cuyo caso
                        # lo maneja la excepción en la propia función
                        for key in palabra.getposiciones():
                            imagen = tablero.getcasilla(key).getimagen()
                            window.FindElement(key).Update(
                                image_filename=imagen)
                        window.FindElement('-PJUGADOR-').Update(
                            f'JUGADOR: {puntos_jugador}')
                        gui.actualizar_atril(atril_jugador, window)
                        window.FindElement('-TURNO-').Update('IA')
                        atril_jugador.setestado(0)
                        window.FindElement('-CAMBIAR-').Update(disabled=True)
                        window.FindElement('-JUGAR-').Update(disabled=True)

                        # Se vacía la palabra
                        palabra.vaciar()

                        # Cambio de turno
                        turno += 1
                    else:
                        sg.Popup(f'"{palabra.__str__()}" no existe\n'
                                 f'en nuestro diccionario')

            # TURNO IA
            else:
                palabra_ia = ia.elegir_palabra(atril_IA.fichas, dificultad)
                if palabra_ia != None:
                    sg.Popup('La IA todavía no aprendió a usar el tablero\n'
                            f'pero quiso jugar la palabra: "{palabra_ia}"')
                else: 
                    sg.Popup('La IA no puede formar ninguna palabra, pasa de turno')
                # Cambio de turnos
                turno += 1
                window.FindElement('-TURNO-').Update('JUGADOR')
                atril_jugador.setestado(1)
                window.FindElement('-CAMBIAR-').Update(disabled=False)


            # Control y actualización de reloj
            reloj, corriendo = gui.temporizador(tiempo, inicio, corriendo)
            window.FindElement('-RELOJ-').Update(reloj)
            if reloj=='FIN':
                corriendo=False
                fin=True

    #cierre
    window.Close()

    #$% yo creo que la funcion actualizar puntajes va dentro de logica en vez de la IA 
    if fin:
        if puntos_jugador > puntos_ia: #evalua quien gana
            if ia.actualizar_puntajes([nombre, puntos_jugador], difucultad): #evalua si entra en el top10 (si entra se agrega)
                sg.Popup('¡Ganaste y entraste en el top 10! \n Tu puntiacion es: ' + str(puntos_jugador))
                lg.top10()
            else:
                sg.Popup('¡Ganaste! \n Tu puntiacion es: ' + str(puntos_jugador))
            #ganaste
        elif puntos_jugador == puntos_ia:
            if ia.actualizar_puntajes([nombre, puntos_jugador], dificultadd):
                sg.Popup('¡Empataste y entraste en el top 10! \n Tu puntiacion es: ' + str(puntos_jugador))
                lg.top10()
            else:
                sg.Popup('¡Empataste! La proxima ganarás \n Tu puntiacion es: ' + str(puntos_jugador))
        else:
            if ia.actualizar_puntajes([nombre, puntos_jugador], dificultad):
                sg.Popup('¡Perdiste pero entraste en el top 10! \n Tu puntiacion es: ' + str(puntos_jugador))
                lg.top10()
            else:
                sg.Popup('!Perdiste suerte la próxima! \n Tu puntiacion es: ' + str(puntos_jugador))

if __name__ == '__main__':
    jugar()