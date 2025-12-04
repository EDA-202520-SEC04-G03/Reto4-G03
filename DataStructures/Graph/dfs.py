from DataStructures.Map import map_linear_probing as mp
from DataStructures.List import array_list as al
from DataStructures.Stack import stack
from DataStructures.Graph import vertex as vx
from DataStructures.Stack import stack 

def dfs_vertex(my_graph, vertex, visited_map, parent):
    """
    Realiza una búsqueda en profundidad (DFS) desde un vértice dado en el grafo.

    :param my_graph: El grafo de búsqueda (digraph)
    :param vertex: La llave del vértice de inicio (any)
    :param visited_map: Mapa para rastrear los vértices visitados (map_linear_probing)
    :param parent: Llave del vértice padre en el árbol de DFS (any o None)
    """
    # Marcar el vértice actual como visitado y guardar su padre
    mp.put(visited_map, vertex, {"visited": True, "parent": parent})

    # Obtener el vértice actual del grafo
    current_vertex = mp.get(my_graph["vertices"], vertex)
    if current_vertex is None:
        return

    # Obtener los vértices adyacentes
    adjacents = vx.get_adjacents(current_vertex)
    adjacent_keys = mp.key_set(adjacents)

    # Recorrer cada vértice adyacente
    for i in range(al.size(adjacent_keys)):
        neighbor_key = al.get_element(adjacent_keys, i)

        # Si el vecino no ha sido visitado, realizar DFS recursivo
        info = mp.get(visited_map, neighbor_key)
        if info is None:
            dfs_vertex(my_graph, neighbor_key, visited_map, vertex)


def dfs(my_graph, source):
    """
    Realiza una búsqueda en profundidad (DFS) desde el vértice source.

    :param my_graph: El grafo de búsqueda (digraph)
    :param source: La llave del vértice de inicio (any)
    :returns: Mapa con los vértices visitados durante la búsqueda (map_linear_probing)
              Cada entrada tiene: {"visited": bool, "parent": key o None}
    :rtype: map_linear_probing
    """
    # Crear un mapa para registrar los vértices visitados
    visited_map = mp.new_map(num_elements=1000, load_factor=0.5)

    # Iniciar la DFS desde el vértice fuente (sin padre)
        # Iniciar desde el vértice fuente
    st = stack.new_stack()
    stack.push(st, source)
    mp.put(visited_map, source, {"visited": True, "parent": None})

    # DFS iterativo
    while not stack.is_empty(st):
        current = stack.pop(st)

        # Obtener el vértice actual del grafo
        current_vertex = mp.get(my_graph["vertices"], current)
        if current_vertex is None:
            continue

        # Obtener los vértices adyacentes
        adjacents = vx.get_adjacents(current_vertex)
        adjacent_keys = mp.key_set(adjacents)

        # Recorrer cada vértice adyacente
        size_adj = al.size(adjacent_keys)
        i = 0
        while i < size_adj:
            neighbor_key = al.get_element(adjacent_keys, i)

            # Si el vecino no ha sido visitado, marcarlo y apilarlo
            info = mp.get(visited_map, neighbor_key)
            if info is None:
                mp.put(visited_map, neighbor_key, {"visited": True, "parent": current})
                stack.push(st, neighbor_key)

            i += 1


    return visited_map


def has_path_to(key_v, visited_map):
    """
    Verifica si existe un camino hacia el vértice con la llave key_v en el mapa de visitados.

    :param key_v: La llave del vértice a verificar (any)
    :param visited_map: Mapa con los vértices visitados (map_linear_probing)
    :returns: True si existe un camino hacia el vértice, False en caso contrario (bool)
    """
    info = mp.get(visited_map, key_v)
    if info is None:
        return False
    return info.get("visited", False)


def path_to(key_v, visited_map):
    """
    Retorna el camino desde la raíz de la DFS hasta el vértice key_v si existe.

    :param key_v: La llave del vértice destino (any)
    :param visited_map: Mapa con los vértices visitados (map_linear_probing)
    :returns: Lista con el camino en orden [source, ..., key_v] o None si no existe
    :rtype: list or None
    """
    if not has_path_to(key_v, visited_map):
        return None

    # Reconstruir el camino usando los padres, guardándolo primero en una pila
    path_stack = stack.new_stack()
    current = key_v

    while current is not None:
        stack.push(path_stack, current)
        info = mp.get(visited_map, current)
        current = info.get("parent")

    # Pasar de la pila a una lista en orden source → key_v
    path = []
    while not stack.is_empty(path_stack):
        vertex_key = stack.pop(path_stack)
        path.append(vertex_key)

    return path