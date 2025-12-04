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
    tiempo = reporte['general']['tiempo_carga']
    rows_first = reporte['general']['rows_first']
    rows_last = reporte['general']['rows_last']
    headers = ["Identificador único", "Posición (lat, lon)", "Fecha de creación", "Grullas (tags)", "Conteo de eventos", "Dist. Hídrica Prom (km)"]

    # REPORTE 1: GRAFO DE DISTANCIAS GEOGRÁFICAS
    print("\n" + "="*40)
    print("  GRAFO DE DISTANCIAS GEOGRÁFICAS") 
    print("="*40)
    print(f"Tiempo de carga: {tiempo:.2f} ms") 
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
    print(f"Tiempo de carga: {tiempo:.2f} ms") 
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

def format_row_req_1(item):
    
    punto_id = item["id"]
    if len(punto_id) > 20:
        punto_id = punto_id[:20] + "..."

    posicion = f"({item['lat']:.3f}, {item['lon']:.3f})"
    num_cranes = item.get("num_cranes", 0)

    cranes_first = item.get("cranes_first", [])
    cranes_last = item.get("cranes_last", [])

    if len(cranes_first) == 0:
        first_str = "[]"
    else:
        first_str = ", ".join(cranes_first)

    if len(cranes_last) == 0:
        last_str = "[]"
    else:
        last_str = ", ".join(cranes_last)

    dist_next = item.get("dist_to_next", None)
    if isinstance(dist_next, (int, float)):
        dist_str = f"{dist_next:.3f}"
    else:
        dist_str = "N/A"

    return [punto_id, posicion, num_cranes, first_str, last_str, dist_str]


def format_row_req_4(item):
    
    punto_id = item["id"]
    if len(punto_id) > 20:
        punto_id = punto_id[:20] + "..."

    posicion = f"({item['lat']:.3f}, {item['lon']:.3f})"
    num_cranes = item.get("num_cranes", 0)

    cranes_first = item.get("cranes_first", [])
    cranes_last = item.get("cranes_last", [])

    if len(cranes_first) == 0:
        first_str = "[]"
    else:
        first_str = ", ".join(cranes_first)

    if len(cranes_last) == 0:
        last_str = "[]"
    else:
        last_str = ", ".join(cranes_last)

    edge_weight = item.get("edge_weight", None)
    if isinstance(edge_weight, (int, float)):
        edge_str = f"{edge_weight:.3f}"
    else:
        edge_str = "N/A"

    return [punto_id, posicion, num_cranes, first_str, last_str, edge_str]

def print_req_1(control):
    """
        Función que imprime la solución del Requerimiento 1 en consola
    """
    print("\n" + "="*80)
    print(" REQ. 1: RUTA DFS DE UN INDIVIDUO ENTRE DOS PUNTOS")
    print("="*80)

    # Entradas
    print("\nIngrese coordenadas de ORIGEN:")
    lat_o = float(input(" Latitud: "))
    lon_o = float(input(" Longitud: "))

    print("\nIngrese coordenadas de DESTINO:")
    lat_d = float(input(" Latitud: "))
    lon_d = float(input(" Longitud: "))

    crane_id = input("\nIngrese el identificador (tag) de la grulla: ").strip()

    print("\nBuscando camino con DFS para la grulla seleccionada...\n")

    # Llamada a la lógica
    result = logic.req_1(control, lat_o, lon_o, lat_d, lon_d, crane_id)

    if result.get("error"):
        print(f" Error: {result['message']}")
        return

    # Resumen general
    print(f"Nodo origen más cercano: {result['origin_node']}")
    print(f"Nodo destino más cercano: {result['dest_node']}")
    print(f"Longitud del camino (número de puntos): {result['path_length']}")
    print(f"Distancia total del camino: {result['total_distance']:.3f} km")

    first_node_with_crane = result.get("first_node_with_crane")
    if first_node_with_crane is None:
        print(f"La grulla '{crane_id}' NO aparece en ningún punto del camino DFS.")
    else:
        print(f"Primer nodo del camino donde aparece la grulla '{crane_id}': {first_node_with_crane}")

    print("\n" + "-"*80)
    print("Detalle de los primeros 5 y últimos 5 puntos del camino DFS")
    print("-"*80 + "\n")

    first_nodes = result.get("first_nodes", [])
    last_nodes = result.get("last_nodes", [])

    headers = [
        "ID Punto",
        "Posición (lat, lon)",
        "# Grullas",
        "3 primeras grullas",
        "3 últimas grullas",
        "Dist. sig. (km)"
    ]
    rows = []

    # Agregar primeros 5
    for item in first_nodes:
        rows.append(format_row_req_1(item))

    # Separador si hay camino largo
    path_length = result.get("path_length", 0)
    if path_length > 10 and len(first_nodes) > 0 and len(last_nodes) > 0:
        rows.append(["...", "...", "...", "...", "...", "..."])

    # Agregar últimos 5
    for item in last_nodes:
        rows.append(format_row_req_1(item))

    print(tabulate(rows, headers=headers, tablefmt="psql"))
    print()

