from DataStructures.Map import map_linear_probing as mp
from DataStructures.List import array_list as al
from DataStructures.Priority_queue import priority_queue as pq
from DataStructures.Queue import queue as q
from DataStructures.Stack import stack
from DataStructures.Graph import dijsktra_structure as ds
from DataStructures.Graph import edge as edg
from DataStructures.Graph import vertex as vx
import math

def bfs_vertex(my_graph, source, visited_map):
    """
    Realiza una búsqueda en anchura (BFS) desde el vértice source y marca los vértices visitados.
    
    :param my_graph: El grafo de búsqueda (digraph)
    :param source: La llave del vértice de inicio (any)
    :param visited_map: Mapa para registrar los vértices visitados (map)
    """
    # Crear una cola para la BFS
    queue = q.new_queue()
    
    # Marcar el vértice fuente como visitado (sin padre) y agregarlo a la cola
    mp.put(visited_map, source, {"visited": True, "parent": None})
    q.enqueue(queue, source)
    
    while not q.is_empty(queue):
        # Extraer el vértice actual de la cola
        current_key = q.dequeue(queue)
        
        # Obtener el vértice actual del grafo
        current_vertex = mp.get(my_graph["vertices"], current_key)
        if current_vertex is None:
            continue
        
        # Obtener los vértices adyacentes
        adjacents = vx.get_adjacents(current_vertex)
        adjacent_keys = mp.key_set(adjacents)
        
        # Procesar cada vértice adyacente
        for i in range(al.size(adjacent_keys)):
            adj_key = al.get_element(adjacent_keys, i)
            
            # Si el vértice adyacente no ha sido visitado, marcarlo y agregarlo a la cola
            if mp.get(visited_map, adj_key) is None:
                mp.put(visited_map, adj_key, {"visited": True, "parent": current_key})
                q.enqueue(queue, adj_key)
                

def bfs(my_graph, source):
    """
    Realiza una búsqueda en anchura (BFS) desde el vértice source.
    
    :param my_graph: El grafo de búsqueda (digraph)
    :param source: La llave del vértice de inicio (any)
    :returns: Mapa con los vértices visitados durante la búsqueda (map), cada uno con "visited" y "parent"
    :rtype: map
    """
    # Crear un mapa para registrar los vértices visitados
    visited_map = mp.new_map(num_elements=1000, load_factor=0.5)
    
    # Realizar la búsqueda en anchura
    bfs_vertex(my_graph, source, visited_map)
    
    return visited_map

def has_path_to_bfs(key_v, visited_map):
    """
    Indica si hay camino entre source y key_v basado en el mapa de visitados de BFS.
    
    :param key_v: La llave del vértice de destino (any)
    :param visited_map: Mapa con la información de vértices visitados durante la búsqueda (map)
    :returns: True si existe camino, False de lo contrario
    :rtype: bool
    """
    info = mp.get(visited_map, key_v)
    if info is None:
        return False
    return info.get("visited", False)


def path_to_bfs(key_v, visited_map):
    """
    Retorna el camino entre source y key_v en una pila basado en el mapa de visitados de BFS.
    
    :param key_v: La llave del vértice de destino (any)
    :param visited_map: Mapa con la información de vértices visitados durante la búsqueda (map)
    :returns: Una pila con los vértices del camino entre source y vertex. None si no hay camino.
    :rtype: stack
    """
    if not has_path_to_bfs(key_v, visited_map):
        return None
    
    # Crear una pila para almacenar el camino
    path = stack.new_stack()
    
    # Reconstruir el camino desde key_v hasta source usando los padres
    current = key_v
    
    while current is not None:
        stack.push(path, current)
        info = mp.get(visited_map, current)
        current = info.get("parent")
    
    return path