
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

# Merge que ordena las medianas
def merge_medianas(lista):
    if len(lista) <= 1:
        return lista
    mid = len(lista) // 2

    def merge_sorted(left, right):
        merged = []
        while left and right:
            # Compara primero por mediana (valor en posición [1])
            if left[0][1] < right[0][1]:
                merged.append(left.pop(0))
            elif left[0][1] == right[0][1]:
                # En caso de empate, usar el identificador de pregunta (posición [0]) en orden alfabético
                if left[0][0] < right[0][0]:
                    merged.append(left.pop(0))
                else:
                    merged.append(right.pop(0))
            else:
                merged.append(right.pop(0))

        merged.extend(left or right)
        return merged
    return merge_sorted(merge_medianas(lista[:mid]), merge_medianas(lista[mid:]))

# Function outs the list of IDs ordered
def ordenar_encuestados(arr):
    merged = merge_encuestados(arr)
    for id, (nombre, experticia, opinion) in merged:
        print(f"({id}, Nombre: {nombre}, Experticia: {experticia}, Opinión: {opinion})")

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

# Function to calculate the average
def calcular_promedio(list, j):
    n = 0
    for i in list:
        n += i[j]
    promedio = n / len(list)
    promedio_redondeado = round(promedio, 2)
    return promedio_redondeado

# Function to print the question in order
def ordenar_preguntas(K):
    # K is a dictionary where keys are questions and values are sets of encuestados
    M = K.keys()
    # Create a list to store the questions and their corresponding values ordered
    preguntas = []
    # Iterate through each question in K
    for x in M:
        # Calcula el promedio
        promedio = calcular_promedio(K[x], 2)
        # Organiza las opniones
        merged = merge_opiniones(list(K[x]))
        preguntas.append([promedio, x, merged])

    # Sort the preguntas list
    preguntas_organizadas = insertionsort(preguntas)
    return preguntas_organizadas

# Function to get the key from a value in a dictionary
def obtener_llave_por_valor(diccionario, valor_buscado):
    for llave, valor in diccionario:
        if valor == valor_buscado:
            return llave
    return None

# Ordena los temas por promedio de preguntas
def ordenar_temas(K, encuestados):
    items = K.items() #Saca las llaves de la lista
    nuevo_arr = []
    for tema in items:
        #ordena los preguntas primero
        nuevo = ordenar_preguntas(tema[1])
        #calcula el promedio de cada tema
        promedio = calcular_promedio(nuevo, 0)
        nuevo_arr.append((promedio, tema[0], nuevo))

    #ordena cada tema dependiendo de su promedio 
    temas_organizados = insertionsort(nuevo_arr)
    for tema in temas_organizados:
        #improme promedio y tema
        print(f"[{tema[0]:.2f}] {tema[1]}")
        for pregunta in tema[2]:
            values = ()
            for encuestado in pregunta[2]:
                #Saca los IDs de cada encuestado
                values += (obtener_llave_por_valor(encuestados, encuestado),)
            #impreme el promedio de prehunta, pregunta y Id de los encuestados
            print(f" [{pregunta[0]:.2f}] {pregunta[1]}: {values}")

# Función para encontrar la pregunta con mayor y menor promedio de las opiniones
def pregunta_mayor_menor_promedio(temas):
    promedios = []
    for tema_nombre in temas:
        preguntas = temas[tema_nombre]
        for pregunta_id in preguntas:
            encuestados = list(preguntas[pregunta_id])
            opiniones = [e[2] for e in encuestados]
            if opiniones:
                promedio = sum(opiniones) / len(opiniones)
                promedios.append((pregunta_id, promedio))
    if not promedios:
        print("No hay preguntas con opiniones")
        return

    mayor = max(promedios, key=lambda x: (x[1], -ord(x[0][0])))
    menor = min(promedios, key=lambda x: (x[1], x[0]))

    print(f"Pregunta con mayor promedio de opinion: [{mayor[1]:.2f}] {mayor[0]}")
    print(f"Pregunta con menor promedio de opinion: [{menor[1]:.2f}] {menor[0]}")


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

# Funcion auxiliar para calcular la mayor y menor moda de las preguntas
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

    print(f"Pregunta con mayor moda de opinion: [{mayor_moda[1]}] {mayor_moda[0]}")
    print(f"Pregunta con menor moda de opinion: [{menor_moda[1]}] {menor_moda[0]}")

