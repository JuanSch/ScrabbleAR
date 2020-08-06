import PySimpleGUI as sg
import time as t
import logica as lg
import IA as ia
from os import remove
import pickle
import json
import random


def temporizador(tiempo, inicio, corriendo):
    """
    Modulo que recibe tres parametros 
    tiempo = en segundos, la cantidad de tiempo restante
    inicio = el momento t.time de inicio del contador 
    corriendo = variable booleana que indica si el tiempo se terminó o no
        True si el tiempo no se terminó
        False si el tiempo se terminó
    """
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


def inicializar(continuar):
    try:
        with open('configuraciones.json', 'r', encoding='UTF-8') as f:
            configs = json.load(f)
            nombre = configs['nombre']
            dificultad = configs['dificultad']
            if not continuar:
                tiempo = int(configs['tiempo']) * 60  # conversion a minutos
    except FileNotFoundError:
        return 'Error al intentar abrir configuraciones.json \n' \
               'el archivo parece no exisitir'
    else:
        if not continuar:
            try:
                with open('valores_puntajes.json', 'r', encoding='UTF-8') as f:
                    valores = json.load(f)
                    if dificultad != "Personalizada":
                        dificultad_ia = str(dificultad)
                        cant_letras = valores[f'{dificultad}']['bolsa']
                        datos = valores[f'{dificultad}']['tablero']
                        puntos = valores['puntos_letra']
                    else:
                        dificultad_ia = valores['Personalizada']['dificultad_IA']
                        dificultad_tablero = valores['Personalizada']['dificultad_Tablero']
                        cant_letras = valores['Personalizada']['bolsa']
                        datos = valores[dificultad_tablero]['tablero']
                        puntos = valores['Personalizada']['puntos_letra']  
                    casillas = {k: v for k, v in list(datos.items())[1:]}
                    columnas, filas = datos['dimensiones']
            except FileNotFoundError:
                return 'Error al intentar abrir valores_puntajes.json \n' \
                       'el archivo parece no exisitir'
            else:
                tablero = lg.Tablero(columnas, filas, casillas)
                atril_jugador = lg.Atril()
                atril_ia = lg.AtrilIA()
                palabra = lg.Palabra()
                bolsa = lg.Bolsa(cant_letras, puntos)
                puntos_jugador = 0
                puntos_ia = 0
                turno_jugador = random.randrange(0, 2) == 0
                reloj = f'{divmod(tiempo, 60)[0]:02}:{divmod(tiempo, 60)[1]:02}'
                datos_partida = {
                    'nombre': nombre,
                    'tablero': tablero,
                    'atril_jugador': atril_jugador,
                    'atril_ia': atril_ia,
                    'palabra': palabra,
                    'bolsa': bolsa,
                    'dificultad': dificultad,
                    'dificultad_ia': dificultad_ia,
                    'puntos_jugador': puntos_jugador,
                    'puntos_ia': puntos_ia,
                    'turno_jugador': turno_jugador,
                    'tiempo': tiempo,
                    'reloj': reloj
                }
        else:
            try:
                with open('continuar_partida.pickle', 'rb') as f:
                    datos_partida = pickle.load(f)
            except FileNotFoundError:
                return 'Error al intentar abrir valores_puntajes.json \n' \
                       'el archivo parece no exisitir'
    return datos_partida


def columna1_gui(elementos):
    dim_boton = 40, 40
    linea_superior = armar_atril(elementos['atril_ia'], dim_boton)
    botones_tablero = armar_tablero(elementos['tablero'], dim_boton)
    linea_inferior = armar_atril(elementos['atril_jugador'], dim_boton)
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
    return columna1


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
    except TypeError:   # la función puede recibir borrar = None
        pass
    try:
        for casilla in marcar:
            imagen = tablero.getcasilla(casilla).getimagen(True)
            window.FindElement(casilla).Update(
                image_filename=imagen)
    except TypeError:   # la función puede recibir marcar = None
        pass


