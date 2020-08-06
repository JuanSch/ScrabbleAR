import platform
import operator
import random
import json
import PySimpleGUI as sg
from functools import reduce
from itertools import chain
from bisect import insort


def reglas():
    try:
        with open('Reglas.txt', encoding='UTF-8') as f:
            reglas = f.read()
    except FileNotFoundError:
        reglas = "Ocurrió un error al cargar el archivo"
    try:
        with open('Configurar.txt', encoding='UTF-8') as f:
            configurar = f.read()
    except FileNotFoundError:
        configurar = "Ocurrió un error al cargar el archivo"
    try:
        with open('README.md', encoding='UTF-8') as f:
            readme = f.read()
    except FileNotFoundError:
        readme = "Ocurrió un error al cargar el archivo"    

    layout = [[sg.Text('Reglas de Scrabble AR')],
            [sg.Output(size=(35,10), key='-OUTPUT-')],
            [sg.Button('Reglas'),sg.Button('Como configurar'),sg.Button('Informacion adicional')],
            [sg.Button('Volver')]]
    window = sg.Window('', layout)

    while True:
        event, _ = window.read()
        if event in [None, 'Volver']:
            break
        if event in 'Reglas':
            window['-OUTPUT-'].update(reglas)
        if event in 'Como configurar':
            window['-OUTPUT-'].update(configurar)   
        if event in 'Informacion adicional':
            window['-OUTPUT-'].Update(readme)
    window.close()


def top10(dificultad=None):
    """
    Genera una ventana que se actualiza con el top ten de mejores puntajes 
    la ventana tiene 3 botones facil, medio, dificil, al precionarlo actualiza el output 
    """
    try: 
        with open('valores_puntajes.json', 'r', encoding='UTF-8') as f:
            dic = json.load(f)
            if dificultad is None:
                top = dic['top10']
            else: 
                top = dic['top10'][dificultad]
    except FileNotFoundError:
        dic = crear_valores_puntajes()
        with open('valores_puntajes.json', 'w', encoding='UTF-8') as f:
                json.dump(dic, f, indent=4)
        if dificultad is None:
            top = dic['top10']
        else: 
            top = dic['top10'][dificultad]

    if dificultad is None:
        texto_facil = ""
        texto_medio = ""
        texto_dificil = ""
        i = 1
        for elemento in top['Facil']:  # Forma el string por la dificultad
            if elemento[0] != "None":
                texto_facil += str(i)+'° puesto: ' + elemento[0] + ' con ' + str(elemento[1]) + 'punto/s' + '\n'
                i += 1
        if texto_facil == "":
            texto_facil = 'No hay registro de puntajes'

        i = 1
        for elemento in top['Medio']:  # Forma el string por la dificultad
            if elemento[0] != "None":
                texto_medio += str(i)+'° puesto: ' + elemento[0] + ' con ' + str(elemento[1]) + 'punto/s' + '\n'
                i += 1
        if texto_medio == "":
            texto_medio = 'No hay registro de puntajes'

        i = 1
        for elemento in top['Dificil']:  # Forma el string por la dificultad
            if elemento[0] != "None":
                texto_dificil += str(i)+'° puesto: ' + elemento[0] + ' con ' + str(elemento[1]) + 'punto/s' + '\n'
                i += 1
        if texto_dificil == "":
            texto_dificil = 'No hay registro de puntajes'

        layout = [[sg.Text('TOP ten de puntajes')],
            [sg.Output(size=(35,10), key='-OUTPUT-')],
            [sg.Button('Facil'),sg.Button('Medio'),sg.Button('Dificil')],
            [sg.Button('Volver')]]
        window = sg.Window('', layout)

        while True:
            event, _ = window.read()
            if event in [None, 'Volver']:
                break
            if event in 'Facil':
                window['-OUTPUT-'].update(texto_facil)
            if event in 'Medio':
                window['-OUTPUT-'].update(texto_medio)
            if event in 'Dificil':
                window['-OUTPUT-'].update(texto_dificil)                
        window.close()
    else:
        i = 1
        texto = ""
        for elemento in top['Dificil']:  # Forma el string por la dificultad
            if elemento[0] != "None":
                texto += str(i)+'° puesto: ' + elemento[0] + ' con ' + str(elemento[1]) + 'punto/s' + '\n'
                i += 1
        if texto == "":
            texto = 'No hay registro de puntajes'

        layout = [[sg.Text('TOP ten de puntajes')],
                  [sg.Output(size=(35,10), key='-OUTPUT-')],
                  [sg.Button('Salir')]]
        window = sg.Window('', layout)
        condicion = True
        while True:
            event, _ = window.read(timeout=30)
            if event in [None, 'Salir']:
                break
            elif condicion:
                window['-OUTPUT-'].update(texto)
                condicion = False


def ruta():
    """
    Evalúa en qué sistema operativo se está ejecutando el programa
    y retorna el caracter que este emplea como separador de jerarquía
    en las rutas de archivos.
    """

    if platform.system() != "Windows":
        char = '/'
    else:
        char = '\\'
    return char


#####################################################################
#                         INICIO CLASE FICHA                        #
#####################################################################

class Ficha:
    """
    Representa una ficha del juego.

    Atributos:
        letra: (char) la letra que representa la ficha
        valor: (int) el puntaje que corresponde a la letra
        select: (bool) si la ficha está seleccionada o no
    La correspondencia de letras y valores debe estar definida
    por fuera de la clase

    Metodos:
        __init__: constructor
        getvalor: getter para el atributo valor
        getimagen: retorna la ruta de imagen de la ficha
        cambiarselect: modifica el estado de selección de la ficha
    """

    def __init__(self, letra, valor):
        """
        Constructor de la ficha.

        Recibe:
            letra: (char) la letra que representará la ficha
            valor: (int) el puntaje que corresponde a la letra,
            predefinido de forma externa a esta clase

        El atributo select siempre se inicializará en False
        """
        self.letra = letra
        self.valor = valor
        self.select = False

    def getvalor(self):
        """Getter para el atributo valor."""
        return self.valor

    def getimagen(self):
        """
        Evalúa el estado de selección de la ficha
        y retorna la ruta de imagen que corresponda al mismo.
        """
        if self.select:
            return f'imagenes{ruta()}{self.letra.upper()}click.png'
        else:
            return f'imagenes{ruta()}{self.letra.upper()}.png'

    def cambiarselect(self):
        """Cambia el estado del atributo select."""
        self.select = not self.select

#####################################################################
#                          FIN CLASE FICHA                          #
#####################################################################


