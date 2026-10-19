"""Un grupo de procesos que toman tareas de una cola a medida que se
desocupan. La cola reparte por demanda: el proceso que termina antes toma la
siguiente tarea, y ninguno se queda esperando a los demás."""
import multiprocessing


def _trabajador(cola_tareas, cola_resultados, funcion):
    while True:
        tarea = cola_tareas.get()
        if tarea is None:
            return
        indice, argumento = tarea
        cola_resultados.put((indice, funcion(argumento)))


def con_cola(funcion, argumentos, procesos):
    """Ejecuta las tareas mediante procesos trabajadores y dos colas.

    El índice permite devolver los resultados en el orden de los argumentos,
    aunque los trabajadores terminen en otro orden.
    """
    cola_tareas = multiprocessing.Queue()
    cola_resultados = multiprocessing.Queue()
    trabajadores = [
        multiprocessing.Process(
            target=_trabajador,
            args=(cola_tareas, cola_resultados, funcion),
        )
        for _ in range(procesos)
    ]
    for trabajador in trabajadores:
        trabajador.start()

    for indice, argumento in enumerate(argumentos):
        cola_tareas.put((indice, argumento))
    for _ in trabajadores:
        cola_tareas.put(None)

    resultados = [None] * len(argumentos)
    for _ in argumentos:
        indice, resultado = cola_resultados.get()
        resultados[indice] = resultado

    for trabajador in trabajadores:
        trabajador.join()
    cola_tareas.close()
    cola_resultados.close()
    return resultados
