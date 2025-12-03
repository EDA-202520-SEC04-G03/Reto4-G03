import time as pytime
import csv
import os
import math
from datetime import datetime, date, time as dtime, timedelta
from DataStructures.List import array_list as lt
from DataStructures.Map import map_linear_probing as mp
from DataStructures.Graph import bfs
from DataStructures.Graph import digraph
from DataStructures.Graph import dfs
from DataStructures.Graph import topological_sort as ts
from DataStructures.Graph import vertex as vx
from DataStructures.Graph import edge as edg
from DataStructures.Stack import stack


csv.field_size_limit(2147483647)

data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "Data", "Challenge-4")


def new_logic():
    """
    Crea el catalogo para almacenar las estructuras de datos
    """
    #TODO: Llama a las funciónes de creación de las estructuras de datos

    catalog = {
        "mov_migratorios" : digraph.new_graph(0),
        "recursos_hidricos" : digraph.new_graph(0)
    }
    return catalog

def safe_event_id(event):
    if "THIS:" in event:
        event = event.replace("THIS:", "").strip()
    return event


def haversine(lat1, lon1, lat2, lon2):
    
    dLat = (lat2 - lat1) * math.pi / 180.0
    dLon = (lon2 - lon1) * math.pi / 180.0

    lat1 = (lat1) * math.pi / 180.0
    lat2 = (lat2) * math.pi / 180.0

    a = (pow(math.sin(dLat / 2), 2) + pow(math.sin(dLon / 2), 2) * math.cos(lat1) * math.cos(lat2))
    rad = 6371
    c = 2 * math.asin(math.sqrt(a))
    return rad * c

def cmp_function(element1, element2):
    if element1 == element2:
        return 0

def compare_by_date_id(row1, row2):
    """
    Compara fechas. Si son iguales, desempata por ID.
    Retorna True si row1 es MENOR (más antiguo) que row2.
    """
    # Usamos las llaves que tú creaste en el pre-procesamiento
    t1 = row1['timestamp_actualizado'] 
    t2 = row2['timestamp_actualizado']
    
    if t1 < t2:
        return True
    return False
    

def format_date(date):
    date.strip()
    return datetime.strptime(date, "%Y-%m-%d %H:%M:%S.%f")


def get_node_data_row(graph, n_id):
    # Función auxiliar para extraer datos formateados del vértice
    info = digraph.get_vertex_information(graph, n_id)
    if info:
        lat = lt.get_element(info, 0)
        lon = lt.get_element(info, 1)
        dt = lt.get_element(info, 2)
            
        # Convertir lista ADT de grullas a lista Python para visualización
        cranes_adt = lt.get_element(info, 3)
        cranes_py = []
        for k in range(lt.size(cranes_adt)):
            cranes_py.append(lt.get_element(cranes_adt, k))
            
        # Conteo eventos
        event_count = lt.size(lt.get_element(info, 4))

        # Distancia Hídrica
        water_dist = round(lt.get_element(info, 5), 4)
            
        return [n_id, f"({lat}, {lon})", str(dt), str(cranes_py), event_count, water_dist]
    return []


# Funciones para la carga de datos