#####################################################################
#                        INICIO CLASE CASILLA                       #
#####################################################################

class Casilla:
    """
    Representa una casilla del tablero.

    Atributo global:
        valores: (dict) diccionario con las actitudes correspondientes
        a cada tipo de casilla al momento de evaluar el valor
        de la ficha que contienen (ver metodo valor)

    Atributos:
        pos: (tuple) coordenadas del tablero en las que se encuentra
        tipo: (str) indicador del tipo de ficha
        ocupado: (bool) indicador de presencia de una ficha,
        una casilla se da por ocupada luego de confirmada la palabra
        ficha: (class Ficha) ficha asignada a la casilla,
        las fichas sólo se asignan una vez que se confirmó la palabra
        (ver class Palabra)

    Metodos:
        __init__: constructor
        getpos: getter para el atributo pos
        getestado: getter para el atributo estado
        getimagen: retorna la imagen que corresponda a la posición
        que ocupa la casilla en el tablero
        ocupar: confirma la ocupación de la casilla por una ficha
        valor: calcula el valor de la ficha según el tipo de casilla
    """

    valores = {'': lambda x: x,
               '2L': lambda x: x*2,
               '3L': lambda x: x*3,
               '-3': lambda x: x-3,
               '3P': 3,
               '2P': 2
               }

    def __init__(self, pos, tipo=''):
        """
        Constructor de la casilla.

        Recibe:
            pos: (tuple) un par ordenado de enteros que representa
            las coordenadas del tablero en las que se ubica la casilla
            tipo: (str) indicador del tipo de ficha:
                '': común, no modifica el puntaje de ninguna forma
                '2L', '3L': duplica y triplica el puntaje
                de la letra respectivamente
                '-3': resta 3 puntos al valor de la letra
                '2P', '3P': duplica y triplica el puntaje
                de la palabra respectivamente

        El atributo select siempre se inicializará en False,
        y ficha siempre comenzará vacío
        """
        self.pos = pos
        self.tipo = tipo
        self.ocupado = False
        self.ficha = None

    def getpos(self):
        """Getter para el atributo pos."""
        return self.pos

    def getestado(self):
        """Getter para el atributo estado."""
        return self.ocupado

    def getimagen(self, resalte=False):
        """
        Retorna la imagen que corresponda a la posición que ocupa
        la casilla en el tablero.

        Recibe:
            resalte (keyword arg): (bool) default False
            indica si la casilla debe presentar su porde resaltado o no

        Retorna:
            (str) una ruta de archivo
        """
        if self.ficha is not None:
            return self.ficha.getimagen()
        else:
            return f'imagenes{ruta()}casilla{self.tipo}' \
                   f'{"P" if resalte else ""}.png'

    def ocupar(self, ficha):
        """
        Concreta la ocupación de la casilla.

        Recibe:
            ficha: (class Ficha) un objeto ficha

        Guarda la ficha que recibe, se da por ocupada la casilla
        y se deselecciona la ficha (si lo estaba)
        """
        self.ocupado = True
        self.ficha = ficha
        self.ficha.select = False

    def valor(self):
        """
        Evalúa el tipo de casilla y el valor de la ficha,
        retornando el valor final y un modificador de palabra.

        Retorna:
            valor: (int) el puntaje que resulta de operar el valor
            de la ficha que contiene la casilla con el modificador
            de esta última (*1, *2, *3, -3)
            (int): un valor por el que se debe multiplicar la palabra
            una vez sumados todos los valores de las letras.
        """
        try:
            valor = Casilla.valores[self.tipo](self.ficha.getvalor())
            return valor, 1
        except TypeError:
            valor = self.ficha.getvalor()
            return valor, Casilla.valores[self.tipo]


#####################################################################
#                          FIN CLASE CASILLA                        #
#####################################################################


#####################################################################
#                         INICIO CLASE PALABRA                      #
#####################################################################

