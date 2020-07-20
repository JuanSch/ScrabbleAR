from pattern.es import lexicon, spelling, parse
from pattern.web import Wiktionary
from ScrabbleAR import top10
from logica import Ficha, Casilla, Palabra, Tablero, Atril
import concurrent.futures
import json

def actualizar_puntajes(tupla):
    """recibe una tupla[0]= nombre de usuario y tupla[1] el puntaje
    si el puntaje entra en el top diez, se lo inserta donde corresponde en orden descendiente de puntajes
    y se elemina el ultimo ya que la lista con el nuevo puntaje insertado tiene 11 elementos"""
    try:
        with open("valores_puntajes.json",'r') as f: #Cargo el diccionario de puntajes
            dic = json.load(f)
    except FileNotFoundError: #si no existe el archivo, lo creo
        #$% crearvalores()
        with open("valores_puntajes.json",'r') as f:
            dic = json.load(f)
    top = dic['top10']
    if (tupla[1] >= top[9][1]): #si el puntaje es mayor o igual al puntaje minimo en el top
        for i in range (10):
            if top(i)[1] > tupla[1]: #busco la posicion a insertar
                top.insert(i,tupla) #inserto (ahora la lista tiene 11 elementos, desde 0 a 10)
                top.pop(10) #remuevo el elemento en la posicion 10, es decir el decimo-primer elemento
                return True
    else: 
        return False


def validar_palabra(palabra):
    """
    Comprueba que el string que se pasa como palabra sea una palabra valida
    retorna True si lo es. Caso contrario retorna False
    """
    palabra = parse(palabra).split('/')
    if palabra[1] in ('AO','JJ','AQ','DI','DT','VAG','VBG','VAI','VAN','MD',
                      'VAS','VMG','VMI','VB','VMM','VMN','VMP','VBN','VMS',
                      'VSG','VSI','VSN','VSP','VSS'): #VB:verbo, JJ:adjetivo
        if palabra[0] not in lexicon.keys():
            # si es adj o verbo y no esta en el lexicon
            # ni el spelling comprueba con wiktionary
            if palabra[0] not in spelling.keys():
                w = Wiktionary(language="es")
                article = w.search(palabra[0])
                if article != None :
                    return True
                else:
                    return  False
            else:
                return True
        else:
            return True
    elif palabra[1] in ('NC','NN','NCS','NCP','NNS','NP','NNP','W'):
        # sustantivo comprueba con wiktionary
        w = Wiktionary(language="es")
        article = w.search(palabra[0])
        if article != None :
            return True
        else:
            return False

def calcular_puntaje(palabra):
    """
    Funcion que calcula el puntaje de la palabra ingresada 
    """
    puntaje = 0
    with open('valores_puntajes.json') as f: #Abro el archivo
        puntajes = json.load(f)
    for char in palabra:
        puntaje += puntajes['puntos_letra'][char] #por cada caracter evaluo cuanto vale y lo sumo al total
    return(puntaje)