# función para calcular la pregunta con mayor consenso en esta estructura
def pregunta_mayor_consenso(temas):
     # Inicializamos la mejor pregunta y el consenso más alto
    mejor_pregunta = None
    mejor_consenso = -1.0

    # Recorremos cada tema
    for tema_nombre in temas:
        preguntas = temas[tema_nombre]
         # Recorremos cada pregunta en ese tema
        for pregunta_id in preguntas:
            encuestados = list(preguntas[pregunta_id])
            # Extraemos las opiniones de los encuestados (posición 2 en la tupla)
            opiniones = [e[2] for e in encuestados]
            if not opiniones:
                continue

             # Calculamos la moda de las opiniones con la funcion    
            moda_valor = moda(opiniones)
             
             # Contamos cuántos encuestados dieron esa opinión
            cantidad_moda = opiniones.count(moda_valor)
            total = len(opiniones)
           
             # Calculamos el porcentaje de consenso
            consenso = cantidad_moda / total  

            # Verificamos si esta pregunta tiene mayor consenso que la actual mejor
            if consenso > mejor_consenso or (consenso == mejor_consenso and pregunta_id < mejor_pregunta):
                mejor_consenso = consenso
                mejor_pregunta = pregunta_id

    # Mostramos la mejor pregunta encontrada y su porcentaje de consenso
    porcentaje = round(mejor_consenso * 100, 2)
    print(f"Pregunta con mayor consenso: {mejor_pregunta} con {porcentaje}%")
    
# Funcion para calcular la mediana
def calcular_mediana(lista):
    n = len(lista)
    if n % 2 == 1:
        return lista[n // 2]
    else:
        return (lista[n // 2 - 1] + lista[n // 2]) // 2
    
# Funcion que calcula la mediana mayor y menor
def calcular_mediana_por_pregunta(temas):
    items = temas.items() # Saca los valores del diccionario
    nuevo_array = []
    for b in items:
        # Ordena las preguntas
        nuevo = ordenar_preguntas(b[1])
        for n in nuevo:
            # Guarda la pregunta y encuestados
            nuevo_array.append((n[1], n[2]))

    # Itera el arreglo de nuevo_array 
    for i, (pregunta_nombre, op) in enumerate(nuevo_array):
        # Guarda las opiniones de cada pregunta
        opiniones = [e[2] for e in op]
        # Calcula la mediana
        mediana = calcular_mediana(opiniones)
        # Reemplazar la lista de opiniones por la mediana
        nuevo_array[i] = (pregunta_nombre, mediana)  

    # Ordena las medianas
    medianas_ordenadas = merge_medianas(nuevo_array)
    # Mediana mayor y menor
    mayor_pregunta, mayor = medianas_ordenadas[-1]
    menor_pregunta, menor = medianas_ordenadas[0]
    
    print(f"Pregunta con mayor mediana de opinion: [{mayor}] Pregunta: {mayor_pregunta[9:]}")
    print(f"Pregunta con menor mediana de opinion: [{menor}] Pregunta: {menor_pregunta[9:]}")

def pregunta_mayor_extremismo(temas):
    """
    Encuentra la pregunta con mayor extremismo, donde extremismo es el porcentaje
    de opiniones 0 o 10 respecto al total de opiniones en cada pregunta.
    """
    mayor_extremismo = None
    pregunta_mayor = None

    for tema_nombre in temas:
        preguntas = temas[tema_nombre]
        for pregunta_id in preguntas:
            encuestados = list(preguntas[pregunta_id])
            total = len(encuestados)
            if total == 0:
                continue
            # Opinión está en la posición 2 de la tupla
            extremos = sum(1 for e in encuestados if e[2] == 0 or e[2] == 10)
            porcentaje = extremos / total
            if (mayor_extremismo is None) or (porcentaje > mayor_extremismo) or (porcentaje == mayor_extremismo and pregunta_id < pregunta_mayor):
                mayor_extremismo = porcentaje
                pregunta_mayor = pregunta_id

    if pregunta_mayor is not None:
        print(f"Pregunta con mayor extremismo: {pregunta_mayor} con {mayor_extremismo*100:.2f}%")
    else:
        print("\nNo hay preguntas con extremismo.")

encuestados = {
    1: ("Diego Morales", 5, 8),
    2: ("Laura Jiménez", 8, 6),
    3: ("Pedro Suárez", 10, 9),
    4: ("Carolina Rojas", 4, 0),
    5: ("Andrés Cárdenas", 6, 7),
    6: ("Marcela Gómez", 7, 8),
    7: ("Pablo Castillo", 9, 4),
    8: ("Diana Martínez", 2, 1),
    9: ("Santiago Reyes", 1, 6),
    10: ("María Cano", 8, 0),
    11: ("Ana Mejía", 3, 7),
    12: ("Luis Vargas", 10, 10),
    13: ("Verónica López", 6, 1),
    14: ("Daniela Torres", 5, 4),
    15: ("Ricardo Pérez", 7, 6),
    16: ("Jessica Sandoval", 4, 9),
    17: ("Juan Álvarez", 8, 0),
    18: ("Felipe Mendoza", 9, 8),
    19: ("Gloria Ramírez", 3, 7),
    20: ("Héctor Orozco", 2, 6)
}

personas = list(encuestados.items())


"""
Dado que los valores de cada encuestado son una tupla,
se puede acceder a ellos como encuestados[1][0] para el nombre, 
encuestados[1][1] para la experticia y encuestados[1][2] para la opinión.

Si vas a camnbiar algo en el código, asegúrate de comentarlo y escribir por el grupo.
"""