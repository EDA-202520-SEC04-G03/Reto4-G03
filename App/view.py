import sys
from App import logic
from tabulate import tabulate

def new_logic():
    """
        Se crea una instancia del controlador
    """
    #TODO: Llamar la función de la lógica donde se crean las estructuras de datos
    return logic.new_logic()

def print_menu():
    print("Bienvenido")
    print("0- Cargar información")
    print("1- Ejecutar Requerimiento 1")
    print("2- Ejecutar Requerimiento 2")
    print("3- Ejecutar Requerimiento 3")
    print("4- Ejecutar Requerimiento 4")
    print("5- Ejecutar Requerimiento 5")
    print("6- Ejecutar Requerimiento 6")
    print("7- Salir")

def load_data(control):
    """
    Carga los datos
    """
    #TODO: Realizar la carga de datos
    print("Seleccione el tamaño del archivo que quiere cargar:\n")
    print("1. 1000_cranes_mongolia_large.csv")
    print("2. 1000_cranes_mongolia_small.csv")
    print("3. 1000_cranes_mongolia_30pct.csv")
    print("4. 1000_cranes_mongolia_80pct.csv\n")

    tamano_archivo = int(input("Que tamaño de archivo quieres usar? (ingresa el número): "))
    cranes_file = 1
    if tamano_archivo == 1:
        cranes_file = "1000_cranes_mongolia_large.csv"
    if tamano_archivo == 2:
        cranes_file = "1000_cranes_mongolia_small.csv"
    if tamano_archivo == 3:
        cranes_file = "1000_cranes_mongolia_30pct.csv"
    if tamano_archivo == 4:
        cranes_file = "1000_cranes_mongolia_80pct.csv"
    
    print("\nCargando información de los archivos ....\n")

    datos, reporte = logic.load_data(control, cranes_file)
    
    # Datos comunes
    grullas = reporte['general']['total_grullas']
    eventos = reporte['general']['total_eventos']
    rows_first = reporte['general']['rows_first']
    rows_last = reporte['general']['rows_last']
    headers = ["Identificador único", "Posición (lat, lon)", "Fecha de creación", "Grullas (tags)", "Conteo de eventos", "Dist. Hídrica Prom (km)"]

    # REPORTE 1: GRAFO DE DISTANCIAS GEOGRÁFICAS
    print("\n" + "="*40)
    print("  GRAFO DE DISTANCIAS GEOGRÁFICAS") 
    print("="*40)
    print(f"Total Grullas reconocidas: {grullas}")
    print(f"Total de eventos cargados: {eventos}")
    print(f"Total de nodos del grafo: {reporte['distancia']['nodos']}")
    print(f"Total de arcos en el grafo: {reporte['distancia']['arcos']}")
    print("\n" + "="*40)
    print("DETALLE DE NODOS (VÉRTICES)")
    print("="*40 + "\n")

    print("--- Primeros 5 Nodos ---")
    print(tabulate(rows_first, headers=headers, tablefmt="psql"))
    print("\n")
    print("--- Últimos 5 Nodos ---")
    print(tabulate(rows_last, headers=headers, tablefmt="psql"))
    print("\n")

    # REPORTE 2: GRAFO DE FUENTES HÍDRICAS
    print("\n" + "="*40)
    print("  GRAFO DE FUENTES HÍDRICAS") 
    print("="*40)
    print(f"Total Grullas reconocidas: {grullas}")
    print(f"Total de eventos cargados: {eventos}")
    print(f"Total de nodos del grafo: {reporte['agua']['nodos']}")
    print(f"Total de arcos en el grafo: {reporte['agua']['arcos']}")
    print("\n" + "="*40)
    print("DETALLE DE NODOS (VÉRTICES)")
    print("="*40 + "\n")
    
    # Imprimimos la misma tabla porque los nodos contienen la misma info base
    print("--- Primeros 5 Nodos ---")
    print(tabulate(rows_first, headers=headers, tablefmt="psql"))
    print("\n")
    print("--- Últimos 5 Nodos ---")
    print(tabulate(rows_last, headers=headers, tablefmt="psql"))
    print("\nCarga finalizada exitosamente.")
    
    return datos

def print_data(control, id):
    """
        Función que imprime un dato dado su ID
    """
    #TODO: Realizar la función para imprimir un elemento
    pass

