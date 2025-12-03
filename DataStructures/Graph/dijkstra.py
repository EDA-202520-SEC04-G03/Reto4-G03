from DataStructures.Map import map_linear_probing as mp
from DataStructures.List import array_list as al
from DataStructures.Priority_queue import priority_queue as pq
from DataStructures.Queue import queue as q
from DataStructures.Stack import stack
from DataStructures.Graph import dijsktra_structure as ds
from DataStructures.Graph import edge as edg
from DataStructures.Graph import vertex as vx
import math


def dijkstra(my_graph, source):
    """
    Implementa el algoritmo de Dijkstra para encontrar los caminos mas baratos 
    desde el vertice source hasta todos sus vertices alcanzables.
    
    :param my_graph: El grafo de busqueda (digraph)
    :param source: La llave del vertice de inicio (any)
    :returns: Estructura resultante con la información para llegar a cada vertice 
              alcanzable desde el vertice source aplicando Dijkstra
    :rtype: dijkstra_structure
    """
    # Obtener el orden del grafo (número de vértices)
    g_order = mp.size(my_graph["vertices"])
    
    # Crear la estructura de Dijkstra
    search = ds.new_dijsktra_structure(source, g_order)
    
    # Inicializar todas las distancias como infinito
    vertices_keys = mp.key_set(my_graph["vertices"])
    for i in range(al.size(vertices_keys)):
        key = al.get_element(vertices_keys, i)
        mp.put(search["visited"], key, {
            "dist_to": math.inf,
            "edge_from": None
        })
    
    # La distancia al vértice fuente es 0
    mp.put(search["visited"], source, {
        "dist_to": 0.0,
        "edge_from": None
    })
    
    # Agregar el vértice fuente a la cola de prioridad
    search["pq"] = pq.insert(search["pq"], 0.0, source)
    
    # Procesar la cola de prioridad
    while not pq.is_empty(search["pq"]):
        # Extraer el vértice con menor distancia
        min_node = pq.del_min(search["pq"])
        current_key = min_node["key"]
        
        # Obtener el vértice actual del grafo
        current_vertex = mp.get(my_graph["vertices"], current_key)
        if current_vertex is None:
            continue
        
        # Obtener información del vértice actual
        current_info = mp.get(search["visited"], current_key)
        current_dist = current_info["dist_to"]
        
        # Obtener los vértices adyacentes
        adjacents = vx.get_adjacents(current_vertex)
        adjacent_keys = mp.key_set(adjacents)
        
        # Relajar cada arco saliente
        for i in range(al.size(adjacent_keys)):
            adj_key = al.get_element(adjacent_keys, i)
            edge = mp.get(adjacents, adj_key)
            
            # Calcular la nueva distancia
            edge_weight = edg.weight(edge)
            new_dist = current_dist + edge_weight
            
            # Obtener la distancia actual al vértice adyacente
            adj_info = mp.get(search["visited"], adj_key)
            old_dist = adj_info["dist_to"]
            
            # Si encontramos un camino más corto, actualizamos
            if new_dist < old_dist:
                mp.put(search["visited"], adj_key, {
                    "dist_to": new_dist,
                    "edge_from": current_key
                })
                
                # Actualizar o insertar en la cola de prioridad
                search["pq"] = pq.insert(search["pq"], new_dist, adj_key)
    
    return search


def dist_to(key_v, aux_structure):
    """
    Retorna el costo del camino para llegar del vertice source al vertice key_v.
    
    :param key_v: La llave del vertice destino (any)
    :param aux_structure: La estructura de busqueda resultante de Dijkstra (dijkstra_structure)
    :returns: El costo total para llegar de source a vertex. Infinito si no existe camino
    :rtype: float
    """
    vertex_info = mp.get(aux_structure["visited"], key_v)
    
    if vertex_info is None:
        return math.inf
    
    return vertex_info["dist_to"]


def has_path_to(key_v, aux_structure):
    """
    Indica si hay camino entre source y key_v.
    
    :param key_v: La llave del vertice de destino (any)
    :param aux_structure: La estructura de busqueda resultante de Dijkstra (dijkstra_structure)
    :returns: True si existe camino, False de lo contrario
    :rtype: bool
    """
    distance = dist_to(key_v, aux_structure)
    return distance != math.inf


def path_to(key_v, aux_structure):
    """
    Retorna el camino entre source y key_v en una pila.
    
    :param key_v: La llave del vertice de destino (any)
    :param aux_structure: La estructura de busqueda resultante de Dijkstra (dijkstra_structure)
    :returns: Una pila con los vertices del camino entre source y vertex. None si no hay camino.
    :rtype: stack
    """
    if not has_path_to(key_v, aux_structure):
        return None
    
    # Crear una pila para almacenar el camino
    path = stack.new_stack()
    
    # Reconstruir el camino desde key_v hasta source
    current = key_v
    
    while current is not None:
        stack.push(path, current)
        vertex_info = mp.get(aux_structure["visited"], current)
        current = vertex_info["edge_from"]
    
    return path