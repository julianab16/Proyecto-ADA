import os
import sys
from alternativa_dos import (
    ordenar_temas,
    ordenar_encuestados,
    pregunta_mayor_menor_promedio,
    pregunta_moda_max_min,
    calcular_mediana_por_pregunta,
    pregunta_mayor_extremismo,
    pregunta_mayor_consenso
)

# --------------------------------------------------
# Paso 1: procesar encuestados

def procesar_archivo_dos(nombre_archivo,salida_archivo):
    encuestados = {}  # Diccionario con ID -> (nombre, experticia, opinion)
    temas = {}     # Lista de listas de enteros
    with open(nombre_archivo, "r", encoding="utf-8") as archivo:
        lineas = archivo.readlines()

        # Separar en dos secciones: datos de encuestados y temas
    linea_division = 0
    for i, linea in enumerate(lineas):
        if linea.strip().startswith('{'):
            linea_division = i
            break
    
    # Procesar encuestados
    for i, linea in enumerate(lineas[:linea_division]):
        if not linea.strip():
            continue
        partes = linea.strip().split(',')
        nombre = partes[0].strip()
        experticia = int(partes[1].split(':')[1].strip())
        opinion = int(partes[2].split(':')[1].strip())
        encuestados[i + 1] = (nombre, experticia, opinion)
    
    # Procesar temas
    tema_actual = 1
    pregunta_actual = 1
    temas[f"Tema {tema_actual}"] = {}
    
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
            temas[f"Tema {tema_actual}"][f"Pregunta {tema_actual}.{pregunta_actual}"] = {
                encuestados[i] for i in indices
            }
            pregunta_actual += 1
        except:
            print(f"❌ Línea mal formateada: '{linea}' (saltada)")

    os.makedirs(os.path.dirname(salida_archivo), exist_ok=True)
    original_stdout = sys.stdout

    with open(salida_archivo, 'w', encoding='utf-8') as archivo_salida:
        sys.stdout = archivo_salida

        print("Resultados de la encuesta:")
        ordenar_temas(temas, list(encuestados.items()))
        print()
        print("Lista de encuestados:")
        personas = list(encuestados.items())
        ordenar_encuestados(personas)
        print()
        print("Resultados:")
        pregunta_mayor_menor_promedio(temas)
        pregunta_moda_max_min(temas)
        calcular_mediana_por_pregunta(temas)
        pregunta_mayor_extremismo(temas)
        pregunta_mayor_consenso(temas)

        sys.stdout = original_stdout  # Restaura stdout

    print(f"✅ Reporte guardado en {salida_archivo}")
