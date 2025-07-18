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


if __name__ == "__main__":
    # Datos de ejemplo con encuestados
    arbol = ArbolRojoNegro()
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

    for d in datos:
        arbol.insertar(d)

    lista_encuestados = []
    arbol.recorrido_inorden(arbol.raiz, lista_encuestados)
    print("Lista de encuestados ordenada por experticia descendente y ID:")
    print(lista_encuestados[::-1])

# Comentario general: Se puede mejorar el código integrando validaciones para datos duplicados, 
# manejando actualización de datos de encuestados 

# Idea: Yo creo que podríamos hacer funciones auxiliares para calcular la mediana, moda, promedio, 
# extremismo y consenso recorriendo el árbol, extrayendo todas las opiniones en una lista 
# temporal y procesándola. Si hacemos funciones auxiliares no habria que cambiar ninguna estructura
# sino agregar al codigo y tomar la estructura del arbol