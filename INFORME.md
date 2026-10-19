# Informe

**Nombre y código:** Karen Andrea Sanabria González – 202459413

## Parte 1: tabla de tiempos

| Tarea | Secuencia | Hilos | Procesos |
|---|---:|---:|---:|
| Contar primos | 1621.6 ms | 1684.7 ms | 882.0 ms |
| Consultas lentas | 4001.5 ms | 1003.6 ms | 1246.4 ms |

**Qué forma ganó en cada tarea y qué papel juega el bloqueo global del intérprete:**

En la tarea de contar primos, la ejecución con procesos obtuvo el mejor rendimiento, con un tiempo de 882.0 ms, mientras que la ejecución secuencial tardó 1621.6 ms y la ejecución con hilos 1684.7 ms.

Esto ocurre porque contar números primos es una tarea que requiere principalmente operaciones de cálculo. En la configuración utilizada, el bloqueo global del intérprete (GIL) de Python impide que varios hilos ejecuten simultáneamente código Python dentro del mismo intérprete. Por esta razón, los hilos no consiguieron acelerar el cálculo e incluso tardaron un poco más debido a los costos de administración y coordinación.

En cambio, los procesos pueden ejecutar código Python de forma paralela en distintos núcleos del procesador, porque cada proceso tiene su propio intérprete. Esto permitió reducir el tiempo de ejecución aproximadamente un 45.6 % respecto a la versión secuencial.

Para la tarea de consultas lentas, los hilos obtuvieron el mejor resultado, con 1003.6 ms, frente a los 4001.5 ms de la ejecución secuencial y los 1246.4 ms de los procesos.

Esto se debe a que las consultas simuladas pasan gran parte del tiempo esperando. Durante esa espera, el hilo puede liberar el GIL y permitir que otros hilos avancen. Así, varias consultas pueden esperar simultáneamente, reduciendo considerablemente el tiempo total.

Los procesos también mejoraron el rendimiento, pero resultaron un poco más lentos que los hilos debido a los costos adicionales de creación, administración y comunicación entre procesos.

Por lo tanto, los resultados muestran que los procesos son más convenientes para las tareas de cálculo intensivo, mientras que los hilos resultan especialmente útiles para las tareas que requieren principalmente esperar.

## Parte 2: la actualización perdida

**Porcentaje de abonos perdidos en las cinco corridas sin cerrojo:**

En este ejercicio se utilizaron cuatro hilos que debían realizar 100000 abonos cada uno, para un total esperado de 400000 abonos.

| Corrida | Abonos esperados | Abonos obtenidos | Abonos perdidos | Porcentaje perdido |
|---|---:|---:|---:|---:|
| 1 | 400000 | 201265 | 198735 | 49.68 % |
| 2 | 400000 | 196827 | 203173 | 50.79 % |
| 3 | 400000 | 206992 | 193008 | 48.25 % |
| 4 | 400000 | 198952 | 201048 | 50.26 % |
| 5 | 400000 | 183528 | 216472 | 54.12 % |

En promedio, se perdió aproximadamente el **50.62 % de los abonos** cuando no se utilizó un cerrojo.

Al ejecutar las mismas cinco corridas utilizando un cerrojo, se obtuvo el resultado esperado de 400000 abonos en todas las ejecuciones, sin ninguna pérdida.

**Por qué se pierden, con los tres pasos de un abono en la explicación, y por qué el cerrojo lo evita:**

Los abonos se pierden porque varios hilos intentan modificar la misma variable compartida al mismo tiempo. Cada abono requiere tres operaciones:

1. Leer el valor actual del saldo.
2. Sumar una unidad al valor leído.
3. Escribir el nuevo valor en la variable compartida.

El problema ocurre cuando dos hilos leen el mismo saldo antes de que alguno termine de actualizarlo.

Por ejemplo, si el saldo es 100, dos hilos pueden leer ese mismo valor, sumar una unidad y escribir 101. Aunque se realizaron dos abonos, el saldo solamente aumentó una unidad. Esto se conoce como una condición de carrera o actualización perdida.

Para solucionar el problema se utiliza un cerrojo mediante `threading.Lock`, que permite que solamente un hilo ejecute la sección crítica a la vez.

De esta manera, las operaciones de leer, sumar y escribir se realizan juntas, sin que otro hilo pueda intervenir durante la actualización.

Los resultados demostraron que el cerrojo evita las pérdidas, ya que en las cinco ejecuciones se obtuvo exactamente el saldo esperado de 400000 abonos.

## Parte 3: memoria compartida

**Por qué `llenar_lista` devuelve la lista sin tocar y `llenar_compartido` no:**

La función `llenar_lista` utiliza procesos independientes para modificar una lista de Python. Sin embargo, los procesos no comparten automáticamente sus variables y estructuras de datos.

Cada proceso trabaja con su propia representación de la lista, por lo que los cambios realizados dentro de los procesos hijos no se reflejan directamente en la lista que conserva el proceso principal.

Por esta razón, cuando termina la ejecución, la función devuelve la lista original sin modificaciones.

En cambio, `llenar_compartido` utiliza `multiprocessing.Array`, que permite crear un arreglo ubicado en memoria compartida y accesible desde varios procesos.

Así, cuando los procesos escriben valores en el arreglo, los cambios pueden ser observados por el proceso principal.

Además, como cada proceso modifica posiciones diferentes del arreglo, no existe una competencia por escribir en la misma posición y no es necesario utilizar un cerrojo para proteger esas escrituras.

Las tres pruebas realizadas finalizaron correctamente, verificando que la lista convencional permanece sin modificar y que el arreglo compartido contiene los valores esperados.

## Parte 4: la cola

| Trabajadores | Tiempo |
|---|---:|
| Secuencia | 2495.1 ms |
| 1 | 2689.8 ms |
| 2 | 1436.8 ms |
| 4 | 1392.7 ms |

**Por qué de dos a cuatro trabajadores casi no se gana, y qué tarea marca el tiempo total:**

En este ejercicio se utilizó una cola de procesos para distribuir ocho tareas de duración desigual entre distintos trabajadores.

La ejecución secuencial tardó 2495.1 ms. Al utilizar un solo trabajador, el tiempo aumentó a 2689.8 ms, debido a que se añadió el costo de crear y administrar procesos y colas sin obtener paralelismo adicional.

Con dos trabajadores, el tiempo disminuyó a 1436.8 ms, porque las tareas pudieron ejecutarse de manera simultánea.

Sin embargo, al aumentar a cuatro trabajadores, el tiempo solamente se redujo a 1392.7 ms, una mejora aproximada del 3.1 % respecto a dos trabajadores.

Esto sucede porque las tareas tienen duraciones diferentes: algunas son largas y otras cortas. Aunque existan más trabajadores disponibles, no todos permanecen ocupados durante el mismo tiempo.

Cuando los trabajadores terminan las tareas cortas, pueden quedar esperando mientras otro trabajador continúa ejecutando una tarea larga.

Por lo tanto, el tiempo total está limitado principalmente por la tarea más larga que todavía se encuentra en ejecución y por la distribución del trabajo entre los procesos.

Este comportamiento muestra que aumentar el número de trabajadores no garantiza una reducción proporcional del tiempo, especialmente cuando las tareas tienen costos desiguales.

En conclusión, utilizar varios procesos permitió mejorar considerablemente el rendimiento frente a la ejecución secuencial, pero aumentar de dos a cuatro trabajadores produjo una mejora pequeña debido al desequilibrio entre las tareas y a los costos de coordinación.