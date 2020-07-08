import PySimpleGUI as sg
import json
from tableros import jugar

def config_nuevo_juego(configuracion):
    """
    Muestra una ventana de PySimpleGUI en la que podemos elegir
    la dificultad y el tiempo de juego tambien acceder al menu
    de configuracion, una vez definidas las preferencias podremos jugar
    haciendo click en "Jugar"
    """
    s = []
    for i in range(1,61):
        s.append(str(i))

    layout = [
        [sg.T("Nuevo juego", size=(17,1), justification = "center",
              font=("Georgia", 17))],
        [sg.T("Dificultad: "),
         sg.DropDown(('Facil','Medio','Dificil','Personalizada'),
                     default_value=(configuracion['dificultad']),size=(10,1))],
        [sg.T("Tiempo de juego (minutos): ", size=(22, 1)),
         sg.InputCombo((s),size=(5,1),default_value=(configuracion['tiempo']))],
        [sg.Button("Jugar", size=(12, 1), key="-jugar-"),
         sg.Button("Personalizar",size=(12,1), key="-personalizar-")]
        ]

    window_nuevo_juego = sg.Window("ScrabbleAR - Nuevo juego").Layout(layout)

    while True:
        event, values = window_nuevo_juego.Read()
        if event == "-jugar-":
            configuracion['dificultad'] = values[0]
            configuracion['tiempo'] = values[1]
            break
        elif event == "-personalizar-":
            configurar(configuracion)
        else:
            break

    window_nuevo_juego.Close()
    
    if event == "-jugar-":
        return(configuracion,True)
    else:
        return(configuracion,False)

def configurar(dic):
    """
    Muestra una ventana de PySimpleGui donde podemos elegir la cantidad
    de apariciones de cada letra en caso de modificar un valor,
    debemos hacer click en guardar por cada letra modificada
    """
    letras = dic['personalizada']
    lista_letras= []
    lista_valores = []
    for key in letras:
        lista_letras.append(key)
    for y in range(13):
        lista_valores.append(y)
    df_vl = letras['a']
    layout=[
        [sg.T("Perfil personalizado", size=(17,1), justification = "center",
              font=("Georgia", 17))],
        [sg.T("Letra",font=("Georgia", 12)),
         sg.Combo(lista_letras, size=(8,1), default_value= 'a'),
         sg.T("Cantidad:", font=("Georgia", 12),),
         sg.Combo(lista_valores, size=(8,1), default_value=df_vl)],
        [sg.Button("Guardar", size=(12, 1), key="-guardar-")]
        ]

    window_configurar = sg.Window("ScrabbleAR - Configurar").Layout(layout)

    while True:
        event, values = window_configurar.Read()
        if event == None:
            break
        elif event == '-guardar-':
            df_vl = letras[values[0]] = values[1]
            dic['personalizada'] = letras
            with open('configuraciones.json','w', encoding='UTF-8') as f:
                json.dump(dic, f, indent=4)
    window_configurar.Close()
    
def pantalla_inicial(): 
    """
    Muestra una ventana de PySimpleGui donde está el menu principal 
    las opciones del menu son 
        Crear nueva partida
        Continuar una partida existente
        Configurar la dificultad personalizada
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
            with open('configuraciones.json','r', encoding='UTF-8') as f:
                configs = json.load(f)
                configs, condicion = config_nuevo_juego(configs)
            with open('configuraciones.json','w', encoding='UTF-8') as f:
                json.dump(configs, f, indent= 4)
            if condicion:
                jugar() 
                break

        elif event in "-continuar-":

            pass

        elif event in "-configuracion-":
            with open('configuraciones.json', encoding='UTF-8') as f:
                configs = json.load(f)
            configurar(configs)

        elif event in "-puntajes-":
            pass
        
    window.Close()


    

if __name__ == "__main__":
    #configuracion= {'dificultad': 'Facil', 'tiempo': 30}
    #config(configuracion)
    pantalla_inicial()
    #temporizador(2)
    # with open('configuraciones.json','r', encoding='UTF-8') as f:
    #     configs =json.load(f)
    #     configurar(configs)