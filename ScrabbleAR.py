import PySimpleGUI as sg
import json
from partida.jugar import jugar
from auxiliares.utilidades import ruta, top10, reglas, crear_valores_puntajes
from os import remove


def config_nuevo_juego():
    """
    Muestra una ventana de PySimpleGUI en la que podemos elegir
    la dificultad y el tiempo de juego tambien acceder al menu
    de configuracion, una vez definidas las preferencias podremos jugar
    haciendo click en "Jugar"
    """
    s = []
    for i in range(1, 61):
        s.append(str(i))
    try:
        with open(f'archivos{ruta()}configuraciones.json',
                  'r', encoding='UTF-8') as f:
            configuracion = json.load(f)
            nombre = configuracion['nombre']
    except FileNotFoundError:
        configuracion = {
            "dificultad": "Medio",
            "tiempo": "10",
            "nombre": ""
                }
        nombre = configuracion['nombre']

    layout = [
        [sg.T("Nuevo juego", size=(17,1), justification="center",
              font=("Georgia", 17))],
        [sg.T("Dificultad: "),
         sg.DropDown(('Facil','Medio','Dificil','Personalizada'),
                     default_value=(configuracion['dificultad']),size=(10,1))],
        [sg.T("Tiempo de juego (minutos): ", size=(22, 1)),
         sg.InputCombo((s),size=(5,1),default_value=(configuracion['tiempo']))],
        [sg.T('Nombre de usuario'), sg.Input(nombre,size=(17,1))],
        [sg.Button("Jugar", size=(12, 1), key="-jugar-"),
         sg.Button("Personalizar",size=(12,1), key="-personalizar-")]
        ]

    window_nuevo_juego = sg.Window("ScrabbleAR - Nuevo juego").Layout(layout)

    while True:
        event, values = window_nuevo_juego.Read()
        if event == "-jugar-" and values[2] != "":
            configuracion['dificultad'] = values[0]
            configuracion['tiempo'] = values[1]
            configuracion['nombre'] = values[2]
            if values[0] == 'Personalizada':
                sg.popup('¡Atencion! \n En la dificultad personalizada'
                         'no se guardan los puntajes')
            break
        elif event == "-jugar-" and values[2] == "":
            sg.popup('Ingrse un nombre')
        elif event == "-personalizar-":
            configurar()
        else:
            break
    # No necesita manejo de excepciones porque está en modo escritura
    with open(f'archivos{ruta()}configuraciones.json', 'w',
              encoding='UTF-8') as f:
        json.dump(configuracion, f, indent=4)

    window_nuevo_juego.Close()
    
    if event == "-jugar-":
        return True
    else:
        return False


def preguntar_partida_nueva():
    """
    Modulo que genera un menu, te pregunta si queres borrar la partida guardada o conserarla 
    """
    layout = [
        [sg.T("Tiene una partida guardada, si continua, se borrará", justification="center",
              font=("Georgia", 14))],
        [sg.Button('Continuar'), sg.Button('Regresar')]
    ]
    window_preguntar = sg.Window("ScrabbleAR - Partida Guardada").Layout(layout)
    while True:
        event, _ = window_preguntar.Read()
        if event is None:
            condicion = False
            break
        elif event in 'Continuar':
            condicion = True
            break
        elif event in 'Regresar':
            condicion = False
            break

    window_preguntar.Close()
    return condicion