def format_row(item):
    grullas_str = str(item['grullas'][:3]) if len(item['grullas']) > 3 else str(item['grullas'])
    return [
        item['id'][:15] + "...",
        f"({item['lat']:.3f}, {item['lon']:.3f})",
        grullas_str,
        f"{item['dist_next']:.3f}"
    ]

def print_req_2(control):
    """
        Función que imprime la solución del Requerimiento 2 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 2
    print("\n" + "="*80)
    print(" REQ. 2: MOVIMIENTOS DE UN NICHO ALREDEDOR DE UN ÁREA (BFS)")
    print("="*80)
    
    # Entradas
    print("\nIngrese coordenadas de ORIGEN:")
    lat_o = float(input(" Latitud: "))
    lon_o = float(input(" Longitud: "))
        
    print("\nIngrese coordenadas de DESTINO:")
    lat_d = float(input(" Latitud: "))
    lon_d = float(input(" Longitud: "))
        
    radio = float(input("\nIngrese el RADIO del área de interés (km): "))
        
    print("\nProcesando con BFS...\n")
        
    # Llamada a lógica
    result = logic.req_2(control, lat_o, lon_o, lat_d, lon_d, radio)

    if result.get("error"):
            print(f" Error: {result['message']}")
            return
    
    # Resultados
    print(f"Camino encontrado")
    print(f"Tiempo de ejecución: {result['time']:.2f} ms") 
    print(f"Total puntos en el camino: {result['total_puntos']}")
    print(f"Camino encontrado")
    print(f"Total puntos en el camino: {result['total_puntos']}")
    print(f"Distancia total recorrida: {result['total_distancia']:.2f} km")
    print(f"Último nodo dentro del radio ({radio} km): {result['last_node_in_radius']}")
    print("-" * 80)
        
    # Tabla Detallada
    detalles = result['path_details']
    headers = ["ID Punto", "Posición", "Grullas", "Eventos", "Dist. Sig (km)"]
    rows = []
        
    # Primeros 5
    for item in detalles[:5]:
        rows.append(format_row(item))
            
    if len(detalles) > 10:
        rows.append(["...", "...", "...", "...", "..."])
            
    # Últimos 5 (evitando duplicados si la lista es corta)
    start_idx = max(5, len(detalles) - 5)
    for item in detalles[start_idx:]:
        rows.append(format_row(item))
             
    print(tabulate(rows, headers=headers, tablefmt="psql"))


def print_req_3(control):
    """
        Función que imprime la solución del Requerimiento 3 en consola
        
        Busca automáticamente todas las rutas migratorias sin pedir datos al usuario
    """
    print("\n" + "="*80)
    print("  REQ. 3: IDENTIFICAR POSIBLES RUTAS MIGRATORIAS")
    print("="*80)
    
    print("\nAnalizando el nicho biologico automaticamente...")
    print("Buscando todas las rutas migratorias en el grafo de movimientos...")
    print("Procesando...\n")
    
    # LLAMADA SIN PARÁMETROS - ANALIZA TODO EL GRAFO
    result = logic.req_3(control)
    
    # Verificar si hubo error
    if result.get("error"):
        print(f"Error: {result['message']}")
        print(f"Tiempo de ejecucion: {result['time']:.2f} ms\n")
        return
    
    print(f"Total de puntos migratorios en el grafo: {result['total_puntos']}")
    print(f"Tiempo de ejecucion: {result['time']:.2f} ms\n")
    
    if result["has_cycles"]:
        print("="*80)
        print("  NO ES POSIBLE REALIZAR ORDEN TOPOLOGICO")
        print("="*80)
        print("  El grafo contiene ciclos (las grullas regresan a puntos anteriores)\n")
        
        if result["cycle_example"]:
            print("Ejemplo de ciclo detectado:")
            print("-" * 80)
            cycle = result["cycle_example"]
            print(f"Numero de nodos en el ciclo: {len(cycle)}")
            print("\nSecuencia del ciclo:")
            
            for i, node in enumerate(cycle):
                if i < len(cycle) - 1:
                    print(f"  {i+1}. Nodo: {node}")
                else:
                    print(f"  -> Regresa a: {node} (completa el ciclo)")
            
            print("\n  Debido a los ciclos, no se pueden identificar rutas migratorias unicas")
            print("  desde un orden topologico.")
    else:
        print("="*80)
        print("El grafo es un DAG (Grafo Aciclico Dirigido)")
        print("="*80)
        print("  Es posible realizar ordenamiento topologico\n")
        
        routes = result["routes"]
        
        if routes:
            print(f"Total de rutas migratorias identificadas: {result['total_rutas']}")
            print("\n" + "="*80)
            print("DETALLE DE LAS RUTAS (MOSTRANDO LAS 5 MAS LARGAS)")
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
                
                print(f"\nPuntos de la ruta (mostrando los 5 primeros y 5 ultimos):")
                
                headers = ["#", "ID Punto", "Posicion", "Grullas", "Eventos", "Dist. Agua (km)", "Dist. siguiente (km)"]
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
                print(f"\n... y {len(routes) - 5} rutas adicionales identificadas")
        else:
            print(f"No se encontraron rutas migratorias en el grafo")
            print("   Posibles causas:")
            print("   - El grafo no tiene nodos fuente o sumidero")
            print("   - Los puntos estan aislados en el grafo")
    
    print("\n" + "="*80)

def print_req_4(control):
    """
        Función que imprime la solución del Requerimiento 4 en consola
    """
    print("\n" + "="*80)
    print(" REQ. 4: CORREDOR HÍDRICO ÓPTIMO (MST CON PRIM)")
    print("="*80)

    # Entradas
    print("\nIngrese coordenadas cercanas a una FUENTE HÍDRICA:")
    lat_o = float(input(" Latitud: "))
    lon_o = float(input(" Longitud: "))

    print("\nConstruyendo corredor hídrico óptimo con Prim...\n")

    # Llamada a la lógica
    result = logic.req_4(control, lat_o, lon_o)

    if result.get("error"):
        print(f" Error: {result['message']}")
        return

    # Resumen general
    print(f"Punto hídrico de origen más cercano: {result['origin_node']}")
    print(f"Total de puntos en el corredor hídrico (MST): {result['total_points']}")
    print(f"Total de individuos (grullas) que usan el corredor: {result['total_individuals']}")
    print(f"Distancia total del corredor (suma de pesos MST): {result['total_distance']:.3f} km")
    print(f"Tiempo de ejecución: {result['time']:.2f} ms")

    print("\n" + "-"*80)
    print("Detalle de los primeros 5 y últimos 5 puntos del corredor hídrico")
    print("-"*80 + "\n")

    first_nodes = result.get("first_nodes", [])
    last_nodes = result.get("last_nodes", [])

    headers = [
        "ID Punto",
        "Posición (lat, lon)",
        "# Grullas",
        "3 primeras grullas",
        "3 últimas grullas",
        "Peso arista MST (km)"
    ]
    rows = []

    # Primeros 5
    for item in first_nodes:
        rows.append(format_row_req_4(item))

    # Separador si el MST es largo
    total_points = result.get("total_points", 0)
    if total_points > 10 and len(first_nodes) > 0 and len(last_nodes) > 0:
        rows.append(["...", "...", "...", "...", "...", "..."])

    # Últimos 5
    for item in last_nodes:
        rows.append(format_row_req_4(item))

    print(tabulate(rows, headers=headers, tablefmt="psql"))
    print()


def print_req_5(control):
    """
        Función que imprime la solución del Requerimiento 5 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 5
    print("\n" + "="*80)
    print(" REQ. 5: RUTA MIGRATORIA MÁS EFICIENTE (DIJKSTRA)")
    print("="*80)
    
    # Entradas
    print("\nIngrese coordenadas de ORIGEN:")
    lat_o = float(input(" Latitud: "))
    lon_o = float(input(" Longitud: "))
        
    print("\nIngrese coordenadas de DESTINO:")
    lat_d = float(input(" Latitud: "))
    lon_d = float(input(" Longitud: "))
        
    print("\nSeleccione criterio de eficiencia:")
    print(" 1. Distancia de desplazamiento")
    print(" 2. Distancia a fuentes hídricas")
    opt = input(" Opción (1/2): ")
        
    criterio = "distancia" if opt == "1" else "agua"
        
    print(f"\nCalculando ruta óptima por '{criterio}'...\n")
        
    # Llamada a lógica
    result = logic.req_5(control, lat_o, lon_o, lat_d, lon_d, criterio)

    if result.get("error"):
            print(f" Error: {result['message']}")
            return
    
    # Resultados Generales
    print(f"Ruta óptima encontrada")
    print(f"Tiempo de ejecución: {result['time']:.2f} ms")
    print(f"Costo Total ({criterio}): {result['costo_total']:.4f}")
    print(f"Total Puntos (Vértices): {result['total_puntos']}")
    print(f"Total Segmentos (Arcos): {result['total_segmentos']}")
    print("-" * 80)
        
    # Tabla
    detalles = result['path_details']
    headers = ["ID Punto", "Posición", "Grullas", "Dist. Geográfica Sig (km)"]
    rows = []
        
    # Primeros 5
    for item in detalles[:5]:
        rows.append(format_row(item))
            
    if len(detalles) > 10:
        rows.append(["...", "...", "...", "..."])
            
    # Últimos 5
    start_idx = max(5, len(detalles) - 5)
    for item in detalles[start_idx:]:
        rows.append(format_row(item))
             
    print(tabulate(rows, headers=headers, tablefmt="psql"))

