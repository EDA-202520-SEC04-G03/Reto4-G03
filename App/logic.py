import time as pytime
import csv
import os
import math
from datetime import datetime, date, time as dtime, timedelta
from DataStructures.List import array_list as lt
from DataStructures.Map import map_linear_probing as mp
from DataStructures.Graph import bfs as bfs_algos
from DataStructures.Graph import digraph
from DataStructures.Graph import dfs
from DataStructures.Graph import topological_sort as ts
from DataStructures.Graph import vertex as vx
from DataStructures.Graph import edge as edg
from DataStructures.Stack import stack 
from DataStructures.Graph import dijkstra as dij
from DataStructures.Priority_queue import priority_queue as pq


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

def get_closest_node(graph, target_lat, target_lon):
    """Encuentra el ID del nodo más cercano a una coordenada dada"""
    closest_id = None
    min_dist = float('inf')

    keys = digraph.vertices(graph)

    size_keys = lt.size(keys)
    for i in range(size_keys):
        v_id = lt.get_element(keys, i)
        
        # >>> CORRECCIÓN: Obtenemos la info del vértice (que es una LISTA, no un mapa)
        v_data = digraph.get_vertex_information(graph, v_id)
        
        if v_data is not None:
            # >>> CORRECCIÓN: Accedemos por Índices numéricos
            # Índice 0: Latitud, Índice 1: Longitud
            v_lat = lt.get_element(v_data, 0)
            v_lon = lt.get_element(v_data, 1)
            
            dist = haversine(target_lat, target_lon, v_lat, v_lon)
            
            if dist < min_dist:
                min_dist = dist
                closest_id = v_id
            
    return closest_id, min_dist
# Funciones para la carga de datos


