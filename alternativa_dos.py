
# Function to merge and sort encuestados based on Experticia and ID
def merge_encuestados(lista):
    if len(lista) <= 1:
        return lista
    mid = len(lista) // 2

    def merge_sorted(left, right):
        merged = []
        while left and right:
            # Compare the Experticia of the tuples
            if left[0][1][1] > right[0][1][1]:
                merged.append(left[0])
                left.pop(0)
            elif left[0][1][1] == right[0][1][1]:
                # If are the same compare the ID of the tuples
                if left[0][0] > right[0][0]:
                    merged.append(left[0])
                    left.pop(0)
                else:
                    merged.append(right[0])
                    right.pop(0)
            else: 
                merged.append(right[0])
                right.pop(0)
        if left:
            merged +=left
        if right:
            merged +=right

        return merged

    return merge_sorted(merge_encuestados(lista[:mid]),  merge_encuestados(lista[mid:]))

# Function to merge and sort preguntas based on Experticia and Opinión
def merge_opiniones(lista):
        if len(lista) <= 1:
            return lista
        mid = len(lista) // 2

        def merge_sorted(left, right):
            merged = [] # Initialize merged list
            while left and right:
                # Compare the Opinión of the tuples
                if left[0][2] > right[0][2]:
                    merged.append(left[0])
                    left.pop(0)
                elif left[0][2] == right[0][2]:
                    # If are the same compare the Experticia of the tuples
                    if left[0][1] > right[0][1]:
                        merged.append(left[0])
                        left.pop(0)
                    else:
                        merged.append(right[0])
                        right.pop(0)
                else: 
                    merged.append(right[0])
                    right.pop(0)
            if left:
                merged +=left
            if right:
                merged +=right
            return merged
        return merge_sorted(merge_opiniones(lista[:mid]),  merge_opiniones(lista[mid:]))

# Function outs the list of IDs ordered
def ordenar_encuestados(arr):
    nuevo_arr = []
    merged = merge_encuestados(arr)
    for i in merged:
        nuevo_arr.append(i[0])
    print(nuevo_arr)

# Function to calculate the average
def calcular_promedio(list, j):
    n = 0
    for i in list:
        n += i[j]
    promedio = n / len(list)
    promedio_redondeado = round(promedio, 2)
    return promedio_redondeado

# Function to get the key from a value in a dictionary
def obtener_llave_por_valor(diccionario, valor_buscado):
    for llave, valor in diccionario:
        if valor == valor_buscado:
            return llave
    return None


def insertionsort(arr):
    n = len(arr)  # Get the length of the array
     
    if n <= 1:
        return  # If the array has 0 or 1 element, it is already sorted, so return

    for i in range(1, n):  # Iterate over the array starting from the second element
        key = arr[i]  # Store the current element as the key to be inserted in the right position
        j = i-1
        while j >= 0 and key[0] > arr[j][0]:  # Move elements greater than key one position ahead
            arr[j+1] = arr[j] # Shift elements to the right
            j -= 1
        arr[j+1] = key  # Insert the key in the correct position
    return arr  # Return the sorted array

# funcion moda que calcula la moda de una lista
# Si hay empate, devuelve el menor valor
def moda(lista):
    # Creamos un diccionario de frecuencias
    frecuencias = {}
    
    for valor in lista:
        if valor in frecuencias:
            frecuencias[valor] += 1
        else:
            frecuencias[valor] = 1

    # Buscamos el valor de mayor frecuencia
    max_frecuencia = 0
    posibles_modas = []

    for valor in frecuencias:
        if frecuencias[valor] > max_frecuencia:
            max_frecuencia = frecuencias[valor]
            posibles_modas = [valor]
        elif frecuencias[valor] == max_frecuencia:
            posibles_modas.append(valor)

    # En caso de empate, devolvemos la menor moda
    return min(posibles_modas)