def print_req_6(control):
    """
        Función que imprime la solución del Requerimiento 6 en consola
        
        Busca automáticamente la subred hídrica más grande sin pedir datos al usuario
    """
    print("\n" + "="*80)
    print("  REQ. 6: IDENTIFICAR POSIBLES SUBREDES HIDRICAS AISLADAS")
    print("="*80)
    
    print("\nAnalizando el nicho biologico automaticamente...")
    print("   (Grafo con todos los puntos migratorios respecto a fuentes hidricas)")
    print("\nProcesando identificacion de subredes hidricas...")
    print("Buscando componentes conectados (grupos aislados de grullas)...\n")
    
    # LLAMADA SIN PARÁMETROS - BUSCA AUTOMÁTICAMENTE
    result = logic.req_6(control)
    
    # Verificar si hubo error
    if result.get("error"):
        print(f"Error: {result['message']}")
        print(f"Tiempo de ejecucion: {result['time']:.2f} ms\n")
        return
    
    print(f"Analisis completado exitosamente")
    print(f"Tiempo de ejecucion: {result['time']:.2f} ms\n")
    
    print("="*80)
    print("RESUMEN DEL NICHO BIOLOGICO")
    print("="*80)
    print(f"Total de puntos migratorios en el grafo: {result.get('total_puntos', 0)}")
    print(f"Total de arcos (conexiones) en el grafo: {result.get('total_arcos', 0)}")
    print(f"Total de subredes hidricas identificadas: {result.get('total_subredes', 0)}")
    
    # Mostrar cual es la subred mas grande
    if result.get('subred_mas_grande'):
        print(f"\nSUBRED MAS GRANDE: Subred #{result['subred_mas_grande']} con {result['puntos_subred_mas_grande']} puntos migratorios")
    print()
    
    if result["total_subredes"] == 0:
        print("  No se identificaron subredes hídricas en el grafo.")
        return
    
    # Mostrar las 5 subredes mas grandes
    print("="*80)
    print("DETALLE DE LAS 5 SUBREDES MAS GRANDES")
    print("="*80 + "\n")
    
    subredes_mostrar = result.get("subredes", [])[:5]
    
    for subred in subredes_mostrar:
        print(f"{'─'*80}")
        print(f"SUBRED #{subred['id']}")
        print(f"{'─'*80}")
        print(f"Total de puntos migratorios: {subred['total_puntos']}")
        print(f"Total de individuos (grullas): {subred['total_grullas']}")
        
        # Mostrar limites geograficos
        print(f"\nLimites geograficos de la subred:")
        print(f"  Latitud  -> Maxima: {subred['lat_max']:.4f} | Minima: {subred['lat_min']:.4f}")
        print(f"  Longitud -> Maxima: {subred['lon_max']:.4f} | Minima: {subred['lon_min']:.4f}")
        print(f"  Longitud latitudinal: {subred['longitud_lat']:.4f} grados")
        print(f"  Longitud longitudinal: {subred['longitud_lon']:.4f} grados")
        
        # Mostrar informacion de grullas
        print(f"\nIndividuos que utilizan esta subred:")
        if len(subred['grullas_primeros_3']) <= 3 and subred['total_grullas'] <= 6:
            # Si hay 6 o menos grullas, mostrar todas
            print(f"  Grullas: {', '.join(subred['grullas_primeros_3'])}")
        else:
            # Mostrar primeros 3 y ultimos 3
            primeros = ', '.join(subred['grullas_primeros_3'])
            ultimos = ', '.join(subred['grullas_ultimos_3'])
            print(f"  Primeros 3: {primeros}")
            print(f"  Ultimos 3: {ultimos}")
        
        # Tabla con primeros 3 puntos migratorios
        print(f"\nPrimeros 3 puntos migratorios de la subred:")
        headers_nodos = ["ID Punto", "Posicion (lat, lon)", "Fecha", "# Grullas", "# Eventos", "Dist. Agua (km)"]
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
        
        # Tabla con ultimos 3 puntos migratorios
        print(f"\nUltimos 3 puntos migratorios de la subred:")
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