def prim_mst_from_source(graph, source):
    """
    Ejecuta Prim desde un vértice fuente sobre un grafo dirigido (lo tratamos
    como no dirigido para efectos del MST, usando los pesos de las aristas salientes).
    Retorna:
      - parent: mapa hijo -> padre
      - key: mapa vertice -> peso del arco con el que entra al MST
      - visit_order: lista (Python) con el orden en el que se van añadiendo vértices
    """
    vertices = digraph.vertices(graph)
    n = lt.size(vertices)

    if n == 0:
        return None, None, []

    # Mapas auxiliares
    visited = mp.new_map(n, 0.5)
    key = mp.new_map(n, 0.5)
    parent = mp.new_map(n, 0.5)

    # Inicialización
    i = 0
    while i < n:
        v = lt.get_element(vertices, i)
        mp.put(visited, v, False)
        mp.put(key, v, float("inf"))
        mp.put(parent, v, None)
        i += 1

    # Cola de prioridad (min-heap)
    heap = pq.new_heap()
    mp.put(key, source, 0.0)
    pq.insert(heap, 0.0, source)

    visit_order = []

    # Bucle principal de Prim
    while not pq.is_empty(heap):
        entry = pq.del_min(heap)
        u = entry["key"]   

        # Si ya fue visitado, lo ignoramos
        if mp.get(visited, u):
            continue

        mp.put(visited, u, True)
        visit_order.append(u)

        # Obtener adyacentes de u
        vertex_obj = digraph.get_vertex(graph, u)
        if vertex_obj is None:
            continue

        adj_map = vx.get_adjacents(vertex_obj)
        adj_keys = mp.key_set(adj_map)
        size_adj = lt.size(adj_keys)

        j = 0
        while j < size_adj:
            v = lt.get_element(adj_keys, j)
            edge_uv = mp.get(adj_map, v)

            if edge_uv is not None:
                w = edg.to(edge_uv)
                weight_uv = edg.weight(edge_uv)

                if not mp.get(visited, w):
                    current_key = mp.get(key, w)
                    if current_key is None or weight_uv < current_key:
                        mp.put(key, w, weight_uv)
                        mp.put(parent, w, u)
                        pq.insert(heap, weight_uv, w)

            j += 1

    return parent, key, visit_order


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
    
    end = get_time()
    tiempo_total = delta_time(start, end)

    reporte = {
        "general": {
            "total_grullas": mp.size(mapa_estado_grullas),
            "total_eventos": total_eventos,
            "rows_first": first_5_rows,
            "rows_last": last_5_rows,
            "tiempo_carga": tiempo_total 
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
    
    return lista_filas, reporte
# Funciones de consulta sobre el catálogo

def req_1(catalog, lat_o, lon_o, lat_d, lon_d, crane_id):
    """
    Camino DFS para un individuo entre dos puntos.
    Usa el grafo de movimientos migratorios y la estructura de vértices
    creada en load_data (lista ADT con índices fijos).
    """

    graph = catalog["mov_migratorios"]

    # 1. Encontrar nodos más cercanos al origen y destino
    node_o, _ = get_closest_node(graph, lat_o, lon_o)
    node_d, _ = get_closest_node(graph, lat_d, lon_d)

    if node_o is None or node_d is None:
        return {
            "error": True,
            "message": "No se encontraron nodos cercanos a las coordenadas dadas."
        }

    # 2. Ejecutar DFS desde el nodo origen
    visited = dfs.dfs(graph, node_o)

    # 3. Verificar si existe un camino hacia el nodo destino
    if not dfs.has_path_to(node_d, visited):
        return {
            "error": True,
            "message": "No existe camino DFS entre los puntos dados.",
            "origin_node": node_o,
            "dest_node": node_d
        }

    # 4. Reconstruir el camino DFS completo (lista Python de ids de nodos)
    path = dfs.path_to(node_d, visited)

    # 5. Recorrer el camino: calcular distancia total y primer nodo con la grulla
    total_distance = 0.0
    first_node_with_crane = None

    path_len = len(path)
    nodes_info = []

    for i in range(path_len):
        node_id = path[i]
        info = digraph.get_vertex_information(graph, node_id)

        # info es una lista ADT (lt) con la estructura:
        # 0: lat, 1: lon, 2: timestamp, 3: lista grullas, 4: eventos, 5: dist_agua_prom
        lat = lt.get_element(info, 0)
        lon = lt.get_element(info, 1)
        cranes_adt = lt.get_element(info, 3)

        # Pasar grullas a lista Python
        cranes_py = []
        size_cranes = lt.size(cranes_adt)
        j = 0
        while j < size_cranes:
            cranes_py.append(lt.get_element(cranes_adt, j))
            j += 1

        # Verificar si la grulla aparece en este nodo (solo marcamos el primero)
        if first_node_with_crane is None:
            # Usamos is_present con cmp_function, como en load_data
            pos = lt.is_present(cranes_adt, crane_id, cmp_function)
            if pos != -1:
                first_node_with_crane = node_id

        # Distancia al siguiente nodo (si existe)
        next_dist = None
        if i < path_len - 1:
            next_edge = digraph.get_edge(graph, node_id, path[i + 1])
            if next_edge is not None:
                next_dist = next_edge["weight"]
                total_distance += next_dist

        # Construir registro para la tabla
        nodo_dict = {
            "id": node_id,
            "lat": lat,
            "lon": lon,
            "num_cranes": len(cranes_py),
            "cranes_first": cranes_py[:3],
            "cranes_last": cranes_py[-3:],
            "dist_to_next": next_dist
        }
        nodes_info.append(nodo_dict)

    # 6. Primeros 5 y últimos 5 nodos del camino
    primeros = nodes_info[:5]
    ultimos = nodes_info[-5:]

    # 7. Retorno final (alineado con el view que armamos)
    return {
        "error": False,
        "origin_node": node_o,
        "dest_node": node_d,
        "first_node_with_crane": first_node_with_crane,
        "path_length": len(path),
        "total_distance": total_distance,
        "first_nodes": primeros,
        "last_nodes": ultimos
    }


def req_2(control, lat_origen, lon_origen, lat_destino, lon_destino, radio_km):
    """
    Retorna el resultado del requerimiento 2
    """
    start = get_time()
    
    graph = control["mov_migratorios"]
    
    # Encontrar nodos más cercanos
    start_node, _ = get_closest_node(graph, lat_origen, lon_origen)
    end_node, _ = get_closest_node(graph, lat_destino, lon_destino)
    
    if not start_node or not end_node:
        return {"error": True, "message": "No se encontraron nodos cercanos."}

    # Ejecutar BFS
    visited_map = bfs_algos.bfs(graph, start_node)
    
    # Reconstruir camino
    path_stack = bfs_algos.path_to_bfs(end_node, visited_map)
    
    if path_stack is None:
        return {"error": True, "message": "No existe camino entre los puntos seleccionados."}

    # Procesar el camino para verificar el radio
    path_details = []
    last_node_in_radius = start_node
    total_dist = 0.0
    prev_node_data = None
    
    # Desempilar
    while not stack.is_empty(path_stack):
        node_id = stack.pop(path_stack)
        node_data = digraph.get_vertex_information(graph, node_id)
        
        current_lat = lt.get_element(node_data, 0)
        current_lon = lt.get_element(node_data, 1)
        
        # Calcular distancia acumulada del viaje
        dist_segment = 0
        if prev_node_data:
            prev_lat = lt.get_element(prev_node_data, 0)
            prev_lon = lt.get_element(prev_node_data, 1)
            
            dist_segment = haversine(prev_lat, prev_lon, current_lat, current_lon)
            total_dist += dist_segment
        
        # Verificar radio con respecto al origen original
        dist_to_origin = haversine(lat_origen, lon_origen, current_lat, current_lon)
        
        if dist_to_origin <= radio_km:
            last_node_in_radius = node_id
            
        # Extraer info extra para tabla
        grullas_adt = lt.get_element(node_data, 3)
        eventos_adt = lt.get_element(node_data, 4)
        
        py_list = []
        if grullas_adt:
            size = lt.size(grullas_adt)
            for i in range(size):
                py_list.append(lt.get_element(grullas_adt, i))
        
        path_details.append({
            "id": node_id,
            "lat": current_lat,
            "lon": current_lon,
            "grullas": py_list,
            "eventos": lt.size(eventos_adt),
            "dist_next": 0 
        })
        
        if len(path_details) > 1:
            path_details[-2]["dist_next"] = dist_segment
            
        prev_node_data = node_data
    
    end = get_time()
    tiempo_total = delta_time(start, end)

    return {
        "error": False,
        "total_puntos": len(path_details),
        "total_distancia": total_dist,
        "last_node_in_radius": last_node_in_radius,
        "path_details": path_details,
        "origen_id": start_node,
        "destino_id": end_node,
        "time": tiempo_total 
    }


def req_3(catalog):
    """
    REQ. 3: Identifica posibles rutas migratorias dentro del nicho biológico
    
    NO requiere parámetros de entrada - analiza automáticamente todo el grafo
    
    :param catalog: Catálogo con los grafos
    :returns: Diccionario con información de las rutas
    """
    start = get_time()
    
    # Trabajamos con el grafo de movimientos migratorios
    mov_graph = catalog["mov_migratorios"]
    
    # Verificar que el grafo tenga nodos
    if digraph.order(mov_graph) == 0:
        return {
            "error": True,
            "message": "El grafo de movimientos migratorios esta vacio",
            "time": delta_time(start, get_time())
        }
    
    result = {
        "error": False,
        "total_puntos": digraph.order(mov_graph),
        "has_cycles": False,
        "cycle_example": None,
        "topo_order": None,
        "routes": []
    }
    
    # Verificar si el grafo tiene ciclos
    has_cycles, cycle_example = ts.has_cycle(mov_graph)
    result["has_cycles"] = has_cycles
    result["cycle_example"] = cycle_example
    
    if has_cycles:
        # Si hay ciclos, solo mostrar el ciclo de ejemplo
        result["message"] = "No es posible realizar orden topologico debido a ciclos en el grafo"
    else:
        # Si no hay ciclos, realizar ordenamiento topológico
        topo_order = ts.topological_sort(mov_graph)
        
        # Convertir lista ADT a lista Python para facilitar el manejo
        topo_list_py = []
        for i in range(lt.size(topo_order)):
            topo_list_py.append(lt.get_element(topo_order, i))
        
        result["topo_order"] = topo_list_py
        
        # === IDENTIFICAR TODAS LAS RUTAS MIGRATORIAS ===
        
        # Identificar todos los nodos fuente (sin arcos entrantes)
        vertices_keys = digraph.vertices(mov_graph)
        sources = lt.new_list()
        
        for i in range(lt.size(vertices_keys)):
            node = lt.get_element(vertices_keys, i)
            # Un nodo es fuente si ningún otro nodo apunta hacia él
            is_source = True
            
            # Verificar si algún nodo tiene un arco hacia este nodo
            for j in range(lt.size(vertices_keys)):
                other_node = lt.get_element(vertices_keys, j)
                if other_node != node:
                    edge = digraph.get_edge(mov_graph, other_node, node)
                    if edge is not None:
                        is_source = False
                        break
            
            if is_source:
                lt.add_last(sources, node)
        
        # Identificar todos los sumideros (sin arcos salientes)
        sinks = lt.new_list()
        for i in range(lt.size(vertices_keys)):
            node = lt.get_element(vertices_keys, i)
            if digraph.degree(mov_graph, node) == 0:
                lt.add_last(sinks, node)
        
        # Si no hay sumideros, usar todos los nodos como posibles destinos
        if lt.size(sinks) == 0:
            for i in range(lt.size(vertices_keys)):
                lt.add_last(sinks, lt.get_element(vertices_keys, i))
        
        # Para cada fuente, encontrar rutas hacia todos los sumideros
        routes = []
        
        for i in range(lt.size(sources)):
            source = lt.get_element(sources, i)
            
            # Usar BFS desde esta fuente
            visited_map = bfs_algos.bfs(mov_graph, source)
            
            # Encontrar rutas hacia cada sumidero alcanzable
            for j in range(lt.size(sinks)):
                sink = lt.get_element(sinks, j)
                
                if sink != source and bfs_algos.has_path_to_bfs(sink, visited_map):
                    path_stack = bfs_algos.path_to_bfs(sink, visited_map)
                    
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
        
        # Convertir lista Python a lista ADT para ordenar
        routes_adt = lt.new_list()
        for route in routes:
            lt.add_last(routes_adt, route)
        
        # Función de comparación por longitud (descendente)
        def compare_routes_desc(route1, route2):
            if route1["total_points"] > route2["total_points"]:
                return True
            return False
        
        # Ordenar usando merge_sort
        routes_ordenadas = lt.merge_sort(routes_adt, compare_routes_desc)
        
        # Convertir de vuelta a lista Python
        routes = []
        for i in range(lt.size(routes_ordenadas)):
            routes.append(lt.get_element(routes_ordenadas, i))
        
        result["routes"] = routes
        result["total_rutas"] = len(routes)
    
    end = get_time()
    result["time"] = delta_time(start, end)
    
    return result


def req_4(catalog, lat_origen, lon_origen):
    """
    REQ. 4: Construye un corredor hídrico óptimo (MST con Prim)
    a partir del punto hídrico más cercano a unas coordenadas dadas.

    """
    start = get_time()

    graph = catalog["recursos_hidricos"]

    # Verificar que el grafo no esté vacío
    if digraph.order(graph) == 0:
        return {
            "error": True,
            "message": "El grafo de recursos hídricos está vacío.",
            "time": delta_time(start, get_time())
        }

    # Encontrar nodo hídrico más cercano al origen
    origin_node, _ = get_closest_node(graph, lat_origen, lon_origen)

    if origin_node is None:
        return {
            "error": True,
            "message": "No se encontró un punto hídrico cercano a las coordenadas dadas.",
            "time": delta_time(start, get_time())
        }

    # Ejecutar Prim desde el nodo origen
    parent, key, visit_order = prim_mst_from_source(graph, origin_node)

    if parent is None:
        return {
            "error": True,
            "message": "No fue posible construir el corredor hídrico.",
            "time": delta_time(start, get_time())
        }

    # Procesar resultados del MST
    total_distance = 0.0
    all_cranes = set()
    nodes_info = []

    size_visit = len(visit_order)
    i = 0
    while i < size_visit:
        node_id = visit_order[i]
        info = digraph.get_vertex_information(graph, node_id)

        if info is not None:
            lat = lt.get_element(info, 0)
            lon = lt.get_element(info, 1)
            cranes_adt = lt.get_element(info, 3)

            # Convertir lista ADT de grullas a lista Python
            cranes_py = []
            size_cranes = lt.size(cranes_adt)
            j = 0
            while j < size_cranes:
                crane = lt.get_element(cranes_adt, j)
                cranes_py.append(crane)
                all_cranes.add(crane)
                j += 1

            # Peso del arco con el que este nodo entra al MST
            edge_weight = key and mp.get(key, node_id)
            if edge_weight is None:
                edge_weight = 0.0

            node_dict = {
                "id": node_id,
                "lat": lat,
                "lon": lon,
                "num_cranes": len(cranes_py),
                "cranes_first": cranes_py[:3],
                "cranes_last": cranes_py[-3:],
                "edge_weight": edge_weight
            }
            nodes_info.append(node_dict)

        i += 1

    # Distancia total del corredor (suma de key[v] excepto origen)
    k = 0
    while k < size_visit:
        v_id = visit_order[k]
        if v_id != origin_node:
            edge_w = mp.get(key, v_id)
            if edge_w is not None and edge_w != float("inf"):
                total_distance += edge_w
        k += 1

    total_points = len(nodes_info)
    total_individuals = len(all_cranes)

    # Primeros y últimos 5 nodos del corredor
    first_nodes = nodes_info[:5]
    last_nodes = nodes_info[-5:]

    end = get_time()
    tiempo = delta_time(start, end)

    return {
        "error": False,
        "origin_node": origin_node,
        "total_points": total_points,
        "total_individuals": total_individuals,
        "total_distance": total_distance,
        "first_nodes": first_nodes,
        "last_nodes": last_nodes,
        "time": tiempo
    }


def req_5(control, lat_origen, lon_origen, lat_destino, lon_destino, criterio):
    """
    Retorna el resultado del requerimiento 5
    """
    start = get_time()
    # 1. Seleccionar Grafo
    graph = None
    if criterio == "distancia":
        graph = control["mov_migratorios"]
    elif criterio == "agua":
        graph = control["recursos_hidricos"]
    else:
        return {"error": True, "message": "Criterio inválido."}
        
    # 2. Encontrar nodos
    start_node, _ = get_closest_node(graph, lat_origen, lon_origen)
    end_node, _ = get_closest_node(graph, lat_destino, lon_destino)
    
    if not start_node or not end_node:
        return {"error": True, "message": "Puntos fuera del rango."}

    # 3. Ejecutar Dijkstra
    dijkstra_res = dij.dijkstra(graph, start_node)
        
    costo_total = dij.dist_to(end_node, dijkstra_res)
        
    if costo_total == float('inf'):
        return {"error": True, "message": "No existe camino viable."}
             
    path_stack = dij.path_to(end_node, dijkstra_res)
        
    # 4. Procesar resultados
    path_details = []
    total_segments = 0
    prev_node_data = None
    
    while not stack.is_empty(path_stack):
        node_id = stack.pop(path_stack)
        node_data = digraph.get_vertex_information(graph, node_id)
        
        # CORRECCIÓN: Acceso por índices
        lat = lt.get_element(node_data, 0)
        lon = lt.get_element(node_data, 1)
        grullas_adt = lt.get_element(node_data, 3)
        
        dist_segment = 0
        if prev_node_data:
            total_segments += 1
            prev_lat = lt.get_element(prev_node_data, 0)
            prev_lon = lt.get_element(prev_node_data, 1)
            
            dist_segment = haversine(prev_lat, prev_lon, lat, lon)
            
            if len(path_details) > 0:
                path_details[-1]["dist_next"] = dist_segment
        
        py_list = []
    
        if grullas_adt:
            size = lt.size(grullas_adt)
            for i in range(size):
                py_list.append(lt.get_element(grullas_adt, i))

        path_details.append({
            "id": node_id,
            "lat": lat,
            "lon": lon,
            "grullas": py_list,
            "dist_next": 0 
        })
        prev_node_data = node_data

    end = get_time()
    tiempo_total = delta_time(start, end)

    return {
        "error": False,
        "costo_total": costo_total,
        "total_puntos": len(path_details),
        "total_segmentos": total_segments,
        "path_details": path_details,
        "origen_id": start_node,
        "destino_id": end_node,
        "time": tiempo_total
    }

def req_6(catalog):
    """
    REQ. 6: Identifica posibles subredes hídricas (subgrafos o subconjuntos) 
    dentro del nicho biológico para identificar grupos de individuos (grullas) aislados.
    
    NO requiere parámetro de entrada - busca automáticamente todas las subredes
    
    :param catalog: Catálogo con los grafos (contiene el nicho biológico)
    :returns: Diccionario con información de las subredes hídricas identificadas
    """
    start = get_time()
    
    # El nicho biológico es el grafo de recursos hídricos (fuentes hídricas)
    water_graph = catalog["recursos_hidricos"]
    
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
    
    # Recorrer todos los nodos del grafo para encontrar componentes conectados
    for i in range(lt.size(vertices_keys)):
        origen = lt.get_element(vertices_keys, i)
        
        # Si el nodo no ha sido visitado, explorar su componente
        if not mp.get(visited_global, origen):
            # Usar BFS para encontrar todos los nodos alcanzables desde 'origen'
            visited_map = bfs_algos.bfs(water_graph, origen)
            
            # Obtener todos los nodos de este componente
            componente_nodos = lt.new_list()
            
            # Verificar cada nodo del grafo para ver si pertenece a este componente
            for j in range(lt.size(vertices_keys)):
                node_key = lt.get_element(vertices_keys, j)
                
                # Si el nodo es alcanzable desde origen, pertenece al componente
                if bfs_algos.has_path_to_bfs(node_key, visited_map):
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
        
        # Convertir a lista ADT para usar merge_sort
        nodos_adt = lt.new_list()
        for nodo in subred_info["nodos"]:
            lt.add_last(nodos_adt, nodo)
        
        # Función de comparación por timestamp
        def compare_by_timestamp(nodo1, nodo2):
            if nodo1["timestamp"] < nodo2["timestamp"]:
                return True
            return False
        
        # Ordenar usando merge_sort
        nodos_ordenados = lt.merge_sort(nodos_adt, compare_by_timestamp)
        
        # Convertir de vuelta a lista Python
        subred_info["nodos"] = []
        for i in range(lt.size(nodos_ordenados)):
            subred_info["nodos"].append(lt.get_element(nodos_ordenados, i))
        
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
    
    # Ordenar subredes por cantidad de puntos (de mayor a menor) - LA MÁS GRANDE PRIMERO
    result["subredes"].sort(key=lambda x: x["total_puntos"], reverse=True)
    result["total_subredes"] = len(result["subredes"])
    
    # Identificar la subred más grande
    if len(result["subredes"]) > 0:
        result["subred_mas_grande"] = result["subredes"][0]["id"]
        result["puntos_subred_mas_grande"] = result["subredes"][0]["total_puntos"]
    
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