# funcion auxiliar para calcular la mayor y menor moda de las preguntas
def pregunta_moda_max_min(temas):
    lista_modas = []

    for tema_nombre in temas:
        tema = temas[tema_nombre]
        for pregunta_id in tema:
            encuestados = list(tema[pregunta_id])
            opiniones = [e[2] for e in encuestados]
            moda_valor = moda(opiniones)
            lista_modas.append((pregunta_id, moda_valor))

    # Inicializamos con la primera
    mayor_moda = lista_modas[0]
    menor_moda = lista_modas[0]

    for item in lista_modas[1:]:
        # Mayor moda
        if item[1] > mayor_moda[1]:
            mayor_moda = item
        elif item[1] == mayor_moda[1] and item[0] < mayor_moda[0]:
            mayor_moda = item

        # Menor moda
        if item[1] < menor_moda[1]:
            menor_moda = item
        elif item[1] == menor_moda[1] and item[0] < menor_moda[0]:
            menor_moda = item

    print(f"\nPregunta con MAYOR valor de moda: {mayor_moda[0]} con moda = {mayor_moda[1]}")
    print(f"Pregunta con MENOR valor de moda: {menor_moda[0]} con moda = {menor_moda[1]}")


# Function to print 
def ordenar_preguntas(K):
    # K is a dictionary where keys are questions and values are sets of encuestados
    M = K.keys()
    # Create a list of tuples where each tuple contains the value
    def obtener_values(key, list):
        lista = []
        if key in list:
            for x in list[key]:
                lista.append(x)
        return lista
    
    # Create a list to store the questions and their corresponding values ordered
    preguntas = []

    # Iterate through each question in K
    for x in M:
        n = obtener_values(x, K)
        #print(f"Pregunta: {x}, Encuesados: {K[x]}")
        promedio = calcular_promedio(n, 2)
        merged = merge_opiniones(n)
        preguntas.append([promedio, x, merged])

    # Sort the preguntas list
    preguntas_organizadas = insertionsort(preguntas)
    return preguntas_organizadas

def ordenar_temas(K, encuestados):
    items = K.items()
    nuevo_arr = []
    for b in items:
        nuevo = ordenar_preguntas(b[1])
        promedio = calcular_promedio(nuevo, 0)
        #print(f"{promedio} {b[0]} :")
        nuevo_arr.append((promedio, b[0],nuevo))

    temas_organizados = insertionsort(nuevo_arr)
    for i in temas_organizados:
        print("\n")
        print(f"{[i[0]]} {i[1]}")
        for j in i[2]:
            values = ()
            for k in j[2]:
                values += (obtener_llave_por_valor(encuestados, k),)
            print(f"{[j[0]]} {j[1]}: {values}")
 
encuestados = {
    1: ("Sofia García", 1, 6),
    2: ("Alejandro Torres", 7, 10),
    3: ("Valentina Rodriguez", 9, 0),
    4: ("Juan Lopéz", 10, 1),
    5: ("Martina Martinez", 7, 0),
    6: ("Sebastian Perez", 8, 9),
    7: ("Camila Fernandez", 2, 7),
    8: ("Mateo Gonzalez", 4, 7),
    9: ("Isabella Díaz", 7, 5),
    10: ("Daniel Ruiz", 2, 9),
    11: ("Luciana Sanchez", 1, 7),
    12: ("Lucas Vasquez", 6, 8)
}

tema_1 = {
    "Pregunta 1.1": {encuestados[10], encuestados[2]},
    "Pregunta 1.2": {encuestados[1], encuestados[9], encuestados[12], encuestados[6]}}
tema_2 = {
    "Pregunta 2.1": {encuestados[11], encuestados[8], encuestados[7]},
    "Pregunta 2.2": {encuestados[3], encuestados[4], encuestados[5]}}

temas = {
    "Tema 1": tema_1,
    "Tema 2": tema_2}

personas = list(encuestados.items())
print("Lista de encuestados ordenada")
ordenar_encuestados(personas)
print("\n")
print("Lista de Temas ordenada")
ordenar_temas(temas, personas)
pregunta_moda_max_min(temas)
opiniones = [6, 7, 7, 3, 3]
print("moda de las opiniones:")
print(moda(opiniones))
"""
Dado que los valores de cada encuetado son una tupla,
se puede acceder a ellos como encuestados[1][0] para el nombre, 
encuestados[1][1] para la experticia y encuestados[1][2] para la opinión.

Si vas a camnbiar algo en el código, asegúrate de comentarlo y escribir por el grupo.
"""
