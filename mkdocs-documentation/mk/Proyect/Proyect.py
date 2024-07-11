#!/usr/bin/env python3

## Se implementaron las siguientes bibliotecas que permiten realizar los calculos.
import numpy as np ## Esencial para el procesamiento numérico eficiente.
import time ## Proporciona funciones para trabajar con el tiempo y medir el tiempo de ejecución.

from concurrent.futures import ThreadPoolExecutor #Se importa la clase "ThreadPoolExecutor" del módulo "concurrent.future", para trabajar con ejecuciones concurrentes en hilos.

## Este módulo proporciona funciones para simular la evolución temporal de un sistema cuántico utilizando el método de Runge-Kutta de cuarto orden y paralelización mediante hilos.

## Funciones

## Función para crear el estado inicial (grilla). 
## Se toma como parámetro N, el mismo representará el tamaño de la grilla. Asegurando que el fermión se coloque en la posición central si N es impar.

def estado_inicial(N):
    estado_inicial = np.zeros(N) #Se crea un arreglo NumPy de longitud N lleno de ceros (np.zeros(N)).
    estado_inicial[N//2] = 1  # Se coloca un fermión en la posición central de la grilla . Aquí N//2 calcula el índice medio de la grilla, 
    return estado_inicial
 
 
## Función para crear la matriz Hamiltoniana.Determinación del Tamaño.

def matriz_ham(t_i, epsilon):
    N = epsilon.size ## Determina el tamaño del arreglo epsilon.
    matriz = np.zeros((N, N)) ## Inicializa una matriz NxN llena de ceros.
    matriz[np.diag_indices(N)] = epsilon ## Se asignan los valores a los elementos que se hallan en la diagonal de la matriz.
    np.fill_diagonal(matriz[:,1:], t_i) ## Se establece los valores de t_i en las posiciones por encima de la diagonal principal.
    np.fill_diagonal(matriz[1:,:], t_i) ## Se establece los valores de t_i en las posiciones por debajo de la diagonal principal.
    return matriz
    

## Función para la evolución temporal según la ecuación de Schrödinger con paralelización.
## Matriz Hamiltoniana que define el sistema físico.
def ecu_schrodinger_rk4(matriz_ham, grilla_actual, dt): 
    k1 = dt * ecu_sch_paralelo(matriz_ham, grilla_actual) ## Calcular el primer paso de RK4.
    k2 = dt * ecu_sch_paralelo(matriz_ham, grilla_actual + 0.5 * k1) ## Calcula el segundo paso.
    k3 = dt * ecu_sch_paralelo(matriz_ham, grilla_actual + 0.5 * k2) ## Similar a k2.
    k4 = dt * ecu_sch_paralelo(matriz_ham, grilla_actual + k3) ## Utiliza k3 para calcular el último paso.
    grilla_nueva = grilla_actual + (k1 + 2*k2 + 2*k3 + k4) / 6 ## Sumatoria ponderada de los coeficientes k1, k2, k3 y k4.
    return grilla_nueva


## Función para dividir el trabajo entre varios hilos.
def parte_ecu_sch(matriz_ham, grilla_actual, start, end): ## Índices de inicio y fin para la porción de trabajo que manejará un hilo.
    return -1j * matriz_ham[start:end, :] @ grilla_actual ## Multiplicación matricial entre "matriz_ham" y "grilla_actual"(-1j es la unidad imaginaria negativa).


## Función para paralelizar el cálculo de ecu_sch.
## Se define el número de hilos que se usarán para paralelizar el cálculo. Para cada hilo, se calcula una parte local de la ecuación de Schrödinger, además se indica qué parte de la grilla debe manejar cada hilo.
## En la función "ecu_sch_paralelo" se divide el trabajo de multiplicación matricial en múltiples hilos utilizando "ThreadPoolExecutor", donde cada hilo calcula una porción de la grilla según los índices start y end.

def ecu_sch_paralelo(matriz_ham, grilla_actual, num_hilos=1): 
    N = len(grilla_actual) ## Longitud de la grilla.
    step = N // num_hilos ## Cantidad de elementos de la grilla que cada hilo procesará.  
    resultados = np.zeros_like(grilla_actual, dtype=complex) ## Almacenar resultados parciales.
    
    with ThreadPoolExecutor(max_workers=num_hilos) as executor: ## Se crea un pool de hilos,(forma de manejar y distribuir la ejecución de tareas entre varios hilos de manera eficiente), con "max_workers" especificado como num_hilos.
        futuros = [] ## Lista para almacenar los objetos Future que representan los resultados futuros de las operaciones asincrónicas.
        for i in range(num_hilos): ## Bucle que itera sobre el número de hilos para dividir el trabajo.
            start = i * step
            end = (i + 1) * step if i != num_hilos - 1 else N ## Inicio y fin para la porción de la grilla que cada hilo procesará.
            futuros.append(executor.submit(parte_ecu_sch, matriz_ham, grilla_actual, start, end)) ## Retorna el resultado "Future".
        
        for future in futuros:
            resultado = future.result() ## Resultado devuelto por "parte_ecu_sch". 
            start = futuros.index(future) * step
            end = (start + step) if futuros.index(future) != num_hilos - 1 else N ## Calcula nuevamente los índices de inicio y fin para determinar dónde deben colocarse los resultados en el array resultados.
            resultados[start:end] = resultado ## Asigna los resultados calculados por cada hilo.
    
    return resultados ## Resultados de cada hilo se combinan en el array "resultados".


# Función principal para evolucionar la grilla en el tiempo.
def inicio(t_i, epsilon, tiempos):
    dt = tiempos[1] - tiempos[0] ## Calcula el paso de tiempo dt basado en la diferencia entre los primeros dos elementos de tiempos.
    N = epsilon.size ## Determina el tamaño del arreglo.
    grilla_actual = estado_inicial(N) ## Inicializa la función de onda en el tiempo inicial.
    matriz_hamiltoniana = matriz_ham(t_i, epsilon) ## Calcula la matriz Hamiltoniana con los parámetros definidos.
    shape = [0.0 for i in range(len(tiempos))] ## Inicializa un arreglo.
    shape[0] = np.abs(grilla_actual)**2 ## Almacena la forma inicial de la función de onda al cuadrado.
    ## Bucle de intragración temporal.
    for t in range(1, tiempos.size):
        shape[t] = np.abs(grilla_actual)**2
        grilla_actual = ecu_schrodinger_rk4(matriz_hamiltoniana, grilla_actual, dt)
        
    return shape, grilla_actual

## Ejemplo de uso
if __name__ == "__main__":
    N = 100 ## Tamaño del sistema.
    epsilon_val = 0.5 * np.ones(N) ## Valores de la diagonal de matriz Hamiltoniana.
    t_i_val = 1 * np.ones(N) ## Elementos fuera de la diagonal de matriz Hamiltoniana.
    tiempos_val = np.linspace(0.0, 25, 200) ## Tiempos para los cuales se evaluará la función de onda.

    num_hilos_lista = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12] ## Lista que contiene diferentes cantidades de hilos con las cuales se va a ejecutar el programa.

    for num_hilos in num_hilos_lista: ## Este bucle "for" itera sobre cada valor de "num_hilos".
        print(f"Ejecutando con {num_hilos} hilo(s)...")
        start_time = time.time() ## Registra el tiempo de inicio de la ejecución del programa utilizando la función "time.time()" del "módulo time".
        s, g = inicio(t_i_val, epsilon_val, tiempos_val) ## Llama a la función inicio con los parámetros "t_i_val", "epsilon_val" y "tiempos_val". Esta función representa el punto de entrada principal donde se realiazan los cálculos.
        elapsed_time = time.time() - start_time ## Duración total de la ejecución del programa en segundos.
        print(f"Tiempo de ejecución: {elapsed_time:.4f} segundos") ## Se imprime el tiempo de ejecución de cada simulación.
        print()

