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
    # TODO: Imprimir el resultado del requerimiento 3
    pass


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
    """
    # TODO: Imprimir el resultado del requerimiento 6
    pass

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

        elif int(inputs) == 5:
            print_req_6(control)

        elif int(inputs) == 7:
            working = False
            print("\nGracias por utilizar el programa") 
        else:
            print("Opción errónea, vuelva a elegir.\n")
    sys.exit(0)
