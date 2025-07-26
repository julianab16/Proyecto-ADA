# Clase NodoRB: representa un nodo dentro del árbol rojo-negro
# Contiene los datos del encuestado y los punteros necesarios para el balance del árbol

import random
import time
import matplotlib.pyplot as plt

class NodoRB:
    def __init__(self, id_encuestado, experticia, opinion, nombre):
        self.id = id_encuestado
        self.experticia = experticia
        self.opinion = opinion
        self.nombre = nombre
        self.color = 'R'  # 'R' para rojo, 'B' para negro
        self.izq = None
        self.der = None
        self.padre = None

# Clase ArbolRojoNegro: implementa el árbol rojo-negro y sus operaciones básicas  
class ArbolRojoNegro:
    def __init__(self):
        self.NIL = NodoRB(None, None, None, None)
        self.NIL.color = 'B'
        self.raiz = self.NIL

    # Función para insertar un nuevo encuestado en el árbol.
    # Inserta el nodo siguiendo el orden por experticia descendente y, en caso de empate, por ID descendente. (revisar si debe ser ese el orden en caso de empate)
    # Luego llama al balanceo del árbol para mantener las propiedades del árbol rojo-negro.
    def insertar(self, nuevo):
        nodo = NodoRB(nuevo['id'], nuevo['experticia'], nuevo['opinion'], nuevo['nombre'])
        nodo.izq = self.NIL
        nodo.der = self.NIL
        nodo.padre = None

        y = None
        x = self.raiz

        while x != self.NIL:
            y = x
             # Ordenar primero por experticia descendente, luego por ID descendente
            if nodo.experticia > x.experticia or (nodo.experticia == x.experticia and nodo.id > x.id):
                x = x.izq
            else:
                x = x.der

        nodo.padre = y
        if y is None:
            self.raiz = nodo
        elif nodo.experticia > y.experticia or (nodo.experticia == y.experticia and nodo.id > y.id):
            y.izq = nodo
        else:
            y.der = nodo

        nodo.color = 'R'
        self.insertar_fixup(nodo)

    # Función para restaurar las propiedades del árbol rojo-negro después de insertar un nodo.
    # Corrige posibles violaciones a las reglas de balance del árbol mediante rotaciones y recoloreos,
    # asegurando que el árbol permanezca balanceado con altura O(log n).    
    def insertar_fixup(self, z):
        while z.padre and z.padre.color == 'R':
            if z.padre == z.padre.padre.izq:
                y = z.padre.padre.der
                if y and y.color == 'R':
                    z.padre.color = 'B'
                    y.color = 'B'
                    z.padre.padre.color = 'R'
                    z = z.padre.padre
                else:
                    if z == z.padre.der:
                        z = z.padre
                        self.rotar_izquierda(z)
                    z.padre.color = 'B'
                    z.padre.padre.color = 'R'
                    self.rotar_derecha(z.padre.padre)
            else:
                y = z.padre.padre.izq
                if y and y.color == 'R':
                    z.padre.color = 'B'
                    y.color = 'B'
                    z.padre.padre.color = 'R'
                    z = z.padre.padre
                else:
                    if z == z.padre.izq:
                        z = z.padre
                        self.rotar_derecha(z)
                    z.padre.color = 'B'
                    z.padre.padre.color = 'R'
                    self.rotar_izquierda(z.padre.padre)
        self.raiz.color = 'B'

    # Rotación izquierda utilizada en las operaciones de balance
    def rotar_izquierda(self, x):
        y = x.der
        x.der = y.izq
        if y.izq != self.NIL:
            y.izq.padre = x
        y.padre = x.padre
        if x.padre is None:
            self.raiz = y
        elif x == x.padre.izq:
            x.padre.izq = y
        else:
            x.padre.der = y
        y.izq = x
        x.padre = y

    # Rotación derecha utilizada en las operaciones de balance
    def rotar_derecha(self, x):
        y = x.izq
        x.izq = y.der
        if y.der != self.NIL:
            y.der.padre = x
        y.padre = x.padre
        if x.padre is None:
            self.raiz = y
        elif x == x.padre.der:
            x.padre.der = y
        else:
            x.padre.izq = y
        y.der = x
        x.padre = y

    # Aqui hice un recorrido personalizado del árbol, devolvuelve IDs en orden de mayor a menor experticia e ID.
    # Se utiliza un recorrido modificado donde primero se visita el subárbol derecho, luego el nodo actual,
    # y finalmente el subárbol izquierdo. Esto evita tener que invertir la lista al final. 
    # Con esto ya quedo solucionado lo que les mostre que aparecia la lista al reves :)
    def recorrido_inorden(self, nodo, resultado):
        if nodo != self.NIL:
            self.recorrido_inorden(nodo.der, resultado)
            resultado.append(nodo.id)
            self.recorrido_inorden(nodo.izq, resultado)