def partida(window, datos_partida):

    def iniciar():
        """
        Se ejecuta cuando el jugador decide comenzar la partida
        (sea una nueva partida o una continuación)
        - Inicializa el reloj
        - Hace la primera carga de fichas en los atriles
        - Habilita los botones del jugador si es su turno

        return: (int) el valor de t.time en segundos al momento
        de inicializarse
        """
        nonlocal window
        nonlocal bolsa
        nonlocal atril_ia
        nonlocal atril_jugador
        nonlocal turno_jugador

        window.FindElement(event).Update('POSPONER')

        # Inicialización de los datos de reloj
        ini = int(t.time())

        # Inicialización de atriles
        atril_jugador.recibir(bolsa.entregar(atril_jugador.pedir()))
        atril_jugador.setestado(0)
        actualizar_atril(atril_jugador, window)
        atril_ia.recibir(bolsa.entregar(atril_ia.pedir()))
        actualizar_atril(atril_ia, window)
        window.FindElement('-BOLSA-').Update(f'QUEDAN {len(bolsa.fichas)} FICHAS')
        window.FindElement('-PJUGADOR-').Update(f'JUGADOR: {puntos_jugador}')
        window.FindElement('-PIA-').Update(f'IA: {puntos_ia}')

        # Inicia control de turnos
        if turno_jugador:
            window.FindElement('-TURNO-').Update('JUGADOR')
            atril_jugador.setestado(1)
            window.FindElement('-CAMBIAR-').Update(disabled=False)
        else:
            window.FindElement('-TURNO-').Update('IA')

        return ini

    def posponer(datos):
        """
        Se ejecuta si el jugador hace click en 'POSPONER'
        lanza un popup que le pide confirmar, y ejecuta con base en
        su decisión:
        - Si decide salir: los datos de la partida se guardan en un pickle
        - Si no no se hace nada

        return: (bool) True si el usuario desea salir, False en caso contrario
        """
        salir = sg.PopupOKCancel('Se guardará la partida y volverá al menú principal\n'
                                 '¿Desea continuar?')
        if salir:
            try:
                with open('continuar_partida.pickle', 'wb') as f:
                    pickle.dump(datos, f)
            except IOError:
                sg.PopupAutoClose('Hubo un error al tratar de guardar la partida\n'
                                  'no podrás retomarla más tarde :(',
                                  auto_close_duration=5)
            else:
                sg.PopupAutoClose('Partida guardada, podrá retomarla\n'
                                  'la próxima vez que acceda a ScrabbleAr',
                                  auto_close_duration=5)
        return salir

    def click_atril(evento):
        """
        Se ejecutará cada vez que -durante el turno del usuario-
        se efectué un click en el atril
        Maneja todas las actualizacions de objetos y gui
        que puedan ser necesarias
        """

        nonlocal window
        nonlocal tablero
        nonlocal atril_jugador
        nonlocal palabra
        atril_jugador.click(evento)
        actualizar_atril(atril_jugador, window)
        if (atril_jugador.estado == 'ELEGIR'
                and atril_jugador.cambiar != []):
            # si esto sucede significa que el click
            # fue una deselección
            pos = palabra.posficha(atril_jugador.cambiar[0])
            if pos is not None:
                marcar, borrar, devolver = tablero.jugada(palabra, pos)
                actualizar_tablero(marcar, borrar, window, tablero)
                # Se deshabilita el boton de jugar
                # si la palabra ya no es testeable
                if not palabra.probar():
                    window.FindElement('-JUGAR-').Update(disabled=True)

    def click_tablero(evento):
        """
        Se ejecutará cada vez que -durante el turno del usuario-
        se efectué un click en el tablero
        Maneja todas las actualizacions de objetos y gui
        que puedan ser necesarias

        return: (list) de (tuple) o None. La lista de los elementos
        marcados como 'posibles' para su eventual borrado
        en caso de fijarse la palabra en el tablero (ver: click_jugar())
        """

        nonlocal atril_jugador
        nonlocal tablero
        nonlocal palabra
        nonlocal window
        # si estado == PASAR hay una ficha seleccionada
        # para colocar en el tablero
        if atril_jugador.estado == 'PASAR':
            marcar, borrar, _devolver = tablero.jugada(
                palabra, evento, atril_jugador.cambiar[0],
                atril_jugador.cambiar[1])
            actualizar_tablero(marcar, borrar, window, tablero)
            img = palabra.fichas[evento][0].getimagen()
            window.FindElement(evento).Update(image_filename=img)
            atril_jugador.setestado(1)
        # si estado != PASAR puede haberse deseleccionado una ficha
        # ya colocada en el tablero
        elif evento in palabra.getposiciones():
            marcar, borrar, devolver = tablero.jugada(palabra, evento)
            actualizar_tablero(marcar, borrar, window, tablero)
            atril_jugador.click(devolver)
            actualizar_atril(atril_jugador, window)
        # si hay más de dos letras en la palabra y son todas contiguas
        # habilita el botón 'JUGAR', lo deshabilita en caso contrario
        if palabra.probar():
            window.FindElement('-JUGAR-').Update(disabled=False)
        else:
            window.FindElement('-JUGAR-').Update(disabled=True)
        return marcar if marcar else []

    def click_jugar(borrar):
        """
        Se ejecutará cada vez que -durante el turno del usuario-
        se haga click en el botón 'JUGAR'
        Evalúa si la palabra en el tablero es válida, en cuyo caso
        la fija y efectúa las actualizacioes pertinentes
        de estructuras de control y gui

        recibe:
        - borrar: (list) de (tuple) o None. la lista de los elementos
        marcados como 'posibles' la última vez que se agregó
        una ficha al tablero (ver: click_tablero()).
        """
        nonlocal window
        nonlocal tablero
        nonlocal palabra
        nonlocal atril_jugador
        nonlocal puntos_jugador
        nonlocal turno_jugador
        nonlocal fin

        if ia.validar_palabra(str(palabra)):
            # Actualizaciones a la lógica y valores de fondo
            puntos_jugador += tablero.fijar_palabra(palabra)
            atril_jugador.eliminar([v[1] for _k, v in palabra.fichas.items()])
            # Actualizaciones de GUI
            actualizar_tablero((), borrar, window, tablero)
            # borrar siempre va a tener algún valor,
            # aunque sea vacío, en cuyo caso
            # lo maneja la excepción en la propia función
            for key in palabra.getposiciones():
                img = tablero.getcasilla(key).getimagen()
                window.FindElement(key).Update(image_filename=img)
            window.FindElement('-PJUGADOR-').Update(
                f'JUGADOR: {puntos_jugador}')
            actualizar_atril(atril_jugador, window)
            window.FindElement('-TURNO-').Update('IA')
            atril_jugador.setestado(0)
            window.FindElement('-CAMBIAR-').Update(disabled=True)
            window.FindElement('-JUGAR-').Update(disabled=True)
            # Se piden fichas nuevas para el atril
            fichas_nuevas = bolsa.entregar(atril_jugador.pedir())
            if fichas_nuevas:  # Si la lista tiene elementos
                # Se reciben las fichas
                atril_jugador.recibir(fichas_nuevas)
                actualizar_atril(atril_jugador, window)
                # Se actualiza el estado de la bolsa
                window.FindElement('-BOLSA-').Update(f'QUEDAN {len(bolsa.fichas)} FICHAS')
                # Se vacía la palabra
                palabra.vaciar()
                # Cambia el turno
                turno_jugador = not turno_jugador
            else:
                fin = True
        else:
            sg.Popup(f'"{str(palabra)}" no existe\n'
                     f'en nuestro diccionario')

    def click_cambiar():
        """Activa/desactiva y concreta el canje de fichas con la bolsa"""

        nonlocal atril_jugador
        nonlocal tablero
        nonlocal bolsa
        nonlocal palabra
        nonlocal window
        nonlocal turno_jugador

        if atril_jugador.estado == 'CAMBIAR':
            if atril_jugador.cambiar:  # Si hay fichas para cambiar
                # Efectúa el intercambio con la bolsa
                atril_jugador.recibir(bolsa.intercambiar(atril_jugador.entregar()))
                actualizar_atril(atril_jugador, window)
                turno_jugador = not turno_jugador  # Cambia de turno
            atril_jugador.setestado(1)  # Retorna al estado de juego
        else:  # Si el atril estaba en otro estado
            if palabra.min is not None:  # Si había fichas colocadas en el tablero
                casillas = palabra.getposiciones()
                # Deselecciona las fichas - palabra y atril apuntan al mismo objeto
                for pos in casillas:
                    palabra.fichas[pos][0].select = False
                # Actualiza la visualización del tablero
                borrar = list(tablero.getposibles()) + casillas
                actualizar_tablero((), borrar, window, tablero)
                # Actualiza la visualización del atril
                actualizar_atril(atril_jugador, window)
                # Vacía la palabra
                palabra.vaciar()
                # Inhabilita el botón jugar (podía o no estar habilitado)
                window.FindElement('-JUGAR-').Update(disabled=True)
            atril_jugador.setestado(3)  # Pone al atril en modo de intercambio de fichas
        #$% Cambia la visualización del botón

    def turno_ia(dif_ia):

        def seleccionar_fichas(palabra_ia, atril_ia):
            espacios = []
            atril = dict(atril_ia.fichas)
            for char in palabra_ia:
                for k, v in atril.items():
                    if v.letra == char:
                        espacios.append(k)
                        break
                atril.pop(k)
            return espacios

        nonlocal window
        nonlocal atril_ia
        nonlocal atril_jugador
        nonlocal tablero
        nonlocal turno_jugador
        nonlocal puntos_ia
        nonlocal fin

        palabras_ia = ia.elegir_palabra(atril_ia.fichas)
        if palabras_ia is not None:  # Si la IA puede generar palabras
            tupla = ia.elegir_espacio(tablero, palabras_ia, dif_ia)
            if tupla is not None:  # Si la IA encuentra un espacio en el tablero
                casillas, palabra_ia, puntos = tupla
                origen = seleccionar_fichas(palabra_ia, atril_ia)
                for i in range(len(casillas)):
                    ficha = atril_ia.fichas[origen[i]]
                    pos = casillas[i]
                    casilla = tablero.getcasilla(pos)
                    casilla.ocupar(ficha)
                    img = casilla.getimagen()
                    window.FindElement(pos).Update(image_filename=img)
                atril_ia.eliminar(origen)
                actualizar_atril(atril_ia, window)
                # Se actualizan los puntos
                puntos_ia += puntos
                window.FindElement('-PIA-').Update(f'IA: {puntos_ia}')
                # Se piden fichas nuevas para el atril
                fichas_nuevas = bolsa.entregar(atril_ia.pedir())
                if fichas_nuevas:  # Si la lista tiene elementos
                    # Se reciben las fichas
                    atril_ia.recibir(fichas_nuevas)
                    actualizar_atril(atril_ia, window)
                    # Se actualiza el estado de la bolsa
                    window.FindElement('-BOLSA-').Update(f'QUEDAN {len(bolsa.fichas)} FICHAS')
                else:
                    fin = True

        else:
            sg.Popup('La IA no puede formar ninguna palabra, pasa de turno')

        # Se habilitan los botones del jugador
        window.FindElement('-TURNO-').Update('JUGADOR')
        window.FindElement('-CAMBIAR-').Update(disabled=False)
        atril_jugador.setestado(1)

        # Cambia el turno
        turno_jugador = not turno_jugador

    nombre = datos_partida['nombre']
    tablero = datos_partida['tablero']
    atril_jugador = datos_partida['atril_jugador']
    atril_ia = datos_partida['atril_ia']
    palabra = datos_partida['palabra']
    bolsa = datos_partida['bolsa']
    dificultad_ia = datos_partida['dificultad_ia']
    puntos_jugador = datos_partida['puntos_jugador']
    puntos_ia = datos_partida['puntos_ia']
    turno_jugador = datos_partida['turno_jugador']
    tiempo = datos_partida['tiempo']
    corriendo = False
    fin = False

    while not fin:
        event, _values = window.Read(timeout=500)

        if event is None:
            break

        elif event == '-INI/PAUSA-':
            if corriendo:
                if posponer(datos_partida):
                    break
            else:
                inicio = iniciar()
                corriendo = True

        if corriendo:
            # TURNO JUGADOR
            if turno_jugador:
                if event in atril_jugador.fichas.keys():  # click en el atril
                    click_atril(event)
                # Chequea si el click sucede en una posición válida del tablero
                elif event in tablero.getposibles():
                    marcar = click_tablero(event)
                elif event == '-JUGAR-':
                    click_jugar(marcar)
                elif event == '-CAMBIAR-':
                    click_cambiar()

            # TURNO IA
            else:
                turno_ia(dificultad_ia)

            # Control y actualización de reloj
            reloj, corriendo = temporizador(tiempo, inicio, corriendo)
            window.FindElement('-RELOJ-').Update(reloj)
            if reloj == 'FIN':
                corriendo = False
                fin = True

    # cierre
    window.Close()

    return fin


