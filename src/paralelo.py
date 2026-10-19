"""Tres formas de ejecutar la misma lista de tareas.

Cada función recibe la función a ejecutar y la lista de argumentos, y devuelve
la lista de resultados en el mismo orden de los argumentos.
"""
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor


def en_secuencia(funcion, argumentos):
    """Ejecuta las tareas una tras otra. Es el punto de comparación."""
    return [funcion(a) for a in argumentos]


def con_hilos(funcion, argumentos):
    """Ejecuta las tareas con un grupo de hilos.

    ``map`` conserva el orden de los argumentos aunque las tareas terminen en
    otro orden.
    """
    with ThreadPoolExecutor() as ejecutor:
        return list(ejecutor.map(funcion, argumentos))


def con_procesos(funcion, argumentos):
    """Ejecuta las tareas en procesos y conserva el orden de los resultados."""
    with ProcessPoolExecutor() as ejecutor:
        return list(ejecutor.map(funcion, argumentos))
