from DataStructures.Map import map_linear_probing as mp
from DataStructures.List import array_list as lt
from DataStructures.Stack import stack
from DataStructures.Queue import queue as q
from DataStructures.Graph import digraph
from DataStructures.Graph import vertex as vx
from DataStructures.Graph import dfo_structure as dfo


def depth_first_order(my_graph):
    """
    Realiza un recorrido en profundidad del grafo para obtener
    el orden de los vértices en preorden, postorden y postorden inverso.
    
    :param my_graph: El grafo a recorrer (digraph)
    :returns: Estructura dfo con marked, pre, post, reversepost
    :rtype: dfo_structure
    """
    g_order = digraph.order(my_graph)
    search = dfo.new_dfo_structure(g_order)
    vertices_keys = digraph.vertices(my_graph)
    
    for i in range(lt.size(vertices_keys)):
        vertex_key = lt.get_element(vertices_keys, i)
        if mp.get(search["marked"], vertex_key) is None:
            dfs_order(my_graph, vertex_key, search)
    
    return search


def dfs_order(my_graph, vertex_key, search):
    """
    Realiza DFS recursivo para llenar las estructuras de orden.
    
    :param my_graph: El grafo (digraph)
    :param vertex_key: La llave del vértice actual
    :param search: La estructura dfo_structure
    """
    mp.put(search["marked"], vertex_key, True)
    q.enqueue(search["pre"], vertex_key)
    
    current_vertex = digraph.get_vertex(my_graph, vertex_key)
    if current_vertex is not None:
        adjacents = vx.get_adjacents(current_vertex)
        adjacent_keys = mp.key_set(adjacents)
        
        for i in range(lt.size(adjacent_keys)):
            adj_key = lt.get_element(adjacent_keys, i)
            if mp.get(search["marked"], adj_key) is None:
                dfs_order(my_graph, adj_key, search)
    
    q.enqueue(search["post"], vertex_key)
    stack.push(search["reversepost"], vertex_key)


def has_cycle(my_graph):
    """
    Detecta si el grafo tiene ciclos usando DFS con colores.
    
    :param my_graph: El grafo a verificar (digraph)
    :returns: Tupla (bool, list) - (tiene ciclo, ejemplo de ciclo si existe)
    """
    g_order = digraph.order(my_graph)
    colors = mp.new_map(g_order, 0.5)
    vertices_keys = digraph.vertices(my_graph)
    
    # Inicializar todos los nodos como "white" (no visitados)
    for i in range(lt.size(vertices_keys)):
        vertex_key = lt.get_element(vertices_keys, i)
        mp.put(colors, vertex_key, "white")
    
    # Intentar DFS desde cada nodo no visitado
    for i in range(lt.size(vertices_keys)):
        vertex_key = lt.get_element(vertices_keys, i)
        if mp.get(colors, vertex_key) == "white":
            # Usar una pila para simular la recursión y evitar stack overflow
            cycle_found, cycle_path = dfs_cycle_iterative(my_graph, vertex_key, colors)
            if cycle_found:
                return True, cycle_path
    
    return False, None


def dfs_cycle_iterative(my_graph, start_vertex, colors):
    """
    DFS iterativo para detectar ciclos usando una pila explícita.
    
    :returns: Tupla (bool, list) - (encontró ciclo, camino del ciclo)
    """
    # Pila para simular la recursión: (nodo_actual, índice_adyacente, fase)
    # fase: 0 = primera visita (marcar gray), 1 = después de explorar hijos (marcar black)
    stack_dfs = [(start_vertex, 0, 0)]
    parent = mp.new_map(digraph.order(my_graph), 0.5)
    mp.put(parent, start_vertex, None)
    
    while len(stack_dfs) > 0:
        vertex_key, adj_index, phase = stack_dfs.pop()
        
        if phase == 0:
            # Primera visita: marcar como "gray"
            color = mp.get(colors, vertex_key)
            
            if color == "gray":
                # Ya está siendo procesado, esto no debería pasar en DFS correcto
                continue
            
            mp.put(colors, vertex_key, "gray")
            
            # Agregar de nuevo a la pila para marcarlo como "black" después
            stack_dfs.append((vertex_key, adj_index, 1))
            
            # Obtener adyacentes
            current_vertex = digraph.get_vertex(my_graph, vertex_key)
            if current_vertex is not None:
                adjacents = vx.get_adjacents(current_vertex)
                adjacent_keys = mp.key_set(adjacents)
                
                # Procesar cada adyacente
                for i in range(lt.size(adjacent_keys)):
                    adj_key = lt.get_element(adjacent_keys, i)
                    adj_color = mp.get(colors, adj_key)
                    
                    if adj_color == "gray":
                        # ¡Encontramos un ciclo!
                        # Reconstruir el ciclo desde adj_key hasta vertex_key
                        cycle = [adj_key]
                        current = vertex_key
                        visited_in_path = {adj_key}
                        
                        # Seguir los padres hasta encontrar adj_key o un límite
                        max_iterations = digraph.order(my_graph) + 1
                        iterations = 0
                        
                        while current is not None and current != adj_key and iterations < max_iterations:
                            if current in visited_in_path:
                                # Detectamos un bucle en la reconstrucción, abortamos
                                break
                            cycle.append(current)
                            visited_in_path.add(current)
                            current = mp.get(parent, current)
                            iterations += 1
                        
                        if current == adj_key:
                            cycle.append(adj_key)
                        
                        cycle.reverse()
                        return True, cycle
                    
                    elif adj_color == "white":
                        # Nodo no visitado, agregarlo a la pila
                        mp.put(parent, adj_key, vertex_key)
                        stack_dfs.append((adj_key, 0, 0))
        
        elif phase == 1:
            # Segunda visita: marcar como "black" (completamente procesado)
            mp.put(colors, vertex_key, "black")
    
    return False, None


def topological_sort(my_graph):
    """
    Realiza un ordenamiento topológico del grafo si es un DAG.
    
    :param my_graph: El grafo (digraph)
    :returns: Lista con el orden topológico o None si hay ciclos
    """
    has_cycles, _ = has_cycle(my_graph)
    
    if has_cycles:
        return None
    
    dfo_search = depth_first_order(my_graph)
    topo_order = lt.new_list()
    
    while not stack.is_empty(dfo_search["reversepost"]):
        vertex = stack.pop(dfo_search["reversepost"])
        lt.add_last(topo_order, vertex)
    
    return topo_order