# Clase para ordenar las opniones
class ArbolOpiniones(ArbolRojoNegro):
    def insertarOpiniones(self, encuestado):
        nodo = NodoRB(encuestado['id'], encuestado['experticia'], encuestado['opinion'], encuestado['nombre'])
        nodo.izq = self.NIL
        nodo.der = self.NIL
        nodo.padre = None

        y = None
        x = self.raiz

        while x != self.NIL:
            y = x
            # Ordenar decente por opinión, y por experticia
            if nodo.opinion > x.opinion or (nodo.opinion == y.opinion and nodo.experticia > y.experticia):
                x = x.izq
            else:
                x = x.der

        nodo.padre = y
        if y is None:
            self.raiz = nodo
        elif nodo.opinion > y.opinion or (nodo.opinion == y.opinion and nodo.experticia > y.experticia):
            y.izq = nodo
        else:
            y.der = nodo

        nodo.color = 'R'
        self.insertar_fixup(nodo)
        
# Recorre el arbol sacando las opniones de las preguntas en un arreglo
def recorrer_inorden_opniones(arbol):
        resultado = []
        def inorden(nodo):
            if nodo != arbol.NIL:
                inorden(nodo.izq)
                resultado.append(nodo.opinion)
                inorden(nodo.der)
        inorden(arbol.raiz)
        return resultado

# Clase para ordenar las medianas 
class ArbolMediadas(ArbolRojoNegro):
    def insertarMediadas(self, encuestado):
        # El ID de la pregunta se guarda en el id de encuestado y la mediana en la opnion
        nodo = NodoRB(id_encuestado=encuestado[0], experticia=0, opinion=encuestado[1], nombre=None)
        nodo.izq = self.NIL
        nodo.der = self.NIL
        nodo.padre = None

        y = None
        x = self.raiz

        while x != self.NIL:
            y = x
            # Ordenar ascendente por mediana y por id
            if nodo.opinion < x.opinion or (nodo.opinion == y.opinion and nodo.id > y.id):
                x = x.izq
            else:
                x = x.der

        nodo.padre = y
        if y is None:
            self.raiz = nodo
            # Ordenar ascendente por mediana y por id
        elif nodo.opinion < y.opinion or (nodo.opinion == y.opinion and nodo.id < y.id):
            y.izq = nodo
        else:
            y.der = nodo
        nodo.color = 'R'
        self.insertar_fixup(nodo)

# Recorre el arbol sacando los ids y medianas de las preguntas en un arreglo
def recorrer_inorden_medianas(arbol):
        resultado = []
        def inorden(nodo):
            if nodo != arbol.NIL:
                inorden(nodo.izq)
                resultado.append((nodo.opinion, nodo.id))
                inorden(nodo.der)
        inorden(arbol.raiz)
        return resultado

# Recorre el árbol y extrae todas las opiniones en una lista
def recolectar_opiniones(nodo, NIL, opiniones):
    if nodo != NIL:
        recolectar_opiniones(nodo.izq, NIL, opiniones)
        if nodo.opinion is not None:
            opiniones.append(nodo.opinion)
        recolectar_opiniones(nodo.der, NIL, opiniones)


# Calcula el promedio de la lista 
def calcular_promedio(lista):
    if not lista:
        return 0  # Evita división por cero si la lista está vacía
    return sum(lista) / len(lista)

#####################################################################################

