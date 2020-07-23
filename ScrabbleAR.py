import PySimpleGUI as sg
import json
from tableros import jugar
from logica import top10

def config_nuevo_juego():
    """
    Muestra una ventana de PySimpleGUI en la que podemos elegir
    la dificultad y el tiempo de juego tambien acceder al menu
    de configuracion, una vez definidas las preferencias podremos jugar
    haciendo click en "Jugar"
    """
    s = []
    for i in range(1,61):
        s.append(str(i))
    try:
        with open('configuraciones.json','r', encoding='UTF-8') as f:
            configuracion = json.load(f)
            nombre = configuracion['nombre']
    except FileNotFoundError:
        #$% crearconfiguracion()
        with open('configuraciones.json','r', encoding='UTF-8') as f:
            configuracion = json.load(f)
            nombre = configuracion['nombre']

    layout = [
        [sg.T("Nuevo juego", size=(17,1), justification = "center",
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
                sg.popup('¡Atencion! \n En la dificultad personalizada no se guardan los puntajes')
            break
        elif event == "-jugar-" and values[2] == "":
            sg.popup('Ingrse un nombre')
        elif event == "-personalizar-":
            configurar()
        else:
            break

    with open('configuraciones.json','w', encoding='UTF-8') as f:
        json.dump(configuracion, f, indent= 4)

    window_nuevo_juego.Close()
    
    if event == "-jugar-":
        return True
    else:
        return False

def configurar():
    """
    Muestra una ventana de PySimpleGui donde podemos elegir la cantidad
    de apariciones de cada letra en caso de modificar un valor,
    debemos hacer click en guardar por cada letra modificada
    """
    with open('valores_puntajes.json', encoding='UTF-8') as f:
                dic = json.load(f)

    letras = dic['Personalizada']['bolsa']
    print(letras)
    lista_letras= []
    lista_valores = []
    for key in letras:
        lista_letras.append(key[0])
    for y in range(13):
        lista_valores.append(y)
    df_vl = letras[0][1] 
    layout=[
        [sg.T("Perfil personalizado", size=(17,1), justification = "center",
              font=("Georgia", 17))],
        [sg.T("Letra",font=("Georgia", 12)),
         sg.Combo(lista_letras, size=(8,1), default_value= 'a'),
         sg.T("Cantidad:", font=("Georgia", 12),),
         sg.Combo(lista_valores, size=(8,1), default_value=df_vl)],
         [sg.T("Dificultad de la IA: "),
         sg.DropDown(('Facil','Medio','Dificil'),
                     default_value=(dic['Personalizada']['dificultad_IA']),size=(10,1))],
         [sg.T("Dificultad del tablero: "),
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
        values[2] = retorna la dificultad de la IA
        values[3] = retorna la dificultad del tablero
        """
        if event == None:
            break
        elif event == '-guardar-':
            for item in letras:
                if item[0] == values[0]:
                    item[1] = values[1]
                    df_vl = values[1]
                    break
                pass
            dic['Personalizada']['bolsa'] = letras
            dic['Personalizada']['dificultad_IA'] = values[2]
            dic['Personalizada']['dificultad_Tablero'] = values[3]
            with open('valores_puntajes.json','w', encoding='UTF-8') as f:
                json.dump(dic, f, indent=4)
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

    layout = [
        [sg.T("Scrabble AR", size=(17, 1), justification="center",
              font=("Georgia", 17))],
        [sg.T(' '),
         sg.Button('Nueva partida', size=(25, 2), key="-nueva-")],
        [sg.T(' '),
         #$% Este botón sólo debería estar habilitado si es que hay
         #$%una partida guardada lista para continuar
         sg.Button('Continuar partida', size=(25, 2),
                   key="-continuar-", disabled=True)],
        [sg.T(' '),
         sg.Button('Configuración', size=(25, 2), key="-configuracion-")],
        [sg.T(' '),
         sg.Button('Mejores puntajes', size=(25, 2), key="-puntajes-")],
        [sg.T(' '), sg.T("  ", size=(17, 1), justification="center")]
        ]

    window = sg.Window("Menu Principal").Layout(layout)
    
    while True:
        event, _values = window.Read()

        if event == None:
            break

        elif event in "-nueva-":
            if config_nuevo_juego():
                jugar()

        elif event in "-continuar-":
            pass

        elif event in "-configuracion-":
            configurar()

        elif event in "-puntajes-":
            top10()
        
    window.Close()


    

if __name__ == "__main__":
    pantalla_inicial()