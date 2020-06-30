import concurrent.futures
import PySimpleGUI as sg
import json
import time as t
from tableros import jugar

def salir():
    """
    Ventana de PySimpleGUI que te pregunta si realmente deseas salir
    Honestamente es un juego genial, ¿queien querria salir?
    """
    layout = [
        [sg.T("¿Realmente deseas salir?", size=(17,1), justification = "center",
              font=("Georgia", 17))],
        [sg.B("Si", size=(12, 1)),sg.B("No",size=(12,1))]
        ]
    window_salir = sg.Window("ScrabbleAR - salir del juego", layout)

    while True:
        event, _value = window_salir.read()
        if event == 'Si':
            condicion = True
            break
        else:
            condicion = False
            break
    window_salir.close()

    return(condicion)

def config_nuevo_juego(configuracion):
    """
    Muestra una ventana de PySimpleGUI en la que podemos elegir la dificultad y el tiempo de juego 
    tambien acceder al menu de configuracion, una vez definidas las preferencias podremos jugar
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
        [sg.T("Tiempo de juego (en minutos): ", size=(22, 1)),
         sg.InputCombo((s),size=(5,1),default_value=(configuracion['tiempo']))],
        [sg.B("Jugar", size=(12, 1), key="-jugar-"),sg.B("Personalizar",size=(12,1), key="-personalizar-")]
        ]

    window_nuevo_juego = sg.Window("ScrabbleAR - Nuevo juego", layout)

    while True:
        event, value = window_nuevo_juego.read()
        if event == "-jugar-":
            configuracion['dificultad'] = value[0]
            configuracion['tiempo'] = value[1] 
            break
        elif event == "-personalizar-":
            configurar(configuracion)
        else:
            break

    window_nuevo_juego.close()
    
    if event == "-jugar-":
        return(configuracion,True)
    else:
        return(configuracion,False)

def configurar(dic):
    """
    Muestra una ventana de PySimpleGui donde podemos elegir la cantidad de apariciones de cada letra
    en caso de modificar un valor, debemos hacer click en guardar por cada letra modificada 
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
        [sg.T("Letra",font=("Georgia", 12)), sg.Combo(lista_letras, size=(8,1), default_value= 'a'),
         sg.T("Cantidad:", font=("Georgia", 12),),sg.Combo(lista_valores,size=(8,1), default_value=df_vl)],
        [sg.B("Guardar", size=(12, 1), key="-guardar-")]
        ]

    window_configurar = sg.Window("ScrabbleAR - Configurar", layout)

    while True:
        event, value = window_configurar.read()
        if event == None:
            break
        elif event == '-guardar-':
            df_vl = letras[value[0]] = value[1]
            dic['personalizada'] = letras
            with open('configuraciones.json','w', encoding='UTF-8') as f:
                json.dump(dic, f, indent= 4)
    window_configurar.close()
    
def pantalla_inicial(): 
    """
    Muestra una ventana de PySimpleGui donde está el menu principal 
    las opciones del menu son 
        Crear nueva partida
        Continuar una partida existente
        Configurar la dificultad personalizada
        Mostrar los diez mejores puntajes
        Salir
    """

    layout = [
        [sg.T("Scrabble AR", size=(17, 1), justification="center",
              font=("Georgia", 17))],
        [sg.T(' '),sg.B('Nueva partida', size=(25, 2), key="-nueva-")],
        [sg.T(' '),sg.B('Continuar partida', size=(25, 2), key="-continuar-")],
        [sg.T(' '),sg.B('Configuración', size=(25, 2), key="-configuracion-")],
        [sg.T(' '),sg.B('Mejores puntajes', size=(25, 2), key="-puntajes-")],
        [sg.T(' '),sg.B('Salir', size=(25, 2), key="-salir-")],
        [sg.T(' '),sg.T("  ", size=(17, 1), justification="center",)]
        ]

    window = sg.Window("ScrabbleAR - Menu", layout)
    
    while True:
        event, _value = window.read()
        if event == None:
            sg.popup('psicopata')
            break
        elif event == "-salir-":
            if salir():
                break
            else:
                pass

        elif event in "-nueva-":
            with open('configuraciones.json','r', encoding='UTF-8') as f:
                configs =json.load(f)
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
        
    window.close()


    

if __name__ == "__main__":
    #configuracion= {'dificultad': 'Facil', 'tiempo': 30}
    #config(configuracion)
    pantalla_inicial()
    #temporizador(2)
    # with open('configuraciones.json','r', encoding='UTF-8') as f:
    #     configs =json.load(f)
    #     configurar(configs)