class ArbolOpinionExperticia(ArbolRojoNegro):
    # Clase para manejar el árbol de opiniones y experticias, que contiene nodos de tipo NodoRB
    # Cada nodo representa un encuestado con su ID, experticia, opinión y nombre
    def insertar(self, e):
        nodo = NodoRB(e["id"], e["experticia"], e["opinion"], e["nombre"])
        nodo.izq = self.NIL
        nodo.der = self.NIL
        nodo.padre = None

        y = None
        x = self.raiz
        # Inserta el nodo en el árbol siguiendo el orden por opinión descendente,
        # luego por experticia descendente, y finalmente por ID ascendente en caso de empate
        while x != self.NIL:
            y = x
            if (
                nodo.opinion > x.opinion or
                (nodo.opinion == x.opinion and nodo.experticia > x.experticia) or
                (nodo.opinion == x.opinion and nodo.experticia == x.experticia and nodo.id < x.id)
            ):
                x = x.izq
            else:
                x = x.der

        nodo.padre = y
        if y is None:
            self.raiz = nodo
        elif (
            nodo.opinion > y.opinion or
            (nodo.opinion == y.opinion and nodo.experticia > y.experticia) or
            (nodo.opinion == y.opinion and nodo.experticia == y.experticia and nodo.id < y.id)
        ):
            y.izq = nodo
        else:
            y.der = nodo

        nodo.color = 'R'
        self.insertar_fixup(nodo)

    def recorrido_inorden(self, nodo, resultado):
        if nodo != self.NIL:
            self.recorrido_inorden(nodo.izq, resultado)
            resultado.append(nodo.id)
            self.recorrido_inorden(nodo.der, resultado)

def obtener_datos(encuestados):
    # Crea un árbol de opiniones y experticias
    arbol = ArbolOpinionExperticia()
    for e in encuestados:
        arbol.insertar(e)

    # Saca los datos
    opiniones = [e["opinion"] for e in encuestados]
    experticias = [e["experticia"] for e in encuestados]
    cantidad = len(encuestados)

    promedio_opinion = calcular_promedio(opiniones)
    promedio_experticia = calcular_promedio(experticias)
    # Recorre el árbol para obtener los IDs de los encuestados en orden
    ids_ordenados = []
    arbol.recorrido_inorden(arbol.raiz, ids_ordenados)
    # Devuelve los promedios, cantidad y los IDs ordenados
    return promedio_opinion, promedio_experticia, cantidad, ids_ordenados


class NodoPreguntaRB(NodoRB):
    # Nodo específico para las preguntas, hereda de NodoRB
    # Contiene el ID de la pregunta, promedios de opinión y experticia, cantidad de encuestados y una lista de IDs de encuestados   
    def __init__(self, pregunta_id, promedio_opinion, promedio_experticia, cantidad, encuestados):
        super().__init__(id_encuestado=None, experticia=promedio_experticia, opinion=promedio_opinion, nombre=None)
        self.pregunta_id = pregunta_id
        self.promedio_opinion = promedio_opinion
        self.promedio_experticia = promedio_experticia
        self.cantidad = cantidad
        self.encuestados = encuestados


class ArbolPreguntas(ArbolRojoNegro):
    # Clase para manejar el árbol de preguntas, que contiene nodos de tipo NodoPreguntaRB
    # Cada nodo representa una pregunta con su ID, promedios de opinión y experticia
    def __init__(self):
        super().__init__()
        self.NIL = NodoPreguntaRB(None, 0, 0, 0, [])
        self.NIL.color = 'B'
        self.raiz = self.NIL

    def insertar(self, nodo):
        y = None
        x = self.raiz
        while x != self.NIL:
            y = x
            # Orden descendente por promedio_opinion, luego promedio_experticia, luego cantidad, luego pregunta_id ascendente
            if (nodo.promedio_opinion > x.promedio_opinion or
                (nodo.promedio_opinion == x.promedio_opinion and nodo.promedio_experticia > x.promedio_experticia) or
                (nodo.promedio_opinion == x.promedio_opinion and nodo.promedio_experticia == x.promedio_experticia and nodo.cantidad > x.cantidad) or
                (nodo.promedio_opinion == x.promedio_opinion and nodo.promedio_experticia == x.promedio_experticia and nodo.cantidad == x.cantidad and nodo.pregunta_id < x.pregunta_id)):
                x = x.izq
            else:
                x = x.der
        nodo.padre = y
        if y is None:
            self.raiz = nodo
        elif (nodo.promedio_opinion > y.promedio_opinion or
              (nodo.promedio_opinion == y.promedio_opinion and nodo.promedio_experticia > y.promedio_experticia) or
              (nodo.promedio_opinion == y.promedio_opinion and nodo.promedio_experticia == y.promedio_experticia and nodo.cantidad > y.cantidad) or
              (nodo.promedio_opinion == y.promedio_opinion and nodo.promedio_experticia == y.promedio_experticia and nodo.cantidad == y.cantidad and nodo.pregunta_id < y.pregunta_id)):
            y.izq = nodo
        else:
            y.der = nodo
        nodo.color = 'R'
        self.insertar_fixup(nodo)

    def recorrido(self, nodo, resultado):
        if nodo != self.NIL:
            self.recorrido(nodo.izq, resultado)
            resultado.append(nodo)
            self.recorrido(nodo.der, resultado)