def fin_partida(continuar, datos_partida):

    nombre = datos_partida['nombre']
    dificultad = datos_partida['dificultad']
    puntos_jugador = datos_partida['puntos_jugador']
    puntos_ia = datos_partida['puntos_ia']

    if continuar:
        remove("continuar_partida.pickle")  # Como terminó la partida borramos la partida guardada
    if puntos_jugador > puntos_ia:  # evalua quien gana
        if actualizar_puntajes([nombre, puntos_jugador],
                                   dificultad):  # evalua si entra en el top10 (si entra se agrega)
            sg.Popup('¡Ganaste y entraste en el top 10! \n Tu puntiacion es: ' + str(puntos_jugador))
            lg.top10()
        else:
            sg.Popup('¡Ganaste! \n Tu puntiacion es: ' + str(puntos_jugador))
        # ganaste
    elif puntos_jugador == puntos_ia:
        if actualizar_puntajes([nombre, puntos_jugador], dificultad):
            sg.Popup('¡Empataste y entraste en el top 10! \n Tu puntiacion es: ' + str(puntos_jugador))
            lg.top10()
        else:
            sg.Popup('¡Empataste! La proxima ganarás \n Tu puntiacion es: ' + str(puntos_jugador))
    else:
        if actualizar_puntajes([nombre, puntos_jugador], dificultad):
            sg.Popup('¡Perdiste pero entraste en el top 10! \n Tu puntiacion es: ' + str(puntos_jugador))
            lg.top10()
        else:
            sg.Popup('!Perdiste suerte la próxima! \n Tu puntiacion es: ' + str(puntos_jugador))


