"""Los procesos no comparten memoria. Una lista que un proceso hijo modifica
es una copia: el padre no ve el cambio. Para que lo vea, la memoria tiene que
reservarse compartida desde el principio."""
import multiprocessing


def _llenar_tramo_lista(lista, ini, fin):
    for i in range(ini, fin):
        lista[i] = i * i


def llenar_lista(n, procesos):
    """Reparte el llenado de una lista entre varios procesos. Está escrito así
    a propósito: cada proceso llena su copia y el padre recibe la lista igual
    que la mandó."""
    lista = [0] * n
    paso = n // procesos
    hijos = []
    for p in range(procesos):
        ini, fin = p * paso, n if p == procesos - 1 else (p + 1) * paso
        hijos.append(multiprocessing.Process(target=_llenar_tramo_lista, args=(lista, ini, fin)))
    for h in hijos:
        h.start()
    for h in hijos:
        h.join()
    return lista


def llenar_compartido(n, procesos):
    """Llena memoria compartida repartiendo sus posiciones entre procesos.

    Reserva un multiprocessing.Array de enteros de 64 bits ('q'), reparte
    los tramos entre los procesos y devuelve el contenido como lista de Python.
    Cada proceso escribe posiciones distintas, así que no hace falta cerrojo."""
    compartido = multiprocessing.Array("q", n, lock=False)
    paso = n // procesos
    hijos = []
    for p in range(procesos):
        ini, fin = p * paso, n if p == procesos - 1 else (p + 1) * paso
        hijos.append(
            multiprocessing.Process(
                target=_llenar_tramo_lista,
                args=(compartido, ini, fin),
            )
        )
    for hijo in hijos:
        hijo.start()
    for hijo in hijos:
        hijo.join()
    return list(compartido)
