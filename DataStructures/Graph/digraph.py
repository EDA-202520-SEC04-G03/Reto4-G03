import DataStructures.Graph.dfo_structure as dfo
import DataStructures.Graph.dijsktra_structure as ds 
import DataStructures.Graph.edge as edge
import DataStructures.Graph.prim_structure as ps
import DataStructures.Graph.vertex as vertex
from DataStructures.Map import map_linear_probing as mp
from DataStructures.List import array_list as al


def new_graph(order):
    
    initial_capacity = max(order, 10)
    
    graph = {
        "vertices": mp.new_map(initial_capacity, 0.5),
        "num_edges": 0
    }
    return graph


def insert_vertex(my_graph, key_u, info_u):
    
    new_vertex = vertex.new_vertex(key_u, info_u)
    my_graph["vertices"] = mp.put(my_graph["vertices"], key_u, new_vertex)
    return my_graph


def add_edge(my_graph, key_u, key_v, weight=1.0):
    
    
    # Verificar si existe el vertice key_u
    vertex_u = mp.get(my_graph["vertices"], key_u)
    if vertex_u is None:
        raise Exception("El vertice u no existe")
    
    # Verificar si existe el vertice key_v
    vertex_v = mp.get(my_graph["vertices"], key_v)
    if vertex_v is None:
        raise Exception("El vertice v no existe")
    
    # Verificar si el arco ya existe
    edge_exists = vertex.get_edge(vertex_u, key_v)
    
    # Agregar el arco desde key_u hacia key_v
    vertex.add_adjacent(vertex_u, key_v, weight)
    
    # Si el arco no existía, incrementar el contador de arcos
    if edge_exists is None:
        my_graph["num_edges"] += 1
    
    return my_graph


def contains_vertex(my_graph, key_u):
    return mp.contains(my_graph["vertices"], key_u)

def order(my_graph):
    return mp.size(my_graph["vertices"])

def size(my_graph):
    return my_graph["num_edges"]

def get_vertex(my_graph, key_u):
    return mp.get(my_graph["vertices"], key_u)

def degree(my_graph, key_u):

    vertex_u = get_vertex(my_graph, key_u)
    if vertex_u is None:
        raise Exception("El vertice no existe")

    return vertex.degree(vertex_u)

def adjacents(my_graph, key_u):
    vertex_u = get_vertex(my_graph, key_u)
    if vertex_u is None:
        raise Exception("El vertice no existe")

    adjacents = vertex.get_adjacents(vertex_u)
    keys_adjacents = mp.key_set(adjacents)
    return keys_adjacents

def vertices(my_graph):
    return mp.key_set(my_graph["vertices"])

def edges_vertex(my_graph, key_u):

    vertex_u = get_vertex(my_graph, key_u)
    if vertex_u is None:
        raise Exception("El vertice no existe")
    
    adjacents = vertex.get_adjacents(vertex_u)

    return mp.value_set(adjacents)

def update_vertex_info(my_graph, key_u, new_info):
    vertex_u = get_vertex(my_graph, key_u)
    if vertex_u is None:
        return my_graph
    
    vertex.set_value(vertex_u, new_info)
    return my_graph
    
def get_vertex_information(my_graph, key_u):
    vertex_u = get_vertex(my_graph, key_u)
    if vertex_u is None:
        raise Exception("El vertice no existe")
    
    return vertex.get_value(vertex_u)
    