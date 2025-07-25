import re
import os
import sys
from Logica.alternativa_uno import (
    pregunta_mayor_menor_promedio,
    pregunta_moda_max_min_arn,
    calcular_mediana_por_pregunta,
    pregunta_mayor_extremismo,
    pregunta_mayor_consenso
)

def calcular_promedio(lista, clave):
    return round(sum(e[clave] for e in lista) / len(lista), 2)

def pregunta_mayor_menor_experticia(temas):
    resultados = []
    for tema in temas.values():
        for pregunta, encs in tema.items():
            promedio = sum(e["experticia"] for e in encs) / len(encs)
            resultados.append((pregunta, round(promedio, 2)))
    mayor = max(resultados, key=lambda x: (x[1], -ord(x[0][0])))
    menor = min(resultados, key=lambda x: (x[1], x[0]))
    print(f"  Pregunta con mayor promedio de experticia: [{mayor[1]}] Pregunta: {mayor[0]}")
    print(f"  Pregunta con menor promedio de experticia: [{menor[1]}] Pregunta: {menor[0]}")

def procesar_archivo(input_path, output_path, modo="uno"):
    with open(input_path, "r", encoding="utf-8") as f:
        lineas = [line.strip() for line in f if line.strip()]

    encuestados = {}
    bloques = []
    current_id = 1

    # Separar encuestados y bloques
    for linea in lineas:
        if "{" in linea and "}" in linea:
            bloque = eval(linea.strip())
            bloques.append(bloque)
        else:
            match = re.match(r"(.*),\s*Experticia:\s*(\d+),\s*Opinión:\s*(\d+)", linea)
            if match:
                nombre, exp, op = match.groups()
                encuestados[current_id] = {
                    "id": current_id,
                    "nombre": nombre.strip(),
                    "experticia": int(exp),
                    "opinion": int(op)
                }
                current_id += 1

    if len(bloques) % 2 != 0:
        raise ValueError(f"Se esperaban un número par de bloques (pares de preguntas), pero se encontraron {len(bloques)}")

    # Generar temas y preguntas dinámicamente
    temas = {}
    num_temas = len(bloques) // 2
    for i in range(num_temas):
        temas[f"Tema {i+1}"] = {
            f"Pregunta {i+1}.1": [encuestados[j] for j in bloques[2*i]],
            f"Pregunta {i+1}.2": [encuestados[j] for j in bloques[2*i + 1]],
        }

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    original_stdout = sys.stdout

    with open(output_path, "w", encoding="utf-8") as salida:
        sys.stdout = salida

        print("Resultados de la encuesta:\n")

        for tema_nombre, preguntas in temas.items():
            promedio_tema = calcular_promedio([e for p in preguntas.values() for e in p], "opinion")
            print(f"[{promedio_tema}] {tema_nombre}:")
            for pregunta, encs in preguntas.items():
                promedio = calcular_promedio(encs, "opinion")
                ids = tuple(sorted(e["id"] for e in encs))
                print(f" [{promedio}] {pregunta}: {ids}")
            print()

        print("Lista de encuestados:")
        lista_encuestados = sorted(encuestados.values(), key=lambda e: (-e["experticia"], -e["id"]))
        for e in lista_encuestados:
            print(f" ({e['id']}, Nombre:'{e['nombre']}', Experticia:{e['experticia']}, Opinión:{e['opinion']})")
        print()

        print("Resultados:")
        pregunta_mayor_menor_promedio(temas)
        pregunta_mayor_menor_experticia(temas)
        calcular_mediana_por_pregunta(temas)
        pregunta_moda_max_min_arn(temas)
        pregunta_mayor_extremismo(temas)
        pregunta_mayor_consenso(temas)

    sys.stdout = original_stdout
    print(f"\n✅ Archivo generado correctamente: {output_path}")