def print_req_1(control):
    """
        Función que imprime la solución del Requerimiento 1 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 1
    pass


def print_req_2(control):
    """
        Función que imprime la solución del Requerimiento 2 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 2
    pass


def print_req_3(control):
    """
        Función que imprime la solución del Requerimiento 3 en consola
    """
    print("\n" + "="*80)
    print("  REQ. 3: IDENTIFICAR POSIBLES RUTAS MIGRATORIAS")
    print("="*80)
    
    # Pedir el punto de origen al usuario
    punto_origen = input("\nIngrese el identificador del punto migratorio de origen: ").strip()
    
    if not punto_origen:
        print("\n Error: Debe ingresar un punto de origen válido")
        return
    
    print(f"\nBuscando rutas migratorias desde el punto: {punto_origen}")
    print("Procesando...\n")
    
    result = logic.req_3(control, punto_origen)
    
    # Verificar si hubo error
    if result.get("error"):
        print(f" {result['message']}")
        print(f"Tiempo de ejecución: {result['time']:.2f} ms\n")
        return
    
    print(f"Total de puntos migratorios en el grafo: {result['total_puntos']}")
    print(f"Tiempo de ejecución: {result['time']:.2f} ms\n")
    
    if result["has_cycles"]:
        print("  NO ES POSIBLE REALIZAR ORDEN TOPOLÓGICO")
        print("    El grafo contiene ciclos (las grullas regresan a puntos anteriores)\n")
        
        if result["cycle_example"]:
            print("Ejemplo de ciclo detectado:")
            print("-" * 80)
            cycle = result["cycle_example"]
            print(f"Número de nodos en el ciclo: {len(cycle)}")
            print("\nSecuencia del ciclo:")
            
            for i, node in enumerate(cycle):
                if i < len(cycle) - 1:
                    print(f"  {i+1}. Nodo: {node}")
                else:
                    print(f"  → Regresa a: {node} (completa el ciclo)")
            
            print("\n  Debido a los ciclos, no se pueden identificar rutas migratorias únicas")
            print("    desde el punto de origen especificado.")
    else:
        print("✓ El grafo es un DAG (Grafo Acíclico Dirigido)")
        print("  Es posible realizar ordenamiento topológico\n")
        
        routes = result["routes"]
        
        if routes:
            print(f"Total de rutas migratorias desde '{punto_origen}': {result['total_rutas']}")
            print("\n" + "="*80)
            print("DETALLE DE LAS RUTAS (MOSTRANDO LAS 5 MÁS LARGAS)")
            print("="*80 + "\n")
            
            # Mostrar las primeras 5 rutas (o menos si hay menos)
            for idx, route in enumerate(routes[:5], 1):
                print(f"\n{'─'*80}")
                print(f"RUTA #{idx}")
                print(f"{'─'*80}")
                print(f"Total de puntos en la ruta: {route['total_points']}")
                print(f"Total de individuos (grullas) que usan esta ruta: {route['total_cranes']}")
                print(f"Distancia total de la ruta: {route['total_distance']:.2f} km")
                print(f"\nOrigen: {route['origin']}")
                print(f"Destino: {route['destination']}")
                
                # Mostrar primeros 5 y últimos 5 puntos
                path_details = route['path_details']
                
                print(f"\nPuntos de la ruta (mostrando los 5 primeros y 5 últimos):")
                
                headers = ["#", "ID Punto", "Posición", "Grullas", "Eventos", "Dist. Agua (km)", "Dist. siguiente (km)"]
                rows = []
                
                # Primeros 5
                limit_first = min(5, len(path_details))
                for i in range(limit_first):
                    point = path_details[i]
                    pos_str = f"({point['position'][0]:.4f}, {point['position'][1]:.4f})"
                    dist_next = f"{point.get('distance_to_next', 'N/A'):.2f}" if isinstance(point.get('distance_to_next'), (int, float)) else "N/A"
                    
                    rows.append([
                        i+1,
                        point['id'][:20] + "..." if len(point['id']) > 20 else point['id'],
                        pos_str,
                        point['cranes_count'],
                        point['events_count'],
                        f"{point['water_distance']:.2f}",
                        dist_next
                    ])
                
                # Separador si hay más de 10 puntos
                if len(path_details) > 10:
                    rows.append(["...", "...", "...", "...", "...", "...", "..."])
                    
                    # Últimos 5
                    start_last = max(limit_first, len(path_details) - 5)
                    for i in range(start_last, len(path_details)):
                        point = path_details[i]
                        pos_str = f"({point['position'][0]:.4f}, {point['position'][1]:.4f})"
                        dist_next = f"{point.get('distance_to_next', 'N/A'):.2f}" if isinstance(point.get('distance_to_next'), (int, float)) else "N/A"
                        
                        rows.append([
                            i+1,
                            point['id'][:20] + "..." if len(point['id']) > 20 else point['id'],
                            pos_str,
                            point['cranes_count'],
                            point['events_count'],
                            f"{point['water_distance']:.2f}",
                            dist_next
                        ])
                
                print(tabulate(rows, headers=headers, tablefmt="psql"))
                
                # Mostrar las primeras 3 y últimas 3 grullas
                cranes = route['cranes']
                if len(cranes) <= 6:
                    cranes_str = ", ".join(cranes)
                else:
                    cranes_str = ", ".join(cranes[:3]) + " ... " + ", ".join(cranes[-3:])
                
                print(f"\nGrullas que transitan (muestra): {cranes_str}")
                
                # Calcular distancia promedio a vértices vecinos
                distances = [p.get('distance_to_next', 0) for p in path_details if 'distance_to_next' in p]
                if distances:
                    avg_distance = sum(distances) / len(distances)
                    print(f"Distancia promedio entre puntos consecutivos: {avg_distance:.2f} km")
            
            # Resumen final
            if len(routes) > 5:
                print(f"\n... y {len(routes) - 5} rutas adicionales desde el punto de origen")
        else:
            print(f" No se encontraron rutas migratorias desde el punto '{punto_origen}'")
            print("   Posibles causas:")
            print("   - El punto no tiene conexiones salientes")
            print("   - El punto está aislado en el grafo")
    
    print("\n" + "="*80)

