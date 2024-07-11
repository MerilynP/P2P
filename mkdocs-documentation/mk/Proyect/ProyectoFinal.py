#!/usr/bin/env python3

import numpy as np
import time

from concurrent.futures import ThreadPoolExecutor #Se importa la clase "ThreadPoolExecutor" del módulo "concurrent.future", para trabajar con ejecuciones concurrentes en hilos.


# Función para crear el estado inicial (grilla)
def estado_inicial(N):
    estado_inicial = np.zeros(N)
    estado_inicial[N//2] = 1  # Colocar un fermión en el centro de la grilla
    return estado_inicial

# Función para crear la matriz Hamiltoniana
def matriz_ham(t_i, epsilon):
    N = epsilon.size
    matriz = np.zeros((N, N))
    matriz[np.diag_indices(N)] = epsilon 
    np.fill_diagonal(matriz[:,1:], t_i)
    np.fill_diagonal(matriz[1:,:], t_i)
    return matriz

# Función para la evolución temporal según la ecuación de Schrödinger con paralelización
def ecu_schrodinger_rk4(matriz_ham, grilla_actual, dt):
    k1 = dt * ecu_sch_paralelo(matriz_ham, grilla_actual)
    k2 = dt * ecu_sch_paralelo(matriz_ham, grilla_actual + 0.5 * k1)
    k3 = dt * ecu_sch_paralelo(matriz_ham, grilla_actual + 0.5 * k2)
    k4 = dt * ecu_sch_paralelo(matriz_ham, grilla_actual + k3)
    grilla_nueva = grilla_actual + (k1 + 2*k2 + 2*k3 + k4) / 6
    return grilla_nueva

# Función para dividir el trabajo entre varios hilos
def parte_ecu_sch(matriz_ham, grilla_actual, start, end): #Índices de inicio y fin para la porción de trabajo que manejará un hilo
    return -1j * matriz_ham[start:end, :] @ grilla_actual #multiplicación matricial entre "matriz_ham" y "grilla_actual"(-1j es la unidad imaginaria negativa)

# Función para paralelizar el cálculo de ecu_sch
def ecu_sch_paralelo(matriz_ham, grilla_actual, num_hilos=1): #se define el número de hilos que se usarán para paralelizar el cálculo (por defecto)
    N = len(grilla_actual) #longitud de la grilla
    step = N // num_hilos #cantidad de elementos de la grilla que cada hilo procesará 

# en la función "ecu_sch_paralelo" se divide el trabajo de multiplicación matricial en múltiples hilos utilizando "ThreadPoolExecutor", donde cada hilo calcula una porción de la grilla según los índices start y end.
    
    resultados = np.zeros_like(grilla_actual, dtype=complex) #almacenar resultados parciales
    
    with ThreadPoolExecutor(max_workers=num_hilos) as executor: #se crea un pool de hilos,(forma de manejar y distribuir la ejecución de tareas entre varios hilos de manera eficiente), con "max_workers" especificado como num_hilos
        futuros = [] #Lista para almacenar los objetos Future que representan los resultados futuros de las operaciones asincrónicas.
        for i in range(num_hilos): #bucle que itera sobre el número de hilos para dividir el trabajo
            start = i * step
            end = (i + 1) * step if i != num_hilos - 1 else N #nicio y fin para la porción de la grilla que cada hilo procesará
            futuros.append(executor.submit(parte_ecu_sch, matriz_ham, grilla_actual, start, end)) #retorna el resultado "Future"
        
        for future in futuros:
            resultado = future.result() #resultado devuelto por "parte_ecu_sch" 
            start = futuros.index(future) * step
            end = (start + step) if futuros.index(future) != num_hilos - 1 else N #Calcula nuevamente los índices de inicio y fin para determinar dónde deben colocarse los resultados en el array resultados.
            resultados[start:end] = resultado #Asigna los resultados calculados por cada hilo
    
    return resultados

#Resultados de cada hilo se combinan en el array "resultados".

# Función principal para evolucionar la grilla en el tiempo
def inicio(t_i, epsilon, tiempos):
    dt = tiempos[1] - tiempos[0]
    N = epsilon.size
    grilla_actual = estado_inicial(N)
    matriz_hamiltoniana = matriz_ham(t_i, epsilon)
    shape = [0.0 for i in range(len(tiempos))]
    shape[0] = np.abs(grilla_actual)**2
    for t in range(1, tiempos.size):
        shape[t] = np.abs(grilla_actual)**2
        grilla_actual = ecu_schrodinger_rk4(matriz_hamiltoniana, grilla_actual, dt)
        
    return shape, grilla_actual

# Ejemplo de uso
if __name__ == "__main__":
    N = 100
    epsilon_val = 0.5 * np.ones(N)
    t_i_val = 1 * np.ones(N)
    tiempos_val = np.linspace(0.0, 25, 200) 

    num_hilos_lista = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]  #lista que contiene diferentes cantidades de hilos con las cuales se va a ejecutar el programa

    for num_hilos in num_hilos_lista: #Este bucle "for" itera sobre cada valor de "num_hilos"
        print(f"Ejecutando con {num_hilos} hilo(s)...")
        start_time = time.time() #Registra el tiempo de inicio de la ejecución del programa utilizando la función "time.time()" del "módulo time"
        s, g = inicio(t_i_val, epsilon_val, tiempos_val) #Llama a la función inicio con los parámetros "t_i_val", "epsilon_val" y "tiempos_val". Esta función representa el punto de entrada principal donde se realiazan los cálculos
        elapsed_time = time.time() - start_time #duración total de la ejecución del programa en segundos
        print(f"Tiempo de ejecución: {elapsed_time:.4f} segundos")
        print()

