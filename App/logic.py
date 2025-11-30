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
    arcos_agua = mp.new_map(init_cap, load_factor)  
    
    # Mapa Auxiliar de Eventos (Para saber a qué nodo pertenece el anterior)
    mapa_eventos = mp.new_map(init_cap, load_factor)

    # Estructuras auxiliares para el reporte
    total_eventos = 0
    # Lista para guardar IDs en orden de creación
    lista_orden_creacion = lt.new_list() 
    
    for row in reader:
        # Contador de eventos
        total_eventos += 1

        event_id = row["event-id"]
        timestamp = format_date(row["timestamp"])
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
            timestamp_actual = lt.get_element(info_nodo_actual, 2)
        
            distancia = haversine(latitud_nodo, longitud_nodo, loc_latitude, loc_longitude)
            # Calculamos la diferencia de tiempo
            diferencia = timestamp_actual - timestamp
            
            # Pasamos a segundos absolutos y luego dividimos por 3600 para tener HORAS
            diferencia_segundos = abs(diferencia.total_seconds()) 
    

            if distancia <= 3.0 and diferencia_segundos <= 10800.00:
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

                    # --- GESTION SEGURA DE ARCOS AGUA ---
                    agua_destino = lt.get_element(info_nodo_actual, 5)
                    
                    sub_mapa_w = mp.get(arcos_agua, nodo_origen)
                    if sub_mapa_w is None:
                        sub_mapa_w = mp.new_map(small_cap, load_factor)
                        mp.put(arcos_agua, nodo_origen, sub_mapa_w)
                        
                    lista_vals_w = mp.get(sub_mapa_w, nodo_destino)
                    if lista_vals_w is None:
                        lista_vals_w = lt.new_list()
                        mp.put(sub_mapa_w, nodo_destino, lista_vals_w)
                    lt.add_last(lista_vals_w, agua_destino)

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
    lista_origenes_w = mp.key_set(arcos_agua)
    size_origenes_w = lt.size(lista_origenes_w)
    
    for i in range(size_origenes_w):
        origen = lt.get_element(lista_origenes_w, i)
        sub_mapa = mp.get(arcos_agua, origen)
        
        lista_destinos = mp.key_set(sub_mapa)
        size_destinos = lt.size(lista_destinos)
        
        for j in range(size_destinos):
            destino = lt.get_element(lista_destinos, j)
            lista_pesos = mp.get(sub_mapa, destino)
            
            suma = 0.0
            n_vals = lt.size(lista_pesos)
            for k in range(n_vals):
                suma += lt.get_element(lista_pesos, k)
            promedio = suma / n_vals
            
            digraph.add_edge(recursos_hidricos, origen, destino, promedio)

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


def req_3(catalog):
    """
    Retorna el resultado del requerimiento 3
    """
    # TODO: Modificar el requerimiento 3
    pass


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

def req_6(catalog):
    """
    Retorna el resultado del requerimiento 6
    """
    # TODO: Modificar el requerimiento 6
    pass


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