def load_data(catalog, filename):
    """
    Carga los datos del reto
    """
    # TODO: Realizar la carga de datos
    start = get_time()

    mov_migratorios = catalog["mov_migratorios"]
    recursos_hidricos = catalog["recursos_hidricos"]

    path = os.path.join(data_dir, filename)
    file = open(path, encoding="utf-8")
    reader = csv.DictReader(file)
    
    lista_filas = lt.new_list()
    for row in reader:
        # Pre-procesamos la fecha una sola vez para eficiencia
        event = safe_event_id(row["event-id"])
        row["event-id-safe"] = event
        row["timestamp_actualizado"] = format_date(row["timestamp"])
        lt.add_last(lista_filas, row)
    
    lista_filas = lt.merge_sort(lista_filas, compare_by_date_id)

    id_nodo_actual = None 
    # Para no llamar a get_vertex a cada rato
    info_nodo_actual = None 
    
    # Capacidad inicial para mapas auxiliares grandes
    init_cap = 2003
     # Capacidad inicial para sub-mapas auxiliares 
    small_cap = 109     
    load_factor = 0.75

    # Control de Arcos 
    mapa_estado_grullas = mp.new_map(init_cap, load_factor)

    # Acumuladores de Arcos 
    arcos_distancia = mp.new_map(init_cap, load_factor) 
    conexiones_agua = mp.new_map(init_cap, load_factor)
    
    # Mapa Auxiliar de Eventos (Para saber a qué nodo pertenece el anterior)
    mapa_eventos = mp.new_map(init_cap, load_factor)

    # Estructuras auxiliares para el reporte
    total_eventos = 0
    # Lista para guardar IDs en orden de creación
    lista_orden_creacion = lt.new_list() 
    
    size_datos = lt.size(lista_filas)
    
    for i in range(size_datos):
        row = lt.get_element(lista_filas, i)
        # Contador de eventos
        total_eventos += 1

        event_id = row["event-id"]
        timestamp = row["timestamp_actualizado"]
        loc_longitude = float(row["location-long"])
        loc_latitude = float(row["location-lat"])
        water_distance = float(row["comments"]) / 1000    
        crane_id = row["tag-local-identifier"]

        crear_nuevo_nodo = False

        # Si es la primera iteracion, creamos un nuevo nodo
        if id_nodo_actual is None:
            crear_nuevo_nodo = True
        # Si tenemos informacion en el nodo actual, verificamos si ya existe el nodo
        else:
            latitud_nodo = lt.get_element(info_nodo_actual, 0)
            longitud_nodo = lt.get_element(info_nodo_actual, 1)
            timestamp_creacion_nodo = lt.get_element(info_nodo_actual, 2)
        
            distancia = haversine(latitud_nodo, longitud_nodo, loc_latitude, loc_longitude)
            # Calculamos la diferencia de tiempo
            diferencia = timestamp_creacion_nodo - timestamp
            
            # Pasamos a segundos absolutos y luego dividimos por 3600 para tener HORAS
            diferencia_segundos = abs(diferencia.total_seconds()) 
    

            if distancia < 3.0 and diferencia_segundos < 10800.00:
                # Preparamos los datos para la lista de eventos en formato (event-id, datos)
                lista_eventos = lt.get_element(info_nodo_actual, 4)

                datos_evento = lt.new_list()
                lt.add_last(datos_evento, loc_latitude)
                lt.add_last(datos_evento, loc_longitude)
                lt.add_last(datos_evento, timestamp)
                lt.add_last(datos_evento, water_distance)

                # Creamos la lista con (event-id, datos)
                pareja_evento = lt.new_list()
                lt.add_last(pareja_evento, event_id)    
                lt.add_last(pareja_evento, datos_evento)

                # Aquí guardamos la pareja de (event-id, datos) en el nodo
                lt.add_last(lista_eventos, pareja_evento)                

                lista_grullas = lt.get_element(info_nodo_actual, 3)
                # Usamos la funcion is_present de array_list que 
                # retorna -1 si un elemento no esta en la lista
                if lt.is_present(lista_grullas, crane_id, cmp_function) == -1:
                    lt.add_last(lista_grullas, crane_id)

                # Ahora calculamos el promedio de la distancia al agua
                prom_actual = lt.get_element(info_nodo_actual, 5)
                n_eventos = lt.size(lista_eventos) 
                
                # Formula promedio incremental 
                # nuevo_prom = ((prom_act * (n-1)) + dato_nuevo) / n
                nuevo_prom = ((prom_actual * (n_eventos - 1)) + water_distance) / n_eventos
                
                # Actualizar el valor en la lista 
                lt.change_info(info_nodo_actual, 5, nuevo_prom)
                
                # Registrar en mapa auxiliar
                mp.put(mapa_eventos, event_id, id_nodo_actual)
            else:
                crear_nuevo_nodo = True
                
        if crear_nuevo_nodo:
            l_grullas = lt.new_list()
            lt.add_last(l_grullas, crane_id)
            l_eventos = lt.new_list()
            # Preparamos los datos para la lista de eventos en formato (event-id, datos)
            datos_evento = lt.new_list()
            lt.add_last(datos_evento, loc_latitude)
            lt.add_last(datos_evento, loc_longitude)
            lt.add_last(datos_evento, timestamp)
            lt.add_last(datos_evento, water_distance)

            # Creamos la lista con (event-id, datos)
            pareja_evento = lt.new_list()
            lt.add_last(pareja_evento, event_id)    
            lt.add_last(pareja_evento, datos_evento)
            lt.add_last(l_eventos, pareja_evento)

            new_info = lt.new_list()
            # id 0 de la lista
            lt.add_last(new_info, loc_latitude)
            # id 1 de la lista      
            lt.add_last(new_info, loc_longitude)     
            # id 2 de la lista
            lt.add_last(new_info, timestamp)
            # id 3 de la lista
            lt.add_last(new_info, l_grullas)
            # id 4 de la lista
            lt.add_last(new_info, l_eventos)
            # id 5 de la lista
            lt.add_last(new_info, water_distance)

            # Insertar en el grafo
            # El ID del nodo es el ID del evento que lo inaugura
            id_nodo_actual = event_id
            digraph.insert_vertex(mov_migratorios, id_nodo_actual, new_info)
            digraph.insert_vertex(recursos_hidricos, id_nodo_actual, new_info)

            # Guardar ID en orden de creación
            lt.add_last(lista_orden_creacion, id_nodo_actual)

            info_nodo_actual = new_info
            mp.put(mapa_eventos, event_id, id_nodo_actual)

        # Ahora implementamos la lógica para los arcos

        # Verificamos dónde estaba esta grulla la última vez
        estado_previo = mp.get(mapa_estado_grullas, crane_id)
        
        if estado_previo is not None:
            # Recuperar info del evento anterior de esta grulla
            prev_event_id = lt.get_element(estado_previo, 0)
            prev_lat = lt.get_element(estado_previo, 1)
            prev_lon = lt.get_element(estado_previo, 2)
            
            # Buscar Nodos
            nodo_origen = mp.get(mapa_eventos, prev_event_id)
            # El evento actual pertenece al nodo actual
            nodo_destino = id_nodo_actual 
            
            if nodo_origen is not None and nodo_destino is not None:
                if nodo_origen != nodo_destino:
                    dist_vuelo = haversine(prev_lat, prev_lon, loc_latitude, loc_longitude)
                    
                    # --- GESTION SEGURA DE ARCOS DISTANCIA ---
                    sub_mapa = mp.get(arcos_distancia, nodo_origen)
                    if sub_mapa is None:
                        sub_mapa = mp.new_map(small_cap, load_factor)
                        mp.put(arcos_distancia, nodo_origen, sub_mapa)
                    
                    # Ahora sub_mapa existe seguro (es una referencia local)
                    lista_vals = mp.get(sub_mapa, nodo_destino)
                    if lista_vals is None:
                        lista_vals = lt.new_list()
                        mp.put(sub_mapa, nodo_destino, lista_vals)
                    lt.add_last(lista_vals, dist_vuelo)

                    sub_mapa_w = mp.get(conexiones_agua, nodo_origen)
                    if sub_mapa_w is None:
                        sub_mapa_w = mp.new_map(small_cap, load_factor)
                        mp.put(conexiones_agua, nodo_origen, sub_mapa_w)
                    
                    # Usamos '1' para marcar existencia
                    mp.put(sub_mapa_w, nodo_destino, 1)

        # Actualizar estado de la grulla para la próxima vuelta
        nuevo_estado = lt.new_list()
        lt.add_last(nuevo_estado, event_id)
        lt.add_last(nuevo_estado, loc_latitude)
        lt.add_last(nuevo_estado, loc_longitude)
        mp.put(mapa_estado_grullas, crane_id, nuevo_estado)

    # Cerramos el archivo
    file.close()

    # Implementacion de los arcos en el grafo 1: Movimientos
    lista_origenes = mp.key_set(arcos_distancia)
    size_origenes = lt.size(lista_origenes)
    
    for i in range(size_origenes):
        origen = lt.get_element(lista_origenes, i)
        sub_mapa = mp.get(arcos_distancia, origen)
        
        lista_destinos = mp.key_set(sub_mapa)
        size_destinos = lt.size(lista_destinos)
        
        for j in range(size_destinos):
            destino = lt.get_element(lista_destinos, j)
            lista_pesos = mp.get(sub_mapa, destino)
            
            # Calcular promedio
            suma = 0.0
            n_vals = lt.size(lista_pesos)
            for k in range(n_vals):
                suma += lt.get_element(lista_pesos, k)
            promedio = suma / n_vals
            
            digraph.add_edge(mov_migratorios, origen, destino, promedio)

    # Implementación de promedios en el grafo 2: Agua
    lista_origenes_w = mp.key_set(conexiones_agua)
    size_origenes_w = lt.size(lista_origenes_w)
    
    for i in range(size_origenes_w):
        origen = lt.get_element(lista_origenes_w, i)
        sub_mapa = mp.get(conexiones_agua, origen)
        
        lista_destinos = mp.key_set(sub_mapa)
        size_destinos = lt.size(lista_destinos)
        
        for j in range(size_destinos):
            destino = lt.get_element(lista_destinos, j)
            
            # Buscamos la info definitiva del vértice en el grafo
            info_destino = digraph.get_vertex_information(recursos_hidricos, destino)
            if info_destino:
                # El elemento en índice 5 es el promedio de distancia al agua
                peso_agua = lt.get_element(info_destino, 5) 
                digraph.add_edge(recursos_hidricos, origen, destino, peso_agua)

    # Generación de reporte

    # Obtener primeros 5 y últimos 5
    first_5_rows = []
    last_5_rows = []
    total_nodes_created = lt.size(lista_orden_creacion)
    
    # Primeros 5
    limit_first = min(5, total_nodes_created)
    for i in range(limit_first):
        n_id = lt.get_element(lista_orden_creacion, i)
        first_5_rows.append(get_node_data_row(mov_migratorios, n_id))

    # Últimos 5
    start_last = max(0, total_nodes_created - 5)
    for i in range(start_last, total_nodes_created):
        n_id = lt.get_element(lista_orden_creacion, i)
        last_5_rows.append(get_node_data_row(mov_migratorios, n_id))
    
    reporte = {
        "general": {
            "total_grullas": mp.size(mapa_estado_grullas),
            "total_eventos": total_eventos,
            "rows_first": first_5_rows,
            "rows_last": last_5_rows
        },
        "distancia": {
            "nodos": mp.size(digraph.vertices(mov_migratorios)),
            "arcos": digraph.size(mov_migratorios)
        },
        "agua": {
            "nodos": mp.size(digraph.vertices(recursos_hidricos)),
            "arcos": digraph.size(recursos_hidricos)
        }
    }
    return catalog, reporte

