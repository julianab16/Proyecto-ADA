
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

# Function to get the key from a value in a dictionary
def obtener_llave_por_valor(diccionario, valor_buscado):
    for llave, valor in diccionario:
        if valor == valor_buscado:
            return llave
    return None

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
def calcular_promedio(list):
    n = 0
    for i in list:
        n += i[2]
    promedio = n / len(list)
    return promedio

def insertionsort_preguntas(arr):
    n = len(arr)  # Get the length of the array
     
    if n <= 1:
        return  # If the array has 0 or 1 element, it is already sorted, so return

    for i in range(0, n):  # Iterate over the array starting from the second element
        key = arr[i][0]  # Store the current element as the key to be inserted in the right position
        j = i-1
        while j >= 0 and key > arr[j][0]:  # Move elements greater than key one position ahead
            arr[j+1] = arr[j] # Shift elements to the right
            j -= 1
        arr[j+1][0] = key  # Insert the key in the correct position
    return arr  # Return the sorted array

# Function to print 
def ordernar_preguntas(K, encuestados):
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
        promedio = calcular_promedio(n)
        merged = merge_opiniones(n)
        preguntas.append([promedio, x, merged])

    # Sort the preguntas list
    nuevo_arr = insertionsort_preguntas(preguntas)

    # Print the sorted preguntas
    for u in nuevo_arr:
        values = []
        for i in u[2]:
            values.append(obtener_llave_por_valor(encuestados, i))
        print(f"{u[0]} {u[1]}: {values}")


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

temas = {
    "Tema1": tema_1}

personas = list(encuestados.items())

ordenar_encuestados(personas)
print("\n")
ordernar_preguntas(tema_1, personas)
print("\n")


"""
Falta ordenar los temas

Dado que los valores de cada encuetado son una tupla,
se puede acceder a ellos como encuestados[1][0] para el nombre, 
encuestados[1][1] para la experticia y encuestados[1][2] para la opinión.

Si vas a camnbiar algo en el código, asegúrate de comentarlo y escribir por el grupo.
"""
