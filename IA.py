from pattern.es import lexicon, spelling, parse
from pattern.web import Wiktionary
import PySimpleGUI as sg
import time as t
import concurrent.futures
import json

def temporizador(tiempo, inicio):
    reloj = f'{divmod(tiempo,60)[0]:02}:{divmod(tiempo,60)[1]:02}'
    corriendo = True
    while corriendo:
        transcurrido = int(t.time())-inicio
        tiempo -= transcurrido
        reloj = f'{divmod(tiempo, 60)[0]:02}:{divmod(tiempo, 60)[1]:02}'
        if tiempo < 0:
            corriendo = False
        return reloj, corriendo

def validar_palabra(palabra):
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


def elegir_palabra(letras, dificultad,long_maxima = 7):
    def elegir_palabra_dos(letras, dificultad, long_maxima):
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

            for key in lista_uno:
                if key in dic_uno:
                    dic_uno[key] = dic_uno[key] + 1
                else:
                    dic_uno[key] = 1

            for key in lista_dos:
                if key in dic_dos:
                    dic_dos[key] = dic_dos[key] + 1
                else:
                    dic_dos[key] = 1
            
            dic_uno_keys  = []
            for key in dic_uno:
                dic_uno_keys.append(key)

            cumple = False
            for key in dic_dos:
                if key in dic_uno_keys:
                    cumple = True
                else:
                    cumple = False
                    break
            condicion = False
            if cumple:
                for key in dic_dos:
                    if dic_uno[key] >= dic_dos[key]:
                        condicion = True
                    else:
                        condicion = False
                        break
            return(condicion)


        def por_dificulad(palabras_utilies, dificultad):
            """
            Segun la dificultad elige una u otra palaba
            """
            def dificil(palabras):
                """
                cargo los puntajes y me fijo cual es la palabra que mayor puntaje da 
                """
                max = 0
                palabra_elegida = str
                with open('valores_puntajes.json') as f:
                    puntajes = json.load(f)
                    
                for palabra in palabras:
                    puntaje_palabra_actual = 0
                    for char in palabra:
                        puntaje_palabra_actual += puntajes['puntos_letra'][char]
                    if puntaje_palabra_actual > max:
                        max = puntaje_palabra_actual
                        palabra_elegida = palabra
                        
                return(palabra_elegida)


            def medio(palabras):
                with open('valores_puntajes.json') as f:
                    puntajes = json.load(f)
                palabras_posibles = []
                for palabra in palabras:
                    puntaje_palabra_actual = 0
                    for char in palabra:
                        puntaje_palabra_actual += puntajes['puntos_letra'][char]
                    palabras_posibles.append(palabra, puntaje_palabra_actual)
                
                palabra_elegida =  palabras_posibles[len(palabras_posibles)//2]
                return(palabra_elegida)


            def facil(palabras):
                palabra_elegida = str
                with open('valores_puntajes.json') as f:
                    puntajes = json.load(f)
                min = 999
                for palabra in palabras:
                    puntaje_palabra_actual = 0
                    for char in palabra:
                        puntaje_palabra_actual += puntajes['puntos_letra'][char]
                    if puntaje_palabra_actual < min:
                        min = puntaje_palabra_actual
                        palabra_elegida = palabra
                return(palabra_elegida)


            if dificultad == 'facil':
                return(facil(palabras_utilies))
            elif dificultad == "dificil":
                return(dificil(palabras_utilies))
            else:
                return(medio(palabras_utilies))

        letras.sort()
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
            if len(palabra) > 2 and len(palabra) < long_maxima:
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
                resultados.append(f.result()) # f es un objeto que tienen método result
        
        for i in range(0,len(resultados)): #si la palabra existe la aghrego a la lista de palabras utiles
            if resultados[i] == True:
                palabras_utilies.append(palabras_posibles_dos[i])

        if len(palabras_utilies) == 1:
            return(palabras_utilies)
        elif(len(palabras_utilies) > 1):
            return(por_dificulad(palabras_utilies, dificultad))
        else:
            return(None) 
    # Aveces ocurre algun error por parte de wiktionary ajeno
    # al codigo escrito por los aulumnos; cuando sucede
    # solo volvemos a ejecutar el codigo
    try: 
        try:
            return elegir_palabra_dos(letras, dificultad,long_maxima)
        except:
            return elegir_palabra_dos(letras, dificultad,long_maxima)
    except:
        return elegir_palabra_dos(letras, dificultad,long_maxima)

if __name__ == '__main__':
    # dificultad = 'dificil'
    # ejemplo = ['a','p','q','d','t','z','n']
    # res= elegir_palabra(ejemplo, dificultad)   
    # print(res)
    #print(validar_palabra('asada'))
    #$%Comprobar espacio en tablero para la palabra  
    corriendo = True
    inicio = int(t.time())
    while corriendo:
        reloj, corriendo = temporizador(10, inicio)
        print(reloj)
    