class Palabra:
    """
    Representa la palabra que está armando el jugador.

    Es una clase de transferencia de datos entre el atril y el tablero
    El control de que las fichas se vayan colocando en línea
    sucede por fuera de la palabra (ver clase Tablero)

    Atributos:
        min: (tuple) posición del tablero en la que se encuentra
        la primera letra de la palabra
        max: (tuple) posición del tablero en la que se encuentra
        la ultima letra de la palabra
        eje: (int) indica la orientación de la palabra
            0 = horizontal
            1 = vertical
            se corresponden con la posición del eje de desplazamiento
            en las tuplas de coordenadas (x, y)
            que emplea este código
        fichas: (dict) diccionario de pos: ficha, origen
        para todas las fichas que componen la palabra

    Metodos:
        __init__: constructor
        __str__: genera la cadena que componen las fichas
        getposiciones: lista las claves del atributo fichas
        posficha: evalúa si un valor de posición de atril
        concuerda con los guardados en fichas
        agregarletra: agrega una ficha a fichas
        cambiarletra: intercambia una ficha nueva
        por otra preexistente
        modificar: administra el ingreso y egreso de fichas
        a la palabra
        vaciar: retorna la palabra al estado inicial
        probar: evalúa si la palabra es susceptible
        de ser evaluada
    """

    def __init__(self):
        """
        Constructor de la clase, todos los argumentos
        se inicializan vacíos
        """
        self.min = None
        self.max = None
        self.eje = None
        self.fichas = {}

    def __str__(self):
        """
        Retorna la cadena (str) que componen las letras
        de las fichas en orden de lectura (occidental)
        """
        return ''.join(val[1][0].letra for val in self.fichas.items())

    def getposiciones(self):
        """
        Retorna:
            (list): la lista de posiciones que ocupan las fichas
            que componen la palabra
        """
        return list(self.fichas.keys())

    def posficha(self, atril):
        """
        Busca si el valor de atril que recibe está
        entre los que conforman la palabra en curso.

        Recibe:
            atril: (str) el nombre de una posición en el atril
            (ver class Atril)

        Retorna:
            pos: (tuple) o (None) Si el valor que recibe existe
            lo está devuelve la posición de la ficha en el tablero,
            en caso contrario devuelve None
        """
        pos = None
        for k, v in self.fichas.items():
            if v[1] == atril:
                pos = k
        return pos

    def agregarletra(self, pos, ficha, origen):
        """
        Agrega una ficha en una posición no ocupada.

        Recibe:
            pos: (tuple) posición en el tablero
            donde se colocara la ficha
            origen: (str) el nombre de una posición en el atril
            (ver class Atril)
            ficha: (class Ficha) la ficha que se desea colocar

        Cada vez que pase de 1 a 2 fichas evaluará el eje
        en el que se extiende la palabra (ver class Palabra)
        Siempre que haya más de un elemento ordenará self.fichas
        según el orden de lectura (occidental)
        """
        # agrega la ficha al diccionario
        self.fichas[pos] = (ficha, origen)
        longitud = len(self.fichas)
        if longitud == 1:
            # es el primer eelemento agregado a la palabra
            # se inicializan todos los atributos posicionales
            # con el mismo valor
            self.min = self.max = pos
        else:
            posiciones = self.getposiciones()
            # con sólo 2 posiciones ya se puede definir el eje, y no es
            # necesario reevaluarlo por cada nuevo elemento
            if longitud == 2:
                x = pos[0]
                # Si el valor de x en el elemento preexistente es igual
                # al del elemento insertado, significa que los desplazamientos
                # suceden a lo largo del eje y, el valor en el índice [1]
                # de la tupla de coordenadas, en caso contrario
                # puede asegurarse lo opuesto
                if posiciones[0][0] == x:
                    self.eje = 1
                else:
                    self.eje = 0
            # para facilitar operaciones, el diccionario siempre se ordena
            self.fichas = dict(sorted(self.fichas.items(),
                                      key=lambda kv: kv[0][self.eje]))
            evaluar = pos[self.eje]
            # se debe evaluar si hubo un cambio en la posición de min o max,
            # las precondiciones evitan que puedan suceder ambos a la vez
            if evaluar < self.min[self.eje]:
                self.min = pos
            elif evaluar > self.max[self.eje]:
                self.max = pos

    def cambiarletra(self, pos, ficha, origen):
        """
        Permite hacer tanto hacer un intercambio de fichas
        como sólo eliminar una ficha preexistente.

        Evalúa si recibe efectivamente una ficha
        con la que reemplazar la eliminada, y retorna
        siempre el lugar del atril del que salió
        esta última (igual origen) (ver class Atril)

        Recibe:
            pos: (tuple) posición en el tablero
            donde se realizará el intercambio
            origen: (str) el nombre de una posición en el atril
            (ver class Atril) o (None) si no se agrega una ficha nueva
            ficha: (class Ficha) la ficha que se desea colocar
            o (None) si solo se desea eliminar una ficha
            de la palabra

        Retorna:
            (str) el nombre de la posición en el atril
            de la que se originó la ficha eliminada
            (ver class Atril)
        """
        devolver = self.fichas[pos][1]
        if ficha is None:  # en este caso se elimina el elemento
            del self.fichas[pos]
            # debe evaluarse si la palabra quedó vacía, si es así vuelve
            # los valores posicionales a None
            if len(self.fichas) == 0:
                self.min = None
                self.max = None
                self.eje = None
            # en caso contrario debe revisarse si se eliminó alguno
            # de los extremos, en cuyo caso debe recalcularse
            else:
                claves = list(self.fichas.keys())
                if pos == self.max:
                    self.max = claves[-1]
                elif pos == self.min:
                    self.min = claves[0]
                # si la palabra pasó a tener un sólo elemento,
                # el valor de eje vuelve a None
                if len(self.fichas) == 1:
                    self.eje = None
        else:
            self.fichas[pos] = (ficha, origen)
        return devolver

    def modificar(self, pos, ficha=None, origen=None):
        """
        Llama a los módulos agregarletra o cambiarletra
        según resulte necesario para los valores recibidos.

        Recibe:
            pos: (tuple) (tuple) posición en el tablero
            donde se realizará la modificación
            Keyword args:
            origen: (str) el nombre de una posición en el atril
            (ver class Atril) - default None = eliminar ficha
            ficha: (class Ficha) la ficha que se desea colocar
            default default None = eliminar ficha

        Retorna:
            devolver: (str) el nombre de la posición en el atril
            de la que se origina la ficha a devolver (ver class Atril)
            o (None) si no hay ficha para devolver
        """
        if pos in self.fichas:
            devolver = self.cambiarletra(pos, ficha, origen)
            return devolver
        else:
            self.agregarletra(pos, ficha, origen)
            return None

    def vaciar(self):
        """Retorna la palabra a su estado inicial."""
        self.min = None
        self.max = None
        self.eje = None
        self.fichas = {}

    def probar(self):
        """
        Evalúa si la palabra tiene más de dos fichas
        y todas ellas son contiguas.
        """
        ok = False
        if self.eje is not None:
            if (self.max[self.eje] + 1 - self.min[self.eje]
                    == len(self.fichas)):
                ok = True
        return ok

#####################################################################
#                          FIN CLASE PALABRA                        #
#####################################################################


#####################################################################
#                         INICIO CLASE TABLERO                      #
#####################################################################