# Funciones de consulta sobre el catálogo

def req_1(catalog):
    """
    Retorna el resultado del requerimiento 1
    """
    # TODO: Modificar el requerimiento 1
    pass


def req_2(catalog):
    """
    Retorna el resultado del requerimiento 2
    """
    # TODO: Modificar el requerimiento 2
    pass


def req_3(catalog, punto_origen):
    """
    Retorna el resultado del requerimiento 3
    Identifica posibles rutas migratorias desde un punto de origen dado
    
    :param catalog: Catálogo con los grafos
    :param punto_origen: ID del punto migratorio de origen
    :returns: Diccionario con información de las rutas
    """
    start = get_time()
    
    # Trabajamos con el grafo de movimientos migratorios
    mov_graph = catalog["mov_migratorios"]
    
    # Verificar si el punto de origen existe
    if not digraph.contains_vertex(mov_graph, punto_origen):
        return {
            "error": True,
            "message": f"El punto migratorio '{punto_origen}' no existe en el grafo",
            "time": delta_time(start, get_time())
        }
    
    # Verificar si el grafo tiene ciclos
    has_cycles, cycle_example = ts.has_cycle(mov_graph)
    
    result = {
        "error": False,
        "punto_origen": punto_origen,
        "total_puntos": digraph.order(mov_graph),
        "has_cycles": has_cycles,
        "cycle_example": None,
        "topo_order": None,
        "routes": []
    }
    
    if has_cycles:
        # Si hay ciclos, mostrar ejemplo
        result["cycle_example"] = cycle_example
        result["message"] = "No es posible realizar orden topológico debido a ciclos en el grafo"
    else:
        # Si no hay ciclos, realizar ordenamiento topológico
        topo_order = ts.topological_sort(mov_graph)
        result["topo_order"] = topo_order
        
        # === IDENTIFICAR RUTAS MIGRATORIAS DESDE EL PUNTO DE ORIGEN ===
        
        # Usar BFS desde el punto de origen para encontrar todos los nodos alcanzables
        visited_map = bfs.bfs(mov_graph, punto_origen)
        
        # Calcular grado de salida (para identificar sumideros)
        sinks = lt.new_list()
        vertices_keys = digraph.vertices(mov_graph)
        
        for i in range(lt.size(vertices_keys)):
            key = lt.get_element(vertices_keys, i)
            # Es sumidero si tiene grado de salida 0 y es alcanzable desde origen
            if digraph.degree(mov_graph, key) == 0 and bfs.has_path_to_bfs(key, visited_map):
                lt.add_last(sinks, key)
        
        # Si no hay sumideros alcanzables, buscar los nodos más lejanos
        if lt.size(sinks) == 0:
            # Encontrar todos los nodos alcanzables
            for i in range(lt.size(vertices_keys)):
                key = lt.get_element(vertices_keys, i)
                if bfs.has_path_to_bfs(key, visited_map) and key != punto_origen:
                    lt.add_last(sinks, key)
        
        # Encontrar rutas desde el origen a cada sumidero/destino
        routes = []
        
        for j in range(lt.size(sinks)):
            sink = lt.get_element(sinks, j)
            
            if bfs.has_path_to_bfs(sink, visited_map):
                path_stack = bfs.path_to_bfs(sink, visited_map)
                
                # Convertir stack a lista
                path = []
                while not stack.is_empty(path_stack):
                    path.append(stack.pop(path_stack))
                
                # === OBTENER INFORMACIÓN DE LA RUTA ===
                route_info = {
                    "total_points": len(path),
                    "origin": path[0] if len(path) > 0 else None,
                    "destination": path[-1] if len(path) > 0 else None,
                    "path_details": [],
                    "cranes": set(),
                    "total_distance": 0.0
                }
                
                # Recopilar información de cada punto
                for idx, node_id in enumerate(path):
                    info = digraph.get_vertex_information(mov_graph, node_id)
                    
                    if info:
                        lat = lt.get_element(info, 0)
                        lon = lt.get_element(info, 1)
                        timestamp = lt.get_element(info, 2)
                        cranes_list = lt.get_element(info, 3)
                        events_count = lt.size(lt.get_element(info, 4))
                        water_dist = lt.get_element(info, 5)
                        
                        # Recolectar grullas únicas
                        for k in range(lt.size(cranes_list)):
                            crane_id = lt.get_element(cranes_list, k)
                            route_info["cranes"].add(crane_id)
                        
                        node_detail = {
                            "id": node_id,
                            "position": (lat, lon),
                            "timestamp": timestamp,
                            "cranes_count": lt.size(cranes_list),
                            "cranes_list": [lt.get_element(cranes_list, k) for k in range(lt.size(cranes_list))],
                            "events_count": events_count,
                            "water_distance": water_dist
                        }
                        
                        # Calcular distancia al siguiente nodo si existe
                        if idx < len(path) - 1:
                            next_node = path[idx + 1]
                            vertex_obj = digraph.get_vertex(mov_graph, node_id)
                            if vertex_obj:
                                adjacents_map = vx.get_adjacents(vertex_obj)
                                edge_to_next = mp.get(adjacents_map, next_node)
                                if edge_to_next:
                                    distance = edg.weight(edge_to_next)
                                    node_detail["distance_to_next"] = distance
                                    route_info["total_distance"] += distance
                        
                        route_info["path_details"].append(node_detail)
                
                route_info["total_cranes"] = len(route_info["cranes"])
                route_info["cranes"] = list(route_info["cranes"])
                
                routes.append(route_info)
        
        # Ordenar rutas por longitud (de mayor a menor)
        routes.sort(key=lambda x: x["total_points"], reverse=True)
        
        result["routes"] = routes
        result["total_rutas"] = len(routes)
    
    end = get_time()
    result["time"] = delta_time(start, end)
    
    return result