class NodoTemaRB(NodoRB):
    # Nodo específico para los temas, hereda de NodoRB
    def __init__(self, tema_nombre, promedio_opinion, promedio_experticia, cantidad, arbol_preguntas):
        super().__init__(
            id_encuestado=None,
            experticia=promedio_experticia,
            opinion=promedio_opinion,
            nombre=tema_nombre)
        
        self.tema_nombre = tema_nombre
        self.promedio_opinion = promedio_opinion
        self.promedio_experticia = promedio_experticia
        self.cantidad = cantidad
        self.arbol_preguntas = arbol_preguntas  


class ArbolTemas(ArbolRojoNegro):
    # Clase para manejar el árbol de temas, que contiene nodos de tipo NodoTemaRB
    # Cada nodo representa un tema con su nombre, promedios de opinión y experticia, cantidad de preguntas y un árbol de preguntas
    def __init__(self):
        self.NIL = NodoTemaRB(None, 0, 0, 0, None)
        self.NIL.color = 'B'
        self.raiz = self.NIL

    def insertar(self, nodo):
        y = None
        x = self.raiz
        while x != self.NIL:
            y = x
            # Orden descendente por promedio_opinion, luego promedio_experticia, luego cantidad, luego nombre ascendente
            if (nodo.promedio_opinion > x.promedio_opinion or
                (nodo.promedio_opinion == x.promedio_opinion and nodo.promedio_experticia > x.promedio_experticia) or
                (nodo.promedio_opinion == x.promedio_opinion and nodo.promedio_experticia == x.promedio_experticia and nodo.cantidad > x.cantidad) or
                (nodo.promedio_opinion == x.promedio_opinion and nodo.promedio_experticia == x.promedio_experticia and nodo.cantidad == x.cantidad and nodo.tema_nombre < x.tema_nombre)):
                x = x.izq
            else:
                x = x.der
        nodo.padre = y
        if y is None:
            self.raiz = nodo
        elif (nodo.promedio_opinion > y.promedio_opinion or
              (nodo.promedio_opinion == y.promedio_opinion and nodo.promedio_experticia > y.promedio_experticia) or
              (nodo.promedio_opinion == y.promedio_opinion and nodo.promedio_experticia == y.promedio_experticia and nodo.cantidad > y.cantidad) or
              (nodo.promedio_opinion == y.promedio_opinion and nodo.promedio_experticia == y.promedio_experticia and nodo.cantidad == y.cantidad and nodo.tema_nombre < y.tema_nombre)):
            y.izq = nodo
        else:
            y.der = nodo
        nodo.color = 'R'
        self.insertar_fixup(nodo)

    def recorrido(self, nodo, resultado):
        if nodo != self.NIL:
            self.recorrido(nodo.izq, resultado)
            resultado.append(nodo)
            self.recorrido(nodo.der, resultado)

