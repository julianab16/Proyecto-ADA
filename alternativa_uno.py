# Clase NodoRB: representa un nodo dentro del árbol rojo-negro
# Contiene los datos del encuestado y los punteros necesarios para el balance del árbol
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

class ArbolOpiniones(ArbolRojoNegro):
    def insertar(self, opinion_valor):
        # El ID y demás datos no importan aquí, solo la opinión para ordenarla
        nodo = NodoRB(id_encuestado=opinion_valor, experticia=0, opinion=opinion_valor, nombre=None)
        nodo.izq = self.NIL
        nodo.der = self.NIL
        nodo.padre = None

        y = None
        x = self.raiz

        while x != self.NIL:
            y = x
            # Ordenar ascendente por opinión
            if nodo.opinion < x.opinion:
                x = x.izq
            else:
                x = x.der

        nodo.padre = y
        if y is None:
            self.raiz = nodo
        elif nodo.opinion < y.opinion:
            y.izq = nodo
        else:
            y.der = nodo

        nodo.color = 'R'
        self.insertar_fixup(nodo)

def obtener_opiniones_ordenadas(arbol):
        resultado = []

        def inorden(nodo):
            if nodo != arbol.NIL:
                inorden(nodo.izq)
                resultado.append(nodo.opinion)
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
            encuestados = list(tema[pregunta_id])
            #Saca los opniones en un arreglo
            opiniones = [e['opinion'] for e in encuestados]
            resultados[pregunta_id] = opiniones

    medianas = {}
    for pregunta_id, opiniones in resultados.items():
        #Ordena los opiniones 
        arbol = ArbolOpiniones()
        for op in opiniones:
            arbol.insertar(op)
        ordenadas = obtener_opiniones_ordenadas(arbol)
        #Despues de ordenadas, calcula la mediana
        mediana = calcular_mediana(ordenadas)
        medianas[pregunta_id] = mediana

    # Ordena las mediadas
    arbol = ArbolOpiniones()
    for pregunta_id, mediana in medianas.items():
        arbol.insertar((mediana, pregunta_id))  # Mediana como clave, pregunta como valor
    ordenadas = obtener_opiniones_ordenadas(arbol)

    # Mayor y menor
    menor_mediana, menor_pregunta = ordenadas[0]
    mayor_mediana, mayor_pregunta = ordenadas[-1]

    print(f"Pregunta con Mayor mediana de opinion: [{mayor_mediana}] Pregunta: {mayor_pregunta[9:]}")
    print(f"Pregunta con Menor mediana de opinion: [{menor_mediana}] Pregunta: {menor_pregunta[9:]}")


if __name__ == "__main__":
    # Datos de ejemplo con encuestados
    arbol = ArbolRojoNegro()
    arbol_opiniones = ArbolOpiniones()
    datos = [
        {"id": 1, "experticia": 1, "opinion": 6, "nombre": "Sofia García"},
        {"id": 2, "experticia": 7, "opinion": 10, "nombre": "Alejandro Torres"},
        {"id": 3, "experticia": 9, "opinion": 0, "nombre": "Valentina Rodriguez"},
        {"id": 4, "experticia": 10, "opinion": 1, "nombre": "Juan López"},
        {"id": 5, "experticia": 7, "opinion": 0, "nombre": "Martina Martinez"},
        {"id": 6, "experticia": 8, "opinion": 9, "nombre": "Sebastián Pérez"},
        {"id": 7, "experticia": 2, "opinion": 7, "nombre": "Camila Fernández"},
        {"id": 8, "experticia": 4, "opinion": 7, "nombre": "Mateo González"},
        {"id": 9, "experticia": 7, "opinion": 5, "nombre": "Isabella Díaz"},
        {"id": 10, "experticia": 2, "opinion": 9, "nombre": "Daniel Ruiz"},
        {"id": 11, "experticia": 1, "opinion": 7, "nombre": "Luciana Sánchez"},
        {"id": 12, "experticia": 6, "opinion": 8, "nombre": "Lucas Vásquez"}
    ]

    temas = {
    "Tema 1": {
        "Pregunta 1.1": [
            {"id": 10, "experticia": 2, "opinion": 9, "nombre": "Daniel Ruiz"},
            {"id": 2, "experticia": 7, "opinion": 10, "nombre": "Alejandro Torres"}
        ],
        "Pregunta 1.2": [
            {"id": 1, "experticia": 1, "opinion": 6, "nombre": "Sofia García"},
            {"id": 9, "experticia": 7, "opinion": 5, "nombre": "Isabella Díaz"},
            {"id": 12, "experticia": 6, "opinion": 8, "nombre": "Lucas Vásquez"},
            {"id": 6, "experticia": 8, "opinion": 9, "nombre": "Sebastian Perez"}
        ]
    },
    "Tema 2": {
        "Pregunta 2.1": [
            {"id": 11, "experticia": 1, "opinion": 7, "nombre": "Luciana Sánchez"},
            {"id": 8, "experticia": 4, "opinion": 7, "nombre": "Mateo González"},
            {"id": 7, "experticia": 2, "opinion": 7, "nombre": "Camila Fernández"}
        ],
        "Pregunta 2.2": [
            {"id": 3, "experticia": 9, "opinion": 0, "nombre": "Valentina Rodriguez"},
            {"id": 4, "experticia": 10, "opinion": 1, "nombre": "Juan López"},
            {"id": 5, "experticia": 7, "opinion": 0, "nombre": "Martina Martinez"}
        ]}
    }

    for d in datos:
        arbol.insertar(d)

    lista_encuestados = []
    arbol.recorrido_inorden(arbol.raiz, lista_encuestados)
    print("Lista de encuestados ordenada por experticia descendente y ID:")
    print(lista_encuestados[::-1])

    moda_opinion = calcular_moda_arbol(arbol)
    print(f"Moda de opiniones en el árbol: {moda_opinion}")
    pregunta_moda_max_min_arn(temas)
    print()
    print("Medianas:")
    calcular_mediana_por_pregunta(temas)


# Comentario general: Se puede mejorar el código integrando validaciones para datos duplicados, 
# manejando actualización de datos de encuestados 

# Idea: Yo creo que podríamos hacer funciones auxiliares para calcular la mediana, moda, promedio, 
# extremismo y consenso recorriendo el árbol, extrayendo todas las opiniones en una lista 
# temporal y procesándola. Si hacemos funciones auxiliares no habria que cambiar ninguna estructura
# sino agregar al codigo y tomar la estructura del arbol