def req_4(catalog):
    """
    Retorna el resultado del requerimiento 4
    """
    # TODO: Modificar el requerimiento 4
    pass


def req_5(catalog):
    """
    Retorna el resultado del requerimiento 5
    """
    # TODO: Modificar el requerimiento 5
    pass

def req_6(catalog, punto_origen):
    """
    REQ. 6: Identifica posibles subredes hídricas (subgrafos o subconjuntos) 
    dentro del nicho biológico para identificar grupos de individuos (grullas) aislados.
    
    Parámetros de entrada:
    - Nicho biológico de los individuos representado por el grafo con todos los 
      puntos migratorios con respecto a las fuentes hídricas.
    - punto_origen: Identificador del punto migratorio desde donde se inicia el análisis
    
    :param catalog: Catálogo con los grafos (contiene el nicho biológico)
    :param punto_origen: ID del punto migratorio de origen para iniciar el análisis
    :returns: Diccionario con información de las subredes hídricas identificadas
    """
    start = get_time()
    
    # El nicho biológico es el grafo de recursos hídricos (fuentes hídricas)
    water_graph = catalog["recursos_hidricos"]
    
    # Verificar si el punto de origen existe
    if not digraph.contains_vertex(water_graph, punto_origen):
        return {
            "error": True,
            "message": f"El punto migratorio '{punto_origen}' no existe en el grafo",
            "time": delta_time(start, get_time())
        }
    
    # Verificar que el grafo tenga nodos
    if digraph.order(water_graph) == 0:
        return {
            "error": True,
            "message": "El grafo de recursos hídricos está vacío",
            "time": delta_time(start, get_time())
        }
    
    result = {
        "error": False,
        "total_puntos": digraph.order(water_graph),
        "total_arcos": digraph.size(water_graph),
        "subredes": [],
        "total_subredes": 0
    }
    
    # === IDENTIFICAR COMPONENTES CONECTADOS (SUBREDES) ===
    
    # Mapa para rastrear qué nodos ya fueron visitados
    visited_global = mp.new_map(digraph.order(water_graph), 0.5)
    vertices_keys = digraph.vertices(water_graph)
    
    # Inicializar todos los nodos como no visitados
    for i in range(lt.size(vertices_keys)):
        key = lt.get_element(vertices_keys, i)
        mp.put(visited_global, key, False)
    
    # Lista para almacenar las subredes
    subredes = []
    
    # Recorrer todos los nodos del grafo
    for i in range(lt.size(vertices_keys)):
        origen = lt.get_element(vertices_keys, i)
        
        # Si el nodo no ha sido visitado, explorar su componente
        if not mp.get(visited_global, origen):
            # Usar BFS para encontrar todos los nodos alcanzables desde 'origen'
            visited_map = bfs.bfs(water_graph, origen)
            
            # Obtener todos los nodos de este componente
            componente_nodos = lt.new_list()
            
            # Verificar cada nodo del grafo para ver si pertenece a este componente
            for j in range(lt.size(vertices_keys)):
                node_key = lt.get_element(vertices_keys, j)
                
                # Si el nodo es alcanzable desde origen, pertenece al componente
                if bfs.has_path_to_bfs(node_key, visited_map):
                    lt.add_last(componente_nodos, node_key)
                    mp.put(visited_global, node_key, True)
            
            # Si encontramos al menos un nodo en el componente, guardarlo
            if lt.size(componente_nodos) > 0:
                subredes.append(componente_nodos)
    
    # === PROCESAR INFORMACIÓN DE CADA SUBRED ===
    
    for idx, subred_nodos in enumerate(subredes, 1):
        subred_info = {
            "id": idx,
            "total_puntos": lt.size(subred_nodos),
            "nodos": [],
            "grullas": set(),
            "lat_max": float('-inf'),
            "lat_min": float('inf'),
            "lon_max": float('-inf'),
            "lon_min": float('inf'),
            "primeros_3": [],
            "ultimos_3": []
        }
        
        # Recopilar información de cada nodo de la subred
        for i in range(lt.size(subred_nodos)):
            node_id = lt.get_element(subred_nodos, i)
            info = digraph.get_vertex_information(water_graph, node_id)
            
            if info:
                lat = lt.get_element(info, 0)
                lon = lt.get_element(info, 1)
                timestamp = lt.get_element(info, 2)
                cranes_list = lt.get_element(info, 3)
                events_count = lt.size(lt.get_element(info, 4))
                water_dist = lt.get_element(info, 5)
                
                # Actualizar límites geográficos
                subred_info["lat_max"] = max(subred_info["lat_max"], lat)
                subred_info["lat_min"] = min(subred_info["lat_min"], lat)
                subred_info["lon_max"] = max(subred_info["lon_max"], lon)
                subred_info["lon_min"] = min(subred_info["lon_min"], lon)
                
                # Recolectar grullas únicas
                for k in range(lt.size(cranes_list)):
                    crane_id = lt.get_element(cranes_list, k)
                    subred_info["grullas"].add(crane_id)
                
                # Guardar información del nodo
                node_data = {
                    "id": node_id,
                    "lat": lat,
                    "lon": lon,
                    "timestamp": timestamp,
                    "cranes_count": lt.size(cranes_list),
                    "cranes_list": [lt.get_element(cranes_list, k) for k in range(lt.size(cranes_list))],
                    "events_count": events_count,
                    "water_distance": water_dist
                }
                
                subred_info["nodos"].append(node_data)
        
        # Ordenar nodos por timestamp para obtener primeros y últimos
        subred_info["nodos"].sort(key=lambda x: x["timestamp"])
        
        # Obtener primeros 3 y últimos 3
        total_nodos = len(subred_info["nodos"])
        subred_info["primeros_3"] = subred_info["nodos"][:min(3, total_nodos)]
        subred_info["ultimos_3"] = subred_info["nodos"][-min(3, total_nodos):]
        
        # Calcular longitud y latitud de la subred
        subred_info["longitud_lat"] = subred_info["lat_max"] - subred_info["lat_min"]
        subred_info["longitud_lon"] = subred_info["lon_max"] - subred_info["lon_min"]
        
        # Convertir set de grullas a lista y obtener primeros/últimos
        grullas_list = sorted(list(subred_info["grullas"]))
        subred_info["total_grullas"] = len(grullas_list)
        subred_info["grullas_primeros_3"] = grullas_list[:min(3, len(grullas_list))]
        subred_info["grullas_ultimos_3"] = grullas_list[-min(3, len(grullas_list)):]
        
        result["subredes"].append(subred_info)
    
    # Ordenar subredes por cantidad de puntos (de mayor a menor)
    result["subredes"].sort(key=lambda x: x["total_puntos"], reverse=True)
    result["total_subredes"] = len(result["subredes"])
    
    end = get_time()
    result["time"] = delta_time(start, end)
    
    return result


# Funciones para medir tiempos de ejecucion

def get_time():
    """
    devuelve el instante tiempo de procesamiento en milisegundos
    """
    return float(pytime.perf_counter()*1000)


def delta_time(start, end):
    """
    devuelve la diferencia entre tiempos de procesamiento muestreados
    """
    elapsed = float(end - start)
    return elapsed