def temas_ordenados(temas):
    arbol_temas = ArbolTemas()
    # Recorre los temas y crea un árbol de preguntas para cada uno
    # Calcula los promedios de opinión y experticia, y la cantidad total de encuestados
    for tema_nombre, preguntas in temas.items():
        # Crea un árbol de preguntas para el tema actual
        arbol_preguntas = ArbolPreguntas()
        # Recorre las preguntas del tema y obtiene los datos necesarios para crear nodos de tipo NodoPreguntaRB
        for pregunta_id, encuestados in preguntas.items():
            # Obtiene los datos necesarios para el nodo de pregunta
            # Calcula los promedios de opinión y experticia, y la cantidad total de
            prom_op, prom_exp, cantidad, ids = obtener_datos(encuestados)
            nodo_pregunta = NodoPreguntaRB(pregunta_id, prom_op, prom_exp, cantidad, ids)
            nodo_pregunta.izq = arbol_preguntas.NIL
            nodo_pregunta.der = arbol_preguntas.NIL
            arbol_preguntas.insertar(nodo_pregunta)
        preguntas_lista = []
        # Recorre el árbol de preguntas y obtiene los promedios y cantidad total
        arbol_preguntas.recorrido(arbol_preguntas.raiz, preguntas_lista)
        promedio_opinion_tema = calcular_promedio([p.promedio_opinion for p in preguntas_lista])
        promedio_experticia_tema = calcular_promedio([p.promedio_experticia for p in preguntas_lista])
        cantidad_total = sum(p.cantidad for p in preguntas_lista)
        # Crea un nodo de tema con los promedios y el árbol de preguntas y lo inserta en el árbol de temas
        nodo_tema = NodoTemaRB(
            tema_nombre,
            promedio_opinion_tema,
            promedio_experticia_tema,
            cantidad_total,
            arbol_preguntas )
        nodo_tema.izq = arbol_temas.NIL
        nodo_tema.der = arbol_temas.NIL
        arbol_temas.insertar(nodo_tema)
    # Recorre el árbol de temas y muestra los resultados
    temas_lista = []
    arbol_temas.recorrido(arbol_temas.raiz, temas_lista)
    for tema in temas_lista:
        # Imprime el nombre del tema, su promedio de opinión y el árbol de preguntas asociado  
        print(f"[{tema.promedio_opinion:.2f}] {tema.tema_nombre}")
        preguntas_ordenadas = []
        # Recorre el árbol de preguntas del tema y obtiene los nodos ordenados
        tema.arbol_preguntas.recorrido(tema.arbol_preguntas.raiz, preguntas_ordenadas)
        for pregunta in preguntas_ordenadas:
            print(f"[{pregunta.promedio_opinion:.2f}] {pregunta.pregunta_id}: {tuple(pregunta.encuestados)}")

# Función para la pregunta con mayor y menor promedio
def pregunta_mayor_menor_promedio(temas):
    resultados = []
    for tema_nombre in temas:
        preguntas = temas[tema_nombre]
        for pregunta_id, encuestados in preguntas.items():
            opiniones = [e['opinion'] for e in encuestados]
            if opiniones:
                promedio = calcular_promedio(opiniones)
                resultados.append((pregunta_id, promedio))
    if not resultados:
        print("No hay preguntas con opiniones.")
        return

    mayor = max(resultados, key=lambda x: (x[1], -ord(x[0][0])))
    menor = min(resultados, key=lambda x: (x[1], x[0]))

    print(f"Pregunta con MAYOR promedio: {mayor[0]} con promedio = {mayor[1]:.2f}")
    print(f"Pregunta con MENOR promedio: {menor[0]} con promedio = {menor[1]:.2f}")


# Calcula la moda de una lista, devolviendo la menor si hay empate
def calcular_moda_lista(lista):
    frecuencias = {}

    for valor in lista:
        if valor in frecuencias:
            frecuencias[valor] += 1
        else:
            frecuencias[valor] = 1

    max_frecuencia = 0
    posibles_modas = []

    for valor in frecuencias:
        if frecuencias[valor] > max_frecuencia:
            max_frecuencia = frecuencias[valor]
            posibles_modas = [valor]
        elif frecuencias[valor] == max_frecuencia:
            posibles_modas.append(valor)

    return min(posibles_modas)

# Función principal: calcula la moda del árbol Rojo-Negro
# funcion de prueba se puede eliminar
def calcular_moda_arbol(arbol_rb):
    opiniones = []
    recolectar_opiniones(arbol_rb.raiz, arbol_rb.NIL, opiniones)
    if not opiniones:
        return None  # Si no hay datos
    return calcular_moda_lista(opiniones)

