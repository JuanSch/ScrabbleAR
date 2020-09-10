import PySimpleGUI as sg


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
                              border_width=0,)
            print(casilla.getimagen())
            linea.append(boton)
        botones.append(linea)
    return botones


def armar_atril(atril, dim_boton):
    fichas = [sg.Button(key=k, pad=(0, 0), image_filename=atril.imagen(k),
                        image_size=dim_boton, border_width=0,
                        button_color=('#DDDDDD', '#DDDDDD'))
              for k in atril.fichas.keys()]
    return fichas


def columna1_gui(elementos):
    dim_boton = 30, 30
    linea_superior = armar_atril(elementos['atril_ia'], dim_boton)
    botones_tablero = armar_tablero(elementos['tablero'], dim_boton)
    linea_inferior = armar_atril(elementos['atril_jugador'], dim_boton)
    botones_jugador = [sg.T(f'{"".join([" "]*12)}', font=('Arial', '11')),
                       sg.Button('JUGAR', key='-JUGAR-', size=(9, 2),
                                 disabled=True, font=('Arial', '9')),
                       sg.Button('PASAR\nTURNO', key='-PASAR-', size=(9, 2),
                                 disabled=True, font=('Arial', '9')),
                       sg.Button('CAMBIAR\nFICHAS', key='-CAMBIAR-', size=(9, 2),
                                 disabled=True, font=('Arial', '9')),
                       sg.Button('CANCELAR', key='-CANCELAR-', size=(9, 2),
                                 visible=False, font=('Arial', '9'))
                       ]
    for item in botones_jugador:
        linea_inferior.append(item)

    columna1 = [[sg.T('FICHAS IA:')],
                linea_superior,
                [sg.T('')],
                *botones_tablero,
                [sg.T('')],
                [sg.T('FICHAS JUGADOR:'), sg.T(f'{"".join([" "]*51)}'),
                 sg.T('CAMBIOS SIN COSTO:', font=('Arial', '9')),
                 sg.T('5', key='-CAMBIOS-', font=('Arial', '9'))],
                linea_inferior]
    return columna1


def columna2_gui(datos):
    columna2 = [[sg.Button('COMENZAR', key='-INI/PAUSA-', size=(12, 2)),
                 sg.Button('TERMINAR', key='-FIN-', size=(12, 2),
                           visible=False)],
                [sg.T('', font=('Arial', '6'))],
                [sg.T('TIEMPO', font=('Arial', '10'))],
                [sg.T(datos['reloj'], key='-RELOJ-',
                      font=('Arial', '16'))],
                [sg.T('', font=('Arial', '6'))],
                [sg.T('DIFICULTAD:', font=('Arial', '10'))],
                [sg.T(datos['dificultad'], key='-dificultad-',
                      font=('Arial', '16'))],
                [sg.T('', font=('Arial', '6'))],
                [sg.T('TURNO', font=('Arial', '10'))],
                [sg.T('-', size=(10, 1), key='-TURNO-',
                      font=('Arial', '14'))],
                [sg.T('', font=('Arial', '6'))],
                [sg.T('PUNTAJES', font=('Arial', '10'))],
                [sg.T(f'{datos["nombre"].upper()}:', size=(15, 1),
                      key='-PJUGADOR-', font=('Arial', '14'))],
                [sg.T('IA:', size=(15, 1), key='-PIA-',
                      font=('Arial', '14'))],
                [sg.T('', font=('Arial', '6'))],
                [sg.T('BOLSA', font=('Arial', '10'))],
                [sg.T(f'QUEDAN {len(datos["bolsa"].fichas)} FICHAS',
                      key='-BOLSA-', font=('Arial', '14'))],
                [sg.T('', font=('Arial', '6'))],
                [sg.T('HISTORIAL', font=('Arial', '10'))],
                [sg.Output(size=(22, 10))]
                ]
    return columna2