def print_req_4(control):
    """
        Función que imprime la solución del Requerimiento 4 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 4
    pass


def print_req_5(control):
    """
        Función que imprime la solución del Requerimiento 5 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 5
    pass


def print_req_6(control):
    """
        Función que imprime la solución del Requerimiento 6 en consola
        
        Solicita al usuario el punto migratorio de origen para analizar las subredes
    """
    print("\n" + "="*80)
    print("  REQ. 6: IDENTIFICAR POSIBLES SUBREDES HÍDRICAS AISLADAS")
    print("="*80)
    
    # Solicitar el punto de origen al usuario
    punto_origen = input("\nIngrese el identificador del punto migratorio de origen: ").strip()
    
    if not punto_origen:
        print("\n Error: Debe ingresar un punto de origen válido")
        return
    
    print(f"\n📊 Analizando el nicho biológico desde el punto: {punto_origen}")
    print("   (Grafo con todos los puntos migratorios respecto a fuentes hídricas)")
    print("\nProcesando identificación de subredes hídricas...")
    print("Buscando componentes conectados (grupos aislados de grullas)...\n")
    
    result = logic.req_6(control, punto_origen)
    
    # Verificar si hubo error
    if result.get("error"):
        print(f" {result['message']}")
        print(f"Tiempo de ejecución: {result['time']:.2f} ms\n")
        return
    
    print(f"✓ Análisis completado exitosamente")
    print(f"Tiempo de ejecución: {result['time']:.2f} ms\n")
    
    print("="*80)
    print("RESUMEN DEL NICHO BIOLÓGICO")
    print("="*80)
    print(f"Punto migratorio de origen analizado: {result.get('punto_origen', 'N/A')}")
    print(f"Total de puntos migratorios en el grafo: {result.get('total_puntos', 0)}")
    print(f"Total de arcos (conexiones) en el grafo: {result.get('total_arcos', 0)}")
    print(f"Total de subredes hídricas identificadas: {result.get('total_subredes', 0)}")
    print()
    
    if result["total_subredes"] == 0:
        print("  No se identificaron subredes hídricas en el grafo.")
        return
    
    # Mostrar las 5 subredes más grandes
    print("="*80)
    print("DETALLE DE LAS 5 SUBREDES MÁS GRANDES")
    print("="*80 + "\n")
    
    subredes_mostrar = result.get("subredes", [])[:5]
    
    for subred in subredes_mostrar:
        print(f"{'─'*80}")
        print(f"SUBRED #{subred['id']}")
        print(f"{'─'*80}")
        print(f"Total de puntos migratorios: {subred['total_puntos']}")
        print(f"Total de individuos (grullas): {subred['total_grullas']}")
        
        # Mostrar límites geográficos
        print(f"\nLímites geográficos de la subred:")
        print(f"  Latitud  → Máxima: {subred['lat_max']:.4f} | Mínima: {subred['lat_min']:.4f}")
        print(f"  Longitud → Máxima: {subred['lon_max']:.4f} | Mínima: {subred['lon_min']:.4f}")
        print(f"  Longitud latitudinal: {subred['longitud_lat']:.4f} grados")
        print(f"  Longitud longitudinal: {subred['longitud_lon']:.4f} grados")
        
        # Mostrar información de grullas
        print(f"\nIndividuos que utilizan esta subred:")
        if len(subred['grullas_primeros_3']) <= 3 and subred['total_grullas'] <= 6:
            # Si hay 6 o menos grullas, mostrar todas
            print(f"  Grullas: {', '.join(subred['grullas_primeros_3'])}")
        else:
            # Mostrar primeros 3 y últimos 3
            primeros = ', '.join(subred['grullas_primeros_3'])
            ultimos = ', '.join(subred['grullas_ultimos_3'])
            print(f"  Primeros 3: {primeros}")
            print(f"  Últimos 3: {ultimos}")
        
        # Tabla con primeros 3 puntos migratorios
        print(f"\nPrimeros 3 puntos migratorios de la subred:")
        headers_nodos = ["ID Punto", "Posición (lat, lon)", "Fecha", "# Grullas", "# Eventos", "Dist. Agua (km)"]
        rows_primeros = []
        
        for nodo in subred['primeros_3']:
            rows_primeros.append([
                nodo['id'][:25] + "..." if len(nodo['id']) > 25 else nodo['id'],
                f"({nodo['lat']:.4f}, {nodo['lon']:.4f})",
                str(nodo['timestamp']),
                nodo['cranes_count'],
                nodo['events_count'],
                f"{nodo['water_distance']:.2f}"
            ])
        
        print(tabulate(rows_primeros, headers=headers_nodos, tablefmt="psql"))
        
        # Tabla con últimos 3 puntos migratorios
        print(f"\nÚltimos 3 puntos migratorios de la subred:")
        rows_ultimos = []
        
        for nodo in subred['ultimos_3']:
            rows_ultimos.append([
                nodo['id'][:25] + "..." if len(nodo['id']) > 25 else nodo['id'],
                f"({nodo['lat']:.4f}, {nodo['lon']:.4f})",
                str(nodo['timestamp']),
                nodo['cranes_count'],
                nodo['events_count'],
                f"{nodo['water_distance']:.2f}"
            ])
        
        print(tabulate(rows_ultimos, headers=headers_nodos, tablefmt="psql"))
        print()
    
    # Resumen final
    if result.get('total_subredes', 0) > 5:
        print(f"\n{'='*80}")
        print(f"... y {result['total_subredes'] - 5} subredes adicionales identificadas")
        print("(Se muestran solo las 5 más grandes)")
    
    print("\n" + "="*80)

# Se crea la lógica asociado a la vista
control = new_logic()

# main del ejercicio
def main():
    """
    Menu principal
    """
    working = True
    #ciclo del menu
    while working:
        print_menu()
        inputs = input('Seleccione una opción para continuar\n')
        if int(inputs) == 0:
            data = load_data(control)
        elif int(inputs) == 1:
            print_req_1(control)

        elif int(inputs) == 2:
            print_req_2(control)

        elif int(inputs) == 3:
            print_req_3(control)

        elif int(inputs) == 4:
            print_req_4(control)

        elif int(inputs) == 5:
            print_req_5(control)

        elif int(inputs) == 6:
            print_req_6(control)

        elif int(inputs) == 7:
            working = False
            print("\nGracias por utilizar el programa") 
        else:
            print("Opción errónea, vuelva a elegir.\n")
    sys.exit(0)