def pregunta_moda_max_min_arn(temas):
    resultados = []

    for tema_nombre in temas:
        preguntas = temas[tema_nombre]
        for pregunta_id in preguntas:
            encuestados = preguntas[pregunta_id]

            # Insertar en un árbol rojo-negro temporal
            arbol = ArbolRojoNegro()
            for e in encuestados:
                arbol.insertar(e)

            # Recolectar opiniones desde el árbol
            opiniones = []
            recolectar_opiniones(arbol.raiz, arbol.NIL, opiniones)

            if opiniones:
                moda_valor = calcular_moda_lista(opiniones)
                resultados.append((pregunta_id, moda_valor))

    # Inicializar con la primera pregunta
    mayor = menor = resultados[0]

    for r in resultados[1:]:
        # Comparar mayor moda
        if r[1] > mayor[1]:
            mayor = r
        elif r[1] == mayor[1] and r[0] < mayor[0]:  # menor ID si empate
            mayor = r

        # Comparar menor moda
        if r[1] < menor[1]:
            menor = r
        elif r[1] == menor[1] and r[0] < menor[0]:  # menor ID si empate
            menor = r

    print(f"Pregunta con MAYOR moda: {mayor[0]} con moda = {mayor[1]}")
    print(f"Pregunta con MENOR moda: {menor[0]} con moda = {menor[1]}")
    
def pregunta_mayor_consenso(temas):
 # Inicializamos variables para guardar la mejor pregunta y el mayor porcentaje de consenso encontrado   
    mejor_pregunta = None
    mejor_consenso = -1.0
 
  # Iteramos sobre cada tema
    for tema_nombre in temas:
        preguntas = temas[tema_nombre]
       
        # Iteramos sobre cada pregunta dentro del tema
        for pregunta_id in preguntas:
            encuestados = preguntas[pregunta_id]
             # Extraemos solo las opiniones de los encuestados
            opiniones = [e["opinion"] for e in encuestados]
            if not opiniones:
                continue
            # Calculamos la moda para esta pregunta con la funcion de moda de arriba       
            moda = calcular_moda_lista(opiniones)
            cantidad_moda = opiniones.count(moda)
             # Contamos cuántos encuestados tienen esa opinión
            total = len(opiniones)
            consenso = cantidad_moda / total  #aqui calculamos el porcentaje entre 0 y 1 del consenso
            # Actualizamos si encontramos una pregunta con mayor consenso,
            # o si hay empate, la que tenga ID menor (lexicográficamente)
            if consenso > mejor_consenso or (consenso == mejor_consenso and pregunta_id < mejor_pregunta):
                mejor_consenso = consenso
                mejor_pregunta = pregunta_id
    
    # Imprimimos la pregunta con mayor consenso y su porcentaje (redondeado)
    porcentaje = round(mejor_consenso * 100, 2)
    print(f"Pregunta con MAYOR CONSENSO: {mejor_pregunta} con {porcentaje}% de opiniones iguales a la moda")
   