def elegir_palabra(Fichas, dificultad,long_maxima = 7):
    def elegir_palabra_dos(Fichas, dificultad, long_maxima):
        """
        Esta funcion Elige la palabra mas adecuada para nuestra IA y así ganar la mayor cantidad de puntos 
        primero se fija que palabras puede armar con sus letras y depues evalua cual es la palabra que más puntaje da
        """
        def sirve(lista_uno,lista_dos):
            """
            Creo un diccionario con key = letra & value = cantidad de apariciones de la key en la lista
            si el diccionario dos tiene las miscas keys que el uno yu el valor del dic_dos en la key es mayor o igual a la del dic_uno, en cada key 
                entonces puedo armar una palabra 
            """
            dic_uno = {}
            dic_dos = {}

            for key in lista_uno: #Genero un diccionario con key = letra y value = cantidad de apariciones
                if key in dic_uno:
                    dic_uno[key] = dic_uno[key] + 1
                else:
                    dic_uno[key] = 1 

            for key in lista_dos:#Genero un diccionario con key = letra y value = cantidad de apariciones
                if key in dic_dos:
                    dic_dos[key] = dic_dos[key] + 1
                else:
                    dic_dos[key] = 1
            
            dic_uno_keys  = [] #Genero una lista de claves del diccionario uno (las letras de la IA)
            for key in dic_uno:
                dic_uno_keys.append(key)

            cumple = False
            for key in dic_dos: #si el diccionario dos tiene las mismas letras que el diccionario uno
                if key in dic_uno_keys:
                    cumple = True
                else:
                    cumple = False
                    break
            condicion = False

            if cumple:
                for key in dic_dos: #si las cantidad de letras de la IA alcanzan para formar la palabra condicion = True
                    if dic_uno[key] >= dic_dos[key]:
                        condicion = True 
                    else:
                        condicion = False
                        break
            return(condicion) 

        def por_dificulad(palabras_utilies, dificultad, puntaje_letra):

            """
            Segun la dificultad elige una u otra palaba
            """
            def dificil(palabras):
                """
                cargo los puntajes y me fijo cual es la palabra que mayor puntaje da 
                """
                max = 0
                palabra_elegida = str
                    
                for palabra in palabras:
                    puntaje_palabra_actual = calcular_puntaje_IA(palabra,puntaje_letra)
                    if puntaje_palabra_actual > max:
                        max = puntaje_palabra_actual
                        palabra_elegida = palabra
                        
                return(palabra_elegida)


            def medio(palabras):
                palabras_posibles = []
                for palabra in palabras:
                    puntaje_palabra_actual = calcular_puntaje_IA(palabra,puntaje_letra)
                    palabras_posibles.append(palabra, puntaje_palabra_actual)
                
                palabra_elegida =  palabras_posibles[len(palabras_posibles)//2]
                return(palabra_elegida)


            def facil(palabras):
                palabra_elegida = str
                min = 999
                for palabra in palabras:
                    puntaje_palabra_actual = calcular_puntaje_IA(palabra,puntaje_letra)
                    if puntaje_palabra_actual < min:
                        min = puntaje_palabra_actual
                        palabra_elegida = palabra
                return(palabra_elegida)


            if dificultad == 'Facil':
                return(facil(palabras_utilies))
            elif dificultad == "Dificil":
                return(dificil(palabras_utilies))
            else:
                return(medio(palabras_utilies))
        
        def calcular_puntaje_IA(palabra, puntos):
            puntaje = 0
            for char in palabra:
                for tupla in puntos:
                    if tupla[0] == char:
                        puntaje += tupla[1]
                        break
            return puntaje

        # letras = [v.letrar for _, v in Fichas.items()]
        letras = [] 
        puntaje_letra = [] 
        for key, value in Fichas.items():
            letras.append(key)
            puntaje_letra.append([key, value])
        # letras.sort() #Genero la lista de letras 
        
        palabras_posibles = []
        for palabra in lexicon.keys():
            if palabra in spelling.keys(): #por cada palabra que tiene pattern
                palabra_deletrada = []
                for char in palabra: #la separamos por caracteres, la ordenamos y generamos una lista con ellas
                    palabra_deletrada.append(char)
                palabra_deletrada.sort()
                if (sirve(letras, palabra_deletrada) ): #Comparamos ambas listas y si me sirve 
                    palabras_posibles.append(palabra)  #agregamos la palabra a nuestra lista de palabras utiles
        palabras_posibles_dos = [] #elimina las palabras de menos de 3 caracteres 
        for palabra in palabras_posibles:
            if len(palabra) >= 2 and len(palabra) < long_maxima:
                palabras_posibles_dos.append(palabra)
        
        if len(palabras_posibles_dos) == 0:
            return(None)
        palabras_utilies = []
        
        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = []
            for palabra in palabras_posibles_dos: #Creo una lista de threads
                results.append(executor.submit(validar_palabra, palabra))
        
            resultados = []
            for f in concurrent.futures.as_completed(results): #genero un iterador
                resultados.append(f.result()) # f es un objeto que tienen método result que te da el return de "cada thread"
        
        for i in range(0,len(resultados)): #si la palabra existe la aghrego a la lista de palabras utiles
            if resultados[i] == True:
                palabras_utilies.append(palabras_posibles_dos[i])

        if len(palabras_utilies) == 1:
            return(palabras_utilies)
        elif(len(palabras_utilies) > 1):
            return(por_dificulad(palabras_utilies, dificultad, puntaje_letra))
        else:
            return(None) 

    # Aveces ocurre algun error por parte de wiktionary ajeno
    # al codigo escrito por los aulumnos; cuando sucede
    # solo volvemos a ejecutar el codigo
    try: 
        try:
            return elegir_palabra_dos(Fichas, dificultad,long_maxima)
        except:
            return elegir_palabra_dos(Fichas, dificultad,long_maxima)
    except:
        return elegir_palabra_dos(Fichas, dificultad,long_maxima)

if __name__ == '__main__':
    dificultad = 'dificil'
    ejemplo = ['a','p','q','d','t','z','n','a','o','o','a']
    res= elegir_palabra(ejemplo, dificultad)   
    print(res, calcular_puntaje(res))
    #print(validar_palabra('asada'))
    #$%Comprobar espacio en tablero para la palabra