def actualizar_puntajes(tupla, dificultad):
    """recibe una tupla[0]= nombre de usuario y tupla[1] el puntaje
    si el puntaje entra en el top diez, se lo inserta donde corresponde
    en orden descendiente de puntajes y se elemina el ultimo
    ya que la lista con el nuevo puntaje insertado tiene 11 elementos"""
    try:
        with open("valores_puntajes.json", 'r') as f:    # Cargo el diccionario de puntajes
            dic = json.load(f)
    except FileNotFoundError:   # si no existe el archivo, lo creo
        #$% crearvalores()
        with open("valores_puntajes.json", 'r') as f:
            dic = json.load(f)
    top = dic['top10'][dificultad]
    ok = False
    if tupla[1] >= top[-1][1]:    # si el puntaje es mayor o igual al puntaje minimo en el top
        for i in range(len(top)):
            if top(i)[1] > tupla[1]:    # busco la posicion a insertar
                top.insert(i, tupla)  # inserto (ahora la lista tiene 11 elementos, desde 0 a 10)
                if len(top) == 11:
                    top.pop(10)  # remuevo el elemento en la posicion 10,
                    # es decir el decimo-primer elemento
                ok = True
    if ok:
        dic['top10'][dificultad] = top
    with open("valores_puntajes.json", 'w') as f:
        json.dump(top, f, indent=4)
    return ok