# Funcion para calcular la mediana
def calcular_mediana(lista):
    n = len(lista)
    if n % 2 == 1:
        return lista[n // 2]
    else:
        return (lista[n // 2 - 1] + lista[n // 2]) // 2
    
def calcular_mediana_por_pregunta(temas):
    resultados = {}  # Guardará las opiniones por pregunta
    for tema_nombre in temas:
        tema = temas[tema_nombre]
        for pregunta_id in tema:
            #Saca los encuestados en una lista
            encuestados = list(tema[pregunta_id])
            # Va ordenando las opniones 
            arbol = ArbolOpiniones()
            for op in encuestados:
                arbol.insertarOpiniones(op)
            # Obtiene los opiniones
            ordenadas = recorrer_inorden_opniones(arbol)
            # Calcula la mediana
            mediana = calcular_mediana(ordenadas)
            resultados[pregunta_id] = mediana
    
    # Ordena las mediadas
    arbol = ArbolMediadas()
    for pregunta_id, mediana in resultados.items():
        # Inserta: id = pregunta, opinion = mediana
        arbol.insertarMediadas((pregunta_id, mediana))
    # Obtiene las medianas ordendas
    mediadas_ordenadas = recorrer_inorden_medianas(arbol)

    # Mayor y menor
    menor_mediana, menor_pregunta = mediadas_ordenadas[0]
    mayor_mediana, mayor_pregunta = mediadas_ordenadas[-1]

    print(f"Pregunta con Mayor mediana de opinion: [{mayor_mediana}] Pregunta: {mayor_pregunta[9:]}")
    print(f"Pregunta con Menor mediana de opinion: [{menor_mediana}] Pregunta: {menor_pregunta[9:]}") 

def pregunta_mayor_extremismo(temas):
    # Inicializa variables para guardar el mayor porcentaje de extremismo y la pregunta correspondiente
    mayor_extremismo = None
    pregunta_mayor = None
    # Recorre todos los temas
    for tema_nombre in temas:
        preguntas = temas[tema_nombre]
        # Recorre todas las preguntas de cada tema
        for pregunta_id, encuestados in preguntas.items():
            total = len(encuestados)  # Total de encuestados en la pregunta
            if total == 0:
                continue  # Si no hay encuestados, pasa a la siguiente pregunta
            # Cuenta cuántos encuestados tienen opinión 0 o 10 (extremos)
            extremos = sum(1 for e in encuestados if e['opinion'] == 0 or e['opinion'] == 10)
            porcentaje = extremos / total  # Calcula el porcentaje de extremismo
            # Actualiza si encuentra un mayor porcentaje de extremismo o empate con menor ID
            if (mayor_extremismo is None) or (porcentaje > mayor_extremismo) or (porcentaje == mayor_extremismo and pregunta_id < pregunta_mayor):
                mayor_extremismo = porcentaje
                pregunta_mayor = pregunta_id
    # Imprime el resultado si se encontró alguna pregunta con encuestados
    if pregunta_mayor is not None:
        print(f"Pregunta con MAYOR extremismo: {pregunta_mayor} con extremismo = {mayor_extremismo}")
    else:
        print("No hay preguntas con extremismo.")


# if __name__ == "__main__":
#     # Datos de ejemplo con encuestados
#     arbol = ArbolRojoNegro()
#     arbol_opiniones = ArbolOpiniones()
#     datos = [
#         {"id": 1, "experticia": 1, "opinion": 6, "nombre": "Sofia García"},
#         {"id": 2, "experticia": 7, "opinion": 10, "nombre": "Alejandro Torres"},
#         {"id": 3, "experticia": 9, "opinion": 0, "nombre": "Valentina Rodriguez"},
#         {"id": 4, "experticia": 10, "opinion": 1, "nombre": "Juan López"},
#         {"id": 5, "experticia": 7, "opinion": 0, "nombre": "Martina Martinez"},
#         {"id": 6, "experticia": 8, "opinion": 9, "nombre": "Sebastián Pérez"},
#         {"id": 7, "experticia": 2, "opinion": 7, "nombre": "Camila Fernández"},
#         {"id": 8, "experticia": 4, "opinion": 7, "nombre": "Mateo González"},
#         {"id": 9, "experticia": 7, "opinion": 5, "nombre": "Isabella Díaz"},
#         {"id": 10, "experticia": 2, "opinion": 9, "nombre": "Daniel Ruiz"},
#         {"id": 11, "experticia": 1, "opinion": 7, "nombre": "Luciana Sánchez"},
#         {"id": 12, "experticia": 6, "opinion": 8, "nombre": "Lucas Vásquez"}
#     ]

#     temas = {
        
#     "Tema 1": {
#         "Pregunta 1.1": [
#             {"id": 10, "experticia": 2, "opinion": 9, "nombre": "Daniel Ruiz"},
#             {"id": 2, "experticia": 7, "opinion": 10, "nombre": "Alejandro Torres"}
#         ],
#         "Pregunta 1.2": [
#             {"id": 1, "experticia": 1, "opinion": 6, "nombre": "Sofia García"},
#             {"id": 9, "experticia": 7, "opinion": 5, "nombre": "Isabella Díaz"},
#             {"id": 12, "experticia": 6, "opinion": 8, "nombre": "Lucas Vásquez"},
#             {"id": 6, "experticia": 8, "opinion": 9, "nombre": "Sebastian Perez"}
#         ]
#     },
#     "Tema 2": {
#         "Pregunta 2.1": [
#             {"id": 11, "experticia": 1, "opinion": 7, "nombre": "Luciana Sánchez"},
#             {"id": 8, "experticia": 4, "opinion": 7, "nombre": "Mateo González"},
#             {"id": 7, "experticia": 2, "opinion": 7, "nombre": "Camila Fernández"}
#         ],
#         "Pregunta 2.2": [
#             {"id": 3, "experticia": 9, "opinion": 0, "nombre": "Valentina Rodriguez"},
#             {"id": 4, "experticia": 10, "opinion": 1, "nombre": "Juan López"},
#             {"id": 5, "experticia": 7, "opinion": 0, "nombre": "Martina Martinez"}
#         ]}
#     }


#     for d in datos:
#         arbol.insertar(d)

#     lista_encuestados = []
#     arbol.recorrido_inorden(arbol.raiz, lista_encuestados)
#     print("Lista de encuestados ordenada por experticia descendente y ID:")
#     print(lista_encuestados[::-1])
#     print()
#     print("Lista de Temas ordenada:")
#     temas_ordenados(temas)
#     print()
#     print("Promedios:")
#     pregunta_mayor_menor_promedio(temas)
#     print()
#     print(f"Moda:")
#     pregunta_moda_max_min_arn(temas)
#     print()
#     print("Medianas:")
#     calcular_mediana_por_pregunta(temas)
#     print()
#     print("Consenso:")
#     pregunta_mayor_consenso(temas)
#     print()
#     print("Extremismo:")
#     pregunta_mayor_extremismo(temas)


def generar_datos(potencia):
    """
    Genera temas y preguntas según la potencia de dos.
    - Número de temas = 2**potencia
    - Número de preguntas por tema: aleatorio entre 2 y 10
    - Cada pregunta tiene entre 2 y 10 encuestados únicos (no se repiten entre preguntas)
    """
    num_temas = 2**potencia
    temas = {}
    preguntas_total = 0
    preguntas_por_tema = []
    # Decide cuántas preguntas tendrá cada tema
    for _ in range(num_temas):
        n_preg = random.randint(2, 10)
        preguntas_por_tema.append(n_preg)
        preguntas_total += n_preg

    # Genera suficientes encuestados únicos
    encuestados = {}
    for i in range(1, preguntas_total * 10):
        nombre = f"Persona_{i}"
        experticia = random.randint(1, 10)
        opinion = random.randint(0, 10)
        encuestados[i] = {"id": i, "experticia": experticia, "opinion": opinion, "nombre": nombre}

    encuestados_disponibles = list(encuestados.values())
    random.shuffle(encuestados_disponibles)

    for tema_idx in range(num_temas):
        tema_nombre = f"Tema_{tema_idx+1}"
        temas[tema_nombre] = {}
        for preg_idx in range(preguntas_por_tema[tema_idx]):
            pregunta_nombre = f"Pregunta_{preg_idx+1}"
            # Garantiza mínimo 2 y máximo 10 encuestados por pregunta
            max_cantidad = min(10, len(encuestados_disponibles))
            if max_cantidad < 2:
                break  # No hay suficientes encuestados para esta pregunta
            cantidad = random.randint(2, max_cantidad)
            asignados = list(encuestados_disponibles[:cantidad])
            temas[tema_nombre][pregunta_nombre] = asignados
            encuestados_disponibles = encuestados_disponibles[cantidad:]
            if len(encuestados_disponibles) < 2:
                break
        if len(encuestados_disponibles) < 2:
            break

    personas = list(encuestados.values())
    return temas, personas

def measure_time(func, *args, **kwargs):
    start = time.time()
    func(*args, **kwargs)
    end = time.time()
    return end - start

potencias = [6, 8, 10, 12]
tiempos = []
for p in potencias:
    temas, personas = generar_datos(p)
    tiempos.append(measure_time(temas_ordenados, temas))
    print(f"Tiempo para 2^{p}: {tiempos[-1]:.6f} segundos")

print("Tiempos de ejecución para diferentes tamaños de entrada:")
for p, t in zip(potencias, tiempos):
    print(f"2^{p}: {t:.6f} segundos")

sizes = [2**p for p in potencias]

plt.figure(figsize=(8,5))
plt.plot(sizes, tiempos, marker='o')
plt.xlabel('Tamaño de entrada (número de temas)')
plt.ylabel('Tiempo de ejecución (segundos)')
plt.title('Tamaño de entrada vs Tiempo de ejecución')
plt.grid(True)
plt.show()

# Comentario general: Se puede mejorar el código integrando validaciones para datos duplicados, 
# manejando actualización de datos de encuestados 

# Idea: Yo creo que podríamos hacer funciones auxiliares para calcular la mediana, moda, promedio, 
# extremismo y consenso recorriendo el árbol, extrayendo todas las opiniones en una lista 
# temporal y procesándola. Si hacemos funciones auxiliares no habria que cambiar ninguna estructura
# sino agregar al codigo y tomar la estructura del arbol