def configurar():
    """
    Muestra una ventana de PySimpleGui donde podemos elegir la cantidad
    de apariciones de cada letra en caso de modificar un valor,
    debemos hacer click en guardar por cada letra modificada
    """
    try:
        with open(f'archivos{ruta()}valores_puntajes.json',
                  encoding='UTF-8') as f:
            dic = json.load(f)
    except FileNotFoundError:
        dic = crear_valores_puntajes()
        with open(f'archivos{ruta()}valores_puntajes.json', 'w',
                  encoding='UTF-8') as f:
            json.dump(dic, f, indent=4)

    letras = dic['Personalizada']['bolsa']
    lista_letras= []
    for elemento in letras:
        lista_letras.append(elemento[0])
    valor_letra = letras[0][1] 
    valor_punto = dic['Personalizada']['puntos_letra']['a']
    layout=[
        [sg.T("Perfil personalizado", size=(17,1), justification = "center",
              font=("Georgia", 17))],
        [sg.T("Letra",font=("Georgia", 12)),
         sg.Combo(lista_letras, size=(8,1), default_value= 'a', enable_events=True),
         sg.T("Cantidad:", font=("Georgia", 12),),
         sg.Slider(range=(1, 12), orientation='h', size=(13, 20), default_value=valor_letra),
         sg.T("Valor:", font=("Georgia", 12),),
         sg.Slider(range=(1, 20), orientation='h', size=(20, 20), default_value=valor_punto)],
        [sg.T("Dificultad de la IA: "),
         sg.DropDown(('Facil','Medio','Dificil'),
                     default_value=(dic['Personalizada']['dificultad_IA']),size=(10,1)),
                     sg.T("Dificultad del tablero: "),
         sg.DropDown(('Facil','Medio','Dificil'),
                     default_value=(dic['Personalizada']['dificultad_Tablero']),size=(10,1))],
        [sg.Button("Guardar", size=(12, 1), key="-guardar-")]
        ]

    window_configurar = sg.Window("ScrabbleAR - Configurar").Layout(layout)

    while True:
        event, values = window_configurar.Read()
        """
        values[0] = retorna la letra elegida
        values[1] = retorna la cantidad de letras
        values[2] = retorna el puntaje seleccionado
        values[3] = retorna la dificultad de la IA
        values[4] = retorna la dificultad del tablero
        """
        try:
            for item in letras:
                if item[0] == values[0]:
                    valor_letra = int(item[1])
            window_configurar.find_element(1).Update(valor_letra)
            valor_punto = dic['Personalizada']['puntos_letra'][values[0]]
            window_configurar.find_element(2).Update(valor_punto)
        except:
            break
        if event == None:
            break
        elif event == '-guardar-':
            for item in letras:
                if item[0] == values[0]:
                    item[1] = int(values[1])
                    break
            dic['Personalizada']['bolsa'] = letras
            dic['Personalizada']['puntos_letra'][values[0]] = int(values[2])
            dic['Personalizada']['dificultad_IA'] = values[3]
            dic['Personalizada']['dificultad_Tablero'] = values[4]
            try:
                with open(f'archivos{ruta()}valores_puntajes.json', 'w', encoding='UTF-8') as f:
                    json.dump(dic, f, indent=4)
                    sg.popup('Se guardaron los cambios', auto_close= True, auto_close_duration= 1)
            except FileNotFoundError:
                sg.popup('No se encuentra el archivo "valores_puntajes.json"')
    window_configurar.Close()


def pantalla_inicial(): 
    """
    Muestra una ventana de PySimpleGui donde está el menu principal 
    las opciones del menu son 
        Crear nueva partida
        Continuar una partida existente
        Configurar la dificultad Personalizada
        Mostrar los diez mejores puntajes
    """
    try:
        with open(f'archivos{ruta()}continuar_partida.pickle') as _:
            condicion = False
    except FileNotFoundError:
        condicion = True
    layout = [
        [sg.T("Scrabble AR", size=(17, 1), justification="center",
              font=("Georgia", 17))],
        [sg.T(' '),
         sg.Button('Nueva partida', size=(25, 2), key="-nueva-")],
        [sg.T(' '),
         sg.Button('Continuar partida', size=(25, 2),
                   key="-continuar-", disabled= condicion)],
        [sg.T(' '),
         sg.Button('Configuración', size=(25, 2), key="-configuracion-")],
        [sg.T(' '),
         sg.Button('Mejores puntajes', size=(25, 2), key="-puntajes-")],
        [sg.T(' '),
         sg.Button('Reglas', size=(25, 2), key="-reglas-")],
        [sg.T(' '), sg.T("  ", size=(17, 1), justification="center")]
        ]

    window = sg.Window("Menu Principal").Layout(layout)
    
    while True:
        event, _values = window.Read(timeout= 500)

        if event is None:
            break

        elif event in "-nueva-":
            if condicion:
                if config_nuevo_juego():
                    jugar()
            else:
                if preguntar_partida_nueva():
                    remove(f'archivos{ruta()}continuar_partida.pickle')
                    if config_nuevo_juego():
                        jugar()
                    
        elif event in "-continuar-":
            jugar(True)

        elif event in "-configuracion-":
            configurar()

        elif event in "-reglas-":
            reglas()

        elif event in "-puntajes-":
            top10()
        try:
            with open(f'archivos{ruta()}continuar_partida.pickle') as _:
                condicion = False
                window.find_element("-continuar-").Update(disabled = condicion)
        except FileNotFoundError:
            condicion = True
            window.find_element("-continuar-").Update(disabled = condicion)
        
    window.Close()


if __name__ == "__main__":
    pantalla_inicial()