class Tablero:
    """
    Representa el tablero de juego.

    Es la interfaz entre la GUI y la lógica subyacente a los eventos
    que sucedan en el tablero.

    Atributos:
        xy: (tuple(int, int)) la cantidad de columnas y filas
        que componen el tablero
        matriz: (list(list(class Casilla))) matriz de casillas
        cuyos índices [x] [y] se corresponden con sus posiciones
        en el tablero, siendo (x=0,y=0) la casilla superior izquierda
        posibles: (list(tuple(int, int))) contiene las posiciones
        de todas las casillas que no se encuentran ocupadas
        (ver clase Casilla)

    Metodos:
        __init__: constructor
        getmatriz: getter para el atributo matriz
        getxy: getter para el atributo xy
        getposibles: getter para el atributo posibles
        getcasilla: retorna la casilla que se encuentra
        en una posición determinada de la matriz
        getvalidos: evalúa qué casillas se encuentran desocupadas
        limite: evalúa cuantas casillas contiguas están desocupadas
        en una determinada línea y orientación, con un máximo de 6
        jugada: efectúa las modificaciones de atributos
        y de la palabra que surjan de una acción en el tablero
        fijar_palabra: confirma la colocación de una palabra
        en el tablero
    """

    def __init__(self, columnas, filas, casillas):
        """
        Constructor de la clase.

        Genera la matriz de casillas inicializándolas según su tipo,
        y genera el estado inicial de los demás argumentos.
        El atributo posibles se inicializa con la lista completa
        de posiciones que coforman el tablero

        Recibe:
            columnas: (int) cantidad de columnas de la matriz
            filas: (int) cantidad de filas de la matriz
            casillas: (dict) diccionario de coordenadas del tablero
            con tipos de casilla como clave
        """
        self.xy = (columnas, filas)
        matriz = []
        posibles = []
        for y in range(filas):
            linea = []
            for x in range(columnas):
                pos = (x, y)
                ok = False
                for key in casillas.keys():
                    if list(pos) in casillas[key]:
                        casilla = Casilla(pos, key)
                        ok = True
                        break
                if not ok:
                    casilla = Casilla(pos)
                posibles.append(pos)
                linea.append(casilla)
            matriz.append(linea)
        self.matriz = matriz
        self.posibles = posibles

    def getmatriz(self):
        """Getter para el atributo matriz"""
        return self.matriz

    def getxy(self):
        """Getter para el atributo xy"""
        return self.xy

    def getposibles(self):
        """Getter para el atributo posibles"""
        return self.posibles

    def getcasilla(self, pos):
        """
        Retorna el objeto casilla que se encuentra en la posición
        que recibe como parámetro

        Recibe:
            pos: (tuple(int, int)) par ordenado de coordenadas
            que representan una posición en el tablero

        Retorna:
            casilla: (class Casilla) un objeto de tipo casilla
            en el estado que se encuentre
        """
        x, y = pos
        casilla = self.matriz[y][x]
        return casilla

    def getvalidos(self):
        """
        Evalúa qué posiciones de la matriz
        contienen casillas desocupadas

        Retorna:
            validos: (list(tuple(int,int))) las posiciones de la matriz
            que contienen casillas desocupadas
        """
        validos = []
        for x in range(self.xy[0]):
            for y in range(self.xy[1]):
                pos = (x, y)
                if not self.getcasilla(pos).getestado():
                    validos.append(pos)
        return validos

    def limite(self, pos, posibles, eje, borde, direccion, lim=7, ciclo=0):
        """
        Método recursivo:
        Dados un punto de inicio, eje, direccion y longitud maxima,
        devuelve una lista de casillas contiguas no ocupadas
        dentro de los confines del tablero.

        Recibe:
            pos: tupla (int, int) indicando una posición válida
            en la matriz de casillas del tablero
            posibles: (list) lista de posiciones (ver pos), la casilla inicial
            se preasume desocupada y ya parte de la lista, la función
            no la incorpora
            eje: (int) indica la dirección del recorrido
                 0 = recorrido horizontal
                 1 = recorrido vertical
            dirección: '-' (str)= búsqueda hacia la izquierda o hacia arriba
                                  de la posición inicial
                       '+' (str)= búsqueda hacia la derecha o hacia abajo
                                 de la posición inicial
            Keyword args:
            lim: (int) la cantidad máxima de espacios a evaluar
            (incluyendo la posición inicial) default = 7
            ciclo: (int) indicador de cuántas iteraciones se realizaron
            default = 0

        Retorna:
            posibles: un append a posibles (ver recibe) de las casillas
            que no estaban ocupadas
        """

        direcciones = {'+': operator.add, '-': operator.sub}
        direc = direcciones[direccion]
        if ciclo == lim-1:
            return posibles
        else:
            nueva = list(pos)
            coord = direc(pos[eje], 1)
            nueva[eje] = coord
            if nueva[eje] == borde or self.getcasilla(nueva).getestado():
                return posibles
            else:
                posibles.append(tuple(nueva))
                return self.limite(nueva, posibles, eje, borde, direccion,
                                   lim, ciclo + 1)

    def jugada(self, palabra, pos, origen=None, ficha=None):
        """
        Método principal de lógica interna del tablero, debe recibir
        un objeto tipo palabra, y manejará las actualizaciones
        correspondientes a los estados de las casillas
        """

        def habilitados(posibles, eje, izquierda, derecha):
            bordes = self.getxy()
            self.limite(derecha, posibles, eje, -1, '-')
            self.limite(izquierda, posibles, eje, bordes[eje], '+')

        devolver = palabra.modificar(pos, ficha, origen)
        anteriores = list(self.posibles)
        marcar = []
        if devolver is not None and palabra.min is None:
            borrar = anteriores
            self.posibles = self.getvalidos()
        else:
            posibles = []
            eje = palabra.eje
            min = palabra.min
            if eje is None:
                habilitados(posibles, 0, min, min)
                habilitados(posibles, 1, min, min)
                posibles.append(min)
            else:
                max = palabra.max
                habilitados(posibles, eje, min, max)
            self.posibles = set(posibles)
            borrar = list(set(anteriores)-self.posibles)
            marcar = list(self.posibles)
        # Con esto garantizamos que no se marquen como posibles
        # casillas en las que hay una ficha
        # de la palabra en construcción
        for k, _v in palabra.fichas.items():
            if k in marcar:
                marcar.remove(k)
        return marcar, borrar, devolver

    def fijar_palabra(self, palabra):
        """
        Concreta la colocación de la palabra en el tablero.
        Ocupa las casillas, y deseleciona las fichas correspondientes.
        Calcula el puntaje total de la palabra según el valor de
        cada ficha y el tipo de casilla en el que está ubicada
        """
        def calcular(ficha1, ficha2):
            puntos = ficha1[0] + ficha2[0]
            multi = ficha1[1] * ficha2[1]
            return puntos, multi

        valores = []
        for k, v in palabra.fichas.items():
            ficha = v[0]
            casilla = self.getcasilla(k)
            casilla.ocupar(ficha)
            valores.append(casilla.valor())
        valor = reduce(lambda x, y: x*y, reduce(calcular, valores))
        self.posibles = self.getvalidos()
        return valor

#####################################################################
#                         FIN CLASE TABLERO                         #
#####################################################################


#####################################################################
#                         INICIO CLASE ATRIL                        #
#####################################################################

class Atril:
    """
    Representa un atril.
    Tiene diferentes estados según la jugada que se desee hacer.
    Contiene diccionario de fichas con el nombre del espacio
    que cada una de estas ocupa como clave, un indicador de estado,
    una lista de los espacios vacíos y un atributo cambiar,
    que sirve para realizar intercambios con la palabra o con la bolsa

    APAGADO: implica que cualquier acción que suceda en el atril
    será ignorada
    CAMBIAR: es el estado de intercambio de fichas con la bolsa
    ELEGIR y PASAR: son los estados de intercambio de fichas
    con la palabra en formación en el tablero.
    """
    estados = {0: 'APAGADO', 1: 'ELEGIR', 2: 'PASAR', 3: 'CAMBIAR'}

    def __init__(self, inicio='F'):
        fichas = {}
        vacias = []
        for i in range(7):
            nombre = f'{inicio}{i}'
            fichas[nombre] = None
            vacias.append(nombre)
        self.vacias = vacias
        self.fichas = fichas
        self.cambiar = []
        self.estado = Atril.estados[0]

    def setestado(self, valor):
        """Modifica el estado del atril."""
        self.estado = Atril.estados[valor]
        if valor in (1, 3):
            self.cambiar = []

    def imagen(self, espacio):
        """
        Devuelve la imagen que corresponde
        según si hay o no una ficha
        """
        if self.fichas[espacio] is None:
            return f'imagenes{ruta()}Atril.png'
        else:
            return self.fichas[espacio].getimagen()

    def click(self, evento):
        """
        Se encarga de hacer las modificaciones pertinentes
        a los atributos según el estado del atril:
        CAMBIAR: permite seleccionar y deseleccionar tantas
        fichas como haya en el atril, agregándolas a self.cambiar
        ELEGIR: permite seleccionar o deseleccionar
        de a una ficha por vez, agregándola o quitándola
        de self.cambiar, con una referencia a su espacio
        de origen en el atril (ver clase Palabra)
        PASAR: permite la deselección o cambio de fichas,
        vaciando o cambiando el valor de self.cambiar
        según sea necesario
        """
        ficha = self.fichas[evento]
        if self.estado == 'CAMBIAR':
            # Se seleccionarán tantas fichas como se desee intercambiar
            # con la bolsa
            if not ficha.select:
                self.cambiar.append(ficha)
            else:
                self.cambiar.remove(ficha)
            ficha.cambiarselect()
        elif self.estado == 'ELEGIR':
            # Se seleccionará una ficha para colocar en el tablero
            # o se deselccionará una ya colocada
            if not ficha.select:
                # Si la ficha no estaba seleccionada, siginifica que se eligió
                # una para colocar en el tablero, se cambia el estado
                # del atril a 'PASAR'
                self.setestado(2)
            ficha.cambiarselect()
            self.cambiar = (evento, ficha)
        elif self.estado == 'PASAR':
            # Se deseleccionará la ficha en curso, se seleccionará otra
            # o se reemplazará una fichas del tablero
            if evento == self.cambiar[0]:
                # Se hizo click en la ficha que ya estaba seleccionada
                # para colocar en el tablero
                self.cambiar = []
                ficha.cambiarselect()
                self.setestado(1)
            elif not ficha.select:
                # Se decidió cambiar qué ficha se iba a colocar en el tablero
                self.cambiar[1].cambiarselect()
                self.cambiar = (evento, ficha)
                ficha.cambiarselect()
            else:
                # Se cambió una ficha ya colocada en el tablero por otra
                ficha.cambiarselect()
                self.setestado(1)

    def deseleccion(self):
        """Deselecciona todas las fichas que están en el atril"""
        for _k, v in self.fichas.items():
            if v.select:
                v.cambiarselect()
        self.cambiar = []

    def pedir(self):
        return len(self.vacias)

    def recibir(self, lista):
        """
        Guarda las fichas que reciba en self.fichas

        Recibe:
            lista: debe ser una lista de tuplas (letra,valor) -el formato
            de salida de la clase 'bolsa'-, las convierte en fichas
            y las almacena en los casilleros libres. La función asume
            que siempre se recibirá la cantidad requerida de fichas para
            llenar el atril. Esto implica que la condición de fin 'no hay
            fichas suficientes' debe resolverse antes de esta instancia
        """

        for i in range(len(lista)):
            letra = lista[i][0]
            valor = lista[i][1]
            ficha = Ficha(letra, valor)
            self.fichas[self.vacias[i]] = ficha
        self.vacias = []

    def entregar(self):
        """Retorna las fichas que el usuario desea cambiar"""

        for k, v in self.fichas.items():
            if v.select:
                self.fichas[k] = None
                self.vacias.append(k)
        return self.cambiar

    def eliminar(self, origen):
        """Vacía las posiciones indicadas por origen"""
        for v in origen:
            self.fichas[v] = None
            self.vacias.append(v)


class AtrilIA(Atril):
    """
    Clase hija de Atril, sus únicas diferencias con el padre son:
    se inicializa en estado CAMBIAR (las manipulaciones de fichas
    se simulan por fuera de la estructura del atril).
    las posiciones de self.fichas comienzan con 'IA' ('F' en el padre)
    para todas las fichas devolverá la misma imagen ('?')
    """
    def __init__(self):
        Atril.__init__(self, inicio='IA')
        self.estado: Atril.estados[3]

    def imagen(self, espacio):
        if self.fichas[espacio] is None:
            return f'imagenes{ruta()}Atril.png'
        else:
            return f'imagenes{ruta()}FichaIA.png'


#####################################################################
#                           FIN CLASE ATRIL                         #
#####################################################################


#####################################################################
#                         INICIO CLASE BOLSA                        #
#####################################################################
class Bolsa:
    """
    Clase de control de bolsa de fichas, contiene una lista de letras
    con tantas letras como fichas por letra haya disponibles
    y otra con un diccionario letra: valor.
    El formato de salida de las fichas es [(letra, valor)*letras a entregar]
    """

    def __init__(self, letras, valores):
        fichas = list(map(lambda x: [x[0]]*x[1], letras))
        self.fichas = list(chain.from_iterable(fichas))
        self.valores = valores

    def entregar(self, cant):
        """
        Recibe una cantidad (int) de fichas a entregar.
        Genera [(letra, valor)*cantidad] seleccionando letras al azar
        de la bolsa y eliminándolas.
        Si hay menos letras en la bolsa que cant, devolverá una lista
        vacía.
        """
        entregar = []
        if len(self.fichas) >= cant:
            for _i in range(cant):
                pos = random.randrange(len(self.fichas))
                letra = self.fichas[pos]
                self.fichas.pop(pos)
                valor = self.valores[letra]
                ficha = (letra, valor)
                entregar.append(ficha)
        return entregar

    def intercambiar(self, fichas):
        """
        Recibe una lista de fichas [(letra, valor)*cant].
        Reincorpora las letras a la bolsa, y entrega nuevamente
        tantas como haya recibido.
        Para la reincorporación se emplea bisect.insort()
        (inserción ordenada) para evitar la posible acumulación
        de letras indseadas al final de la lista que surgirían
        de un lista.append()
        """

        lista = list(map(lambda x: x.letra, fichas))
        for letra in lista:
            insort(self.fichas, letra)
        return self.entregar(len(lista))

#####################################################################
#                         FIN CLASE BOLSA                        #
#####################################################################


def crear_valores_puntajes():
    valores_puntajes = {
        "puntos_letra": {
            "a": 1,
            "b": 3,
            "c": 3,
            "d": 2,
            "e": 1,
            "f": 4,
            "g": 2,
            "h": 4,
            "i": 1,
            "j": 8,
            "k": 8,
            "l": 1,
            "m": 3,
            "n": 1,
            "\u00f1": 8,
            "o": 1,
            "p": 3,
            "q": 5,
            "r": 1,
            "s": 1,
            "t": 1,
            "u": 1,
            "v": 4,
            "w": 10,
            "x": 8,
            "y": 4,
            "z": 1
        },
        "Facil": {
            "tablero": {
                "dimensiones": [
                    16,
                    16
                ],
                "2L": [
                    [
                        2,
                        0
                    ],
                    [
                        14,
                        0
                    ],
                    [
                        0,
                        1
                    ],
                    [
                        6,
                        1
                    ],
                    [
                        12,
                        1
                    ],
                    [
                        3,
                        2
                    ],
                    [
                        9,
                        2
                    ],
                    [
                        15,
                        2
                    ],
                    [
                        1,
                        3
                    ],
                    [
                        13,
                        3
                    ],
                    [
                        2,
                        6
                    ],
                    [
                        14,
                        6
                    ],
                    [
                        1,
                        9
                    ],
                    [
                        13,
                        9
                    ],
                    [
                        2,
                        12
                    ],
                    [
                        14,
                        12
                    ],
                    [
                        0,
                        13
                    ],
                    [
                        6,
                        13
                    ],
                    [
                        12,
                        13
                    ],
                    [
                        3,
                        14
                    ],
                    [
                        9,
                        14
                    ],
                    [
                        15,
                        14
                    ],
                    [
                        1,
                        15
                    ],
                    [
                        13,
                        15
                    ]
                ],
                "3L": [
                    [
                        7,
                        0
                    ],
                    [
                        8,
                        3
                    ],
                    [
                        3,
                        4
                    ],
                    [
                        9,
                        4
                    ],
                    [
                        15,
                        4
                    ],
                    [
                        7,
                        6
                    ],
                    [
                        3,
                        7
                    ],
                    [
                        9,
                        7
                    ],
                    [
                        15,
                        7
                    ],
                    [
                        0,
                        8
                    ],
                    [
                        6,
                        8
                    ],
                    [
                        12,
                        8
                    ],
                    [
                        8,
                        9
                    ],
                    [
                        0,
                        11
                    ],
                    [
                        7,
                        11
                    ],
                    [
                        12,
                        11
                    ],
                    [
                        7,
                        12
                    ],
                    [
                        8,
                        15
                    ]
                ],
                "2P": [
                    [
                        5,
                        0
                    ],
                    [
                        11,
                        0
                    ],
                    [
                        4,
                        3
                    ],
                    [
                        10,
                        3
                    ],
                    [
                        0,
                        4
                    ],
                    [
                        6,
                        4
                    ],
                    [
                        12,
                        4
                    ],
                    [
                        3,
                        5
                    ],
                    [
                        9,
                        5
                    ],
                    [
                        15,
                        5
                    ],
                    [
                        5,
                        6
                    ],
                    [
                        11,
                        6
                    ],
                    [
                        4,
                        9
                    ],
                    [
                        10,
                        9
                    ],
                    [
                        0,
                        10
                    ],
                    [
                        6,
                        10
                    ],
                    [
                        12,
                        10
                    ],
                    [
                        3,
                        11
                    ],
                    [
                        9,
                        11
                    ],
                    [
                        15,
                        11
                    ],
                    [
                        5,
                        12
                    ],
                    [
                        11,
                        12
                    ],
                    [
                        4,
                        15
                    ],
                    [
                        10,
                        15
                    ]
                ],
                "3P": [
                    [
                        1,
                        0
                    ],
                    [
                        8,
                        0
                    ],
                    [
                        7,
                        3
                    ],
                    [
                        14,
                        3
                    ],
                    [
                        1,
                        6
                    ],
                    [
                        8,
                        6
                    ],
                    [
                        0,
                        7
                    ],
                    [
                        6,
                        7
                    ],
                    [
                        12,
                        7
                    ],
                    [
                        3,
                        8
                    ],
                    [
                        9,
                        8
                    ],
                    [
                        15,
                        8
                    ],
                    [
                        7,
                        9
                    ],
                    [
                        14,
                        9
                    ],
                    [
                        1,
                        12
                    ],
                    [
                        8,
                        12
                    ],
                    [
                        7,
                        15
                    ],
                    [
                        14,
                        15
                    ]
                ],
                "-3": [
                    [
                        2,
                        2
                    ],
                    [
                        13,
                        2
                    ],
                    [
                        2,
                        13
                    ],
                    [
                        13,
                        13
                    ]
                ]
            },
            "bolsa": [
                [
                    "a",
                    12
                ],
                [
                    "e",
                    14
                ],
                [
                    "i",
                    6
                ],
                [
                    "l",
                    5
                ],
                [
                    "n",
                    7
                ],
                [
                    "o",
                    10
                ],
                [
                    "r",
                    6
                ],
                [
                    "s",
                    8
                ],
                [
                    "t",
                    4
                ],
                [
                    "u",
                    5
                ],
                [
                    "d",
                    5
                ],
                [
                    "g",
                    1
                ],
                [
                    "b",
                    2
                ],
                [
                    "c",
                    4
                ],
                [
                    "m",
                    2
                ],
                [
                    "p",
                    2
                ],
                [
                    "f",
                    1
                ],
                [
                    "h",
                    2
                ],
                [
                    "v",
                    1
                ],
                [
                    "y",
                    2
                ],
                [
                    "q",
                    2
                ],
                [
                    "j",
                    1
                ],
                [
                    "\u00f1",
                    1
                ],
                [
                    "x",
                    1
                ],
                [
                    "z",
                    1
                ]
            ]
        },
        "Medio": {
            "tablero": {
                "dimensiones": [
                    15,
                    15
                ],
                "2L": [
                    [
                        3,
                        0
                    ],
                    [
                        11,
                        0
                    ],
                    [
                        6,
                        2
                    ],
                    [
                        8,
                        2
                    ],
                    [
                        0,
                        3
                    ],
                    [
                        7,
                        3
                    ],
                    [
                        14,
                        3
                    ],
                    [
                        2,
                        6
                    ],
                    [
                        6,
                        6
                    ],
                    [
                        8,
                        6
                    ],
                    [
                        12,
                        6
                    ],
                    [
                        3,
                        7
                    ],
                    [
                        11,
                        7
                    ],
                    [
                        2,
                        8
                    ],
                    [
                        6,
                        8
                    ],
                    [
                        8,
                        8
                    ],
                    [
                        12,
                        8
                    ],
                    [
                        0,
                        11
                    ],
                    [
                        7,
                        11
                    ],
                    [
                        14,
                        11
                    ],
                    [
                        6,
                        12
                    ],
                    [
                        8,
                        12
                    ],
                    [
                        3,
                        14
                    ],
                    [
                        11,
                        14
                    ]
                ],
                "3L": [
                    [
                        5,
                        1
                    ],
                    [
                        9,
                        1
                    ],
                    [
                        1,
                        5
                    ],
                    [
                        5,
                        5
                    ],
                    [
                        9,
                        5
                    ],
                    [
                        13,
                        5
                    ],
                    [
                        13,
                        9
                    ],
                    [
                        1,
                        9
                    ],
                    [
                        5,
                        9
                    ],
                    [
                        9,
                        9
                    ],
                    [
                        5,
                        13
                    ],
                    [
                        9,
                        13
                    ]
                ],
                "2P": [
                    [
                        1,
                        1
                    ],
                    [
                        13,
                        1
                    ],
                    [
                        2,
                        2
                    ],
                    [
                        12,
                        2
                    ],
                    [
                        3,
                        3
                    ],
                    [
                        11,
                        3
                    ],
                    [
                        4,
                        4
                    ],
                    [
                        10,
                        4
                    ],
                    [
                        4,
                        10
                    ],
                    [
                        10,
                        10
                    ],
                    [
                        3,
                        11
                    ],
                    [
                        11,
                        11
                    ],
                    [
                        2,
                        12
                    ],
                    [
                        12,
                        12
                    ],
                    [
                        1,
                        13
                    ],
                    [
                        13,
                        13
                    ]
                ],
                "3P": [
                    [
                        0,
                        0
                    ],
                    [
                        7,
                        0
                    ],
                    [
                        14,
                        0
                    ],
                    [
                        0,
                        7
                    ],
                    [
                        14,
                        7
                    ],
                    [
                        0,
                        14
                    ],
                    [
                        7,
                        14
                    ],
                    [
                        14,
                        14
                    ]
                ],
                "-3": [
                    [
                        7,
                        1
                    ],
                    [
                        1,
                        7
                    ],
                    [
                        13,
                        7
                    ],
                    [
                        7,
                        13
                    ]
                ]
            },
            "bolsa": [
                [
                    "a",
                    9
                ],
                [
                    "e",
                    11
                ],
                [
                    "i",
                    4
                ],
                [
                    "l",
                    3
                ],
                [
                    "n",
                    3
                ],
                [
                    "o",
                    6
                ],
                [
                    "r",
                    3
                ],
                [
                    "s",
                    3
                ],
                [
                    "t",
                    3
                ],
                [
                    "u",
                    3
                ],
                [
                    "d",
                    3
                ],
                [
                    "g",
                    2
                ],
                [
                    "b",
                    2
                ],
                [
                    "c",
                    3
                ],
                [
                    "m",
                    1
                ],
                [
                    "p",
                    2
                ],
                [
                    "f",
                    1
                ],
                [
                    "h",
                    2
                ],
                [
                    "v",
                    1
                ],
                [
                    "y",
                    1
                ],
                [
                    "q",
                    1
                ],
                [
                    "j",
                    1
                ],
                [
                    "\u00f1",
                    1
                ],
                [
                    "x",
                    1
                ],
                [
                    "z",
                    1
                ]
            ]
        },
        "Dificil": {
            "tablero": {
                "dimensiones": [
                    17,
                    17
                ],
                "2L": [
                    [
                        3,
                        0
                    ],
                    [
                        13,
                        0
                    ],
                    [
                        4,
                        1
                    ],
                    [
                        0,
                        3
                    ],
                    [
                        16,
                        3
                    ],
                    [
                        1,
                        4
                    ],
                    [
                        7,
                        4
                    ],
                    [
                        8,
                        5
                    ],
                    [
                        4,
                        7
                    ],
                    [
                        5,
                        8
                    ],
                    [
                        11,
                        8
                    ],
                    [
                        12,
                        9
                    ],
                    [
                        8,
                        11
                    ],
                    [
                        9,
                        12
                    ],
                    [
                        15,
                        12
                    ],
                    [
                        0,
                        13
                    ],
                    [
                        16,
                        13
                    ],
                    [
                        12,
                        15
                    ],
                    [
                        3,
                        16
                    ],
                    [
                        13,
                        16
                    ]
                ],
                "3L": [
                    [
                        0,
                        1
                    ],
                    [
                        8,
                        1
                    ],
                    [
                        16,
                        1
                    ],
                    [
                        4,
                        3
                    ],
                    [
                        3,
                        4
                    ],
                    [
                        5,
                        4
                    ],
                    [
                        4,
                        5
                    ],
                    [
                        0,
                        7
                    ],
                    [
                        8,
                        7
                    ],
                    [
                        16,
                        7
                    ],
                    [
                        0,
                        9
                    ],
                    [
                        8,
                        9
                    ],
                    [
                        16,
                        9
                    ],
                    [
                        12,
                        11
                    ],
                    [
                        11,
                        12
                    ],
                    [
                        13,
                        12
                    ],
                    [
                        12,
                        13
                    ],
                    [
                        0,
                        15
                    ],
                    [
                        8,
                        15
                    ],
                    [
                        16,
                        15
                    ]
                ],
                "2P": [
                    [
                        5,
                        0
                    ],
                    [
                        11,
                        0
                    ],
                    [
                        12,
                        1
                    ],
                    [
                        8,
                        3
                    ],
                    [
                        9,
                        4
                    ],
                    [
                        15,
                        4
                    ],
                    [
                        16,
                        5
                    ],
                    [
                        12,
                        7
                    ],
                    [
                        3,
                        8
                    ],
                    [
                        13,
                        8
                    ],
                    [
                        4,
                        9
                    ],
                    [
                        0,
                        11
                    ],
                    [
                        16,
                        11
                    ],
                    [
                        1,
                        12
                    ],
                    [
                        7,
                        12
                    ],
                    [
                        8,
                        13
                    ],
                    [
                        4,
                        15
                    ],
                    [
                        5,
                        16
                    ],
                    [
                        11,
                        16
                    ]
                ],
                "3P": [
                    [
                        1,
                        0
                    ],
                    [
                        7,
                        0
                    ],
                    [
                        9,
                        0
                    ],
                    [
                        15,
                        0
                    ],
                    [
                        12,
                        3
                    ],
                    [
                        11,
                        4
                    ],
                    [
                        13,
                        4
                    ],
                    [
                        12,
                        5
                    ],
                    [
                        1,
                        8
                    ],
                    [
                        7,
                        8
                    ],
                    [
                        9,
                        8
                    ],
                    [
                        15,
                        8
                    ],
                    [
                        4,
                        11
                    ],
                    [
                        3,
                        12
                    ],
                    [
                        5,
                        12
                    ],
                    [
                        4,
                        13
                    ],
                    [
                        1,
                        16
                    ],
                    [
                        7,
                        16
                    ],
                    [
                        9,
                        16
                    ],
                    [
                        15,
                        16
                    ]
                ],
                "-3": [
                    [
                        0,
                        0
                    ],
                    [
                        4,
                        0
                    ],
                    [
                        8,
                        0
                    ],
                    [
                        12,
                        0
                    ],
                    [
                        16,
                        0
                    ],
                    [
                        0,
                        4
                    ],
                    [
                        4,
                        4
                    ],
                    [
                        8,
                        4
                    ],
                    [
                        12,
                        4
                    ],
                    [
                        16,
                        4
                    ],
                    [
                        0,
                        8
                    ],
                    [
                        4,
                        8
                    ],
                    [
                        8,
                        8
                    ],
                    [
                        12,
                        8
                    ],
                    [
                        16,
                        8
                    ],
                    [
                        0,
                        12
                    ],
                    [
                        4,
                        12
                    ],
                    [
                        8,
                        12
                    ],
                    [
                        12,
                        12
                    ],
                    [
                        16,
                        12
                    ],
                    [
                        0,
                        16
                    ],
                    [
                        4,
                        16
                    ],
                    [
                        8,
                        16
                    ],
                    [
                        12,
                        16
                    ],
                    [
                        16,
                        16
                    ]
                ]
            },
            "bolsa": [
                [
                    "a",
                    5
                ],
                [
                    "e",
                    5
                ],
                [
                    "i",
                    2
                ],
                [
                    "l",
                    2
                ],
                [
                    "n",
                    2
                ],
                [
                    "o",
                    4
                ],
                [
                    "r",
                    2
                ],
                [
                    "s",
                    2
                ],
                [
                    "t",
                    2
                ],
                [
                    "u",
                    2
                ],
                [
                    "d",
                    2
                ],
                [
                    "g",
                    1
                ],
                [
                    "b",
                    1
                ],
                [
                    "c",
                    2
                ],
                [
                    "m",
                    1
                ],
                [
                    "p",
                    1
                ],
                [
                    "f",
                    1
                ],
                [
                    "h",
                    2
                ],
                [
                    "v",
                    1
                ],
                [
                    "y",
                    1
                ],
                [
                    "q",
                    1
                ],
                [
                    "j",
                    1
                ],
                [
                    "\u00f1",
                    1
                ],
                [
                    "x",
                    1
                ],
                [
                    "z",
                    1
                ]
            ]
        },
        "Personalizada": {
            "bolsa": [
                [
                    "a",
                    12
                ],
                [
                    "b",
                    12
                ],
                [
                    "c",
                    12
                ],
                [
                    "d",
                    12
                ],
                [
                    "e",
                    8
                ],
                [
                    "f",
                    8
                ],
                [
                    "g",
                    12
                ],
                [
                    "h",
                    4
                ],
                [
                    "i",
                    1
                ],
                [
                    "j",
                    3
                ],
                [
                    "k",
                    8
                ],
                [
                    "l",
                    1
                ],
                [
                    "m",
                    5
                ],
                [
                    "n",
                    1
                ],
                [
                    "\u00f1",
                    5
                ],
                [
                    "o",
                    1
                ],
                [
                    "p",
                    3
                ],
                [
                    "q",
                    5
                ],
                [
                    "r",
                    1
                ],
                [
                    "s",
                    1
                ],
                [
                    "t",
                    1
                ],
                [
                    "u",
                    1
                ],
                [
                    "v",
                    12
                ],
                [
                    "w",
                    10
                ],
                [
                    "x",
                    8
                ],
                [
                    "y",
                    3
                ],
                [
                    "z",
                    1
                ]
            ],
            "dificultad_IA": "Medio",
            "dificultad_Tablero": "Medio",
            "puntos_letra": {
                "a": 12,
                "b": 3,
                "c": 3,
                "d": 2,
                "e": 1,
                "f": 4,
                "g": 2,
                "h": 4,
                "i": 1,
                "j": 8,
                "k": 8,
                "l": 1,
                "m": 3,
                "n": 1,
                "\u00f1": 8,
                "o": 1,
                "p": 3,
                "q": 5,
                "r": 1,
                "s": 1,
                "t": 1,
                "u": 1,
                "v": 4,
                "w": 10,
                "x": 8,
                "y": 4,
                "z": 1
            }
        },
        "top10": {
            "Facil": [
                [
                    "",
                    00
                ],
                [
                    "",
                    0
                ],
                [
                    "",
                    0
                ],
                [
                    "",
                    0
                ],
                [
                    "",
                    0
                ],
                [
                    "",
                    0
                ],
                [
                    "",
                    0
                ],
                [
                    "",
                    0
                ],
                [
                    "",
                    0
                ],
                [
                    "",
                    0
                ]
            ],
            "Medio": [
                [
                    "",
                    0
                ],
                [
                    "",
                    0
                ],
                [
                    "",
                    0
                ],
                [
                    "",
                    0
                ],
                [
                    "",
                    0
                ],
                [
                    "",
                    0
                ],
                [
                    "",
                    0
                ],
                [
                    "",
                    0
                ],
                [
                    "",
                    0
                ],
                [
                    "",
                    0
                ]
            ],
            "Dificil": [
                [
                    "",
                    0
                ],
                [
                    "",
                    0
                ],
                [
                    "",
                    0
                ],
                [
                    "",
                    0
                ],
                [
                    "",
                    0
                ],
                [
                    "",
                    0
                ],
                [
                    "",
                    0
                ],
                [
                    "",
                    0
                ],
                [
                    "",
                    0
                ],
                [
                    "",
                    0
                ]
            ]
        }
        }
    return valores_puntajes
