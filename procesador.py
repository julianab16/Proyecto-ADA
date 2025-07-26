import os
import sys
from alternativa_uno import (
    construir_arbol_y_recorrer,
    temas_ordenados,
    pregunta_mayor_menor_promedio,
    pregunta_moda_max_min_arn,
    calcular_mediana_por_pregunta,
    pregunta_mayor_extremismo,
    pregunta_mayor_consenso
)


def procesar_archivo_uno(nombre_archivo,salida_archivo):
    encuestados = []  # Diccionario con ID -> (nombre, experticia, opinion)
    temas = {}     # Lista de listas de enteros
    with open(nombre_archivo, "r", encoding="utf-8") as archivo:
        lineas = archivo.readlines()

    # Separar en dos secciones: datos de encuestados y temas
    linea_division = 0
    for i, linea in enumerate(lineas):
        if linea.strip().startswith('{'):
            linea_division = i
            break

    for i, linea in enumerate(lineas[:linea_division]):
        if not linea.strip():
            continue
        partes = linea.strip().split(',')
        nombre = partes[0].strip()
        experticia = int(partes[1].split(':')[1].strip())
        opinion = int(partes[2].split(':')[1].strip())
        encuestados.append({
                    "id": i+1,
                    "experticia": experticia,
                    "opinion": opinion,
                    "nombre": nombre
                })

    # Procesar temas
    tema_actual = 1
    pregunta_actual = 1
    temas[f"Tema {tema_actual}"] = {}

    # Creamos diccionario para acceso rápido por ID
    dicc_encuestados = {e["id"]: e for e in encuestados}

    for linea in lineas[linea_division:]:
        linea = linea.strip()
        if not linea:
            tema_actual += 1
            pregunta_actual = 1
            temas[f"Tema {tema_actual}"] = {}
            continue
        try:
            # Convertir línea como conjunto de índices
            indices = list(map(int, linea.strip("{}").split(",")))

            # Verifica si hay algún índice que no está en los encuestados
            indices_invalidos = [i for i in indices if i not in dicc_encuestados]
            if indices_invalidos:
                print(f"❌ Índices fuera de rango en la línea: '{linea}' -> índices inválidos: {indices_invalidos} (saltada)")
                continue

            
            temas[f"Tema {tema_actual}"][f"Pregunta {tema_actual}.{pregunta_actual}"] = [
                    dicc_encuestados[i] for i in indices if i in dicc_encuestados
                ]

            pregunta_actual += 1
        except Exception as e:
            print(f"❌ Línea mal formateada: '{linea}' (saltada). Error: {e}")

    os.makedirs(os.path.dirname(salida_archivo), exist_ok=True)
    original_stdout = sys.stdout

    with open(salida_archivo, 'w', encoding='utf-8') as archivo_salida:
        sys.stdout = archivo_salida

        print("Resultados de la encuesta:")
        temas_ordenados(temas)
        print()
        print("Lista de encuestados:")
        encuestados_ordenados = construir_arbol_y_recorrer(encuestados)
        for e in encuestados_ordenados:
            print(f"({e.id}, Nombre: {e.nombre}, Experticia: {e.experticia}, Opinión: {e.opinion})")
        print()
        print("Resultados:")
        pregunta_mayor_menor_promedio(temas)
        pregunta_moda_max_min_arn(temas)
        calcular_mediana_por_pregunta(temas)
        pregunta_mayor_consenso(temas)
        pregunta_mayor_extremismo(temas)


        sys.stdout = original_stdout  # Restaura stdout

    print(f"✅ Reporte guardado en {salida_archivo}")
    