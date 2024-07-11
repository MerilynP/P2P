sta parte de la documentación del proyecto se centra en un Enfoque orientado a los problemas. Afrontarás tareas que podrías resolver, con la ayuda del código en este proyecto.

## ¿Como iniciar?
descargue el codigo del repositorio de este github en el mismo directorio que tu script de python.

    tu_proyecto/
    │
    ├── Proyect/
    │   ├── __init__.py
    │   └── ProyectoFinal.py
    │
    └── tu_script.py

Dentro de `tu_script.py` ahora puedes importar las funciones como: ecu_schrodinger_rk4(). 

module:

    # tu_script.py
    from Proyect.ProyectoFinal import ecu_schrodinger_rk4
   
Con la Matriz Hamiltoniana que define el sistema físico, podes definir una función para la evolución temporal según la ecuación de Schrödinger con paralelización. En esta función se definen las ecuaciones k1, k2, k3, k4.


	# tu_script.py

def ecu_schrodinger_rk4(matriz_ham, grilla_actual, dt): 
    k1 = dt * ecu_sch_paralelo(matriz_ham, grilla_actual) ## Calcular el primer paso de RK4.
    k2 = dt * ecu_sch_paralelo(matriz_ham, grilla_actual + 0.5 * k1) ## Calcula el segundo paso.
    k3 = dt * ecu_sch_paralelo(matriz_ham, grilla_actual + 0.5 * k2) ## Similar a k2.
    k4 = dt * ecu_sch_paralelo(matriz_ham, grilla_actual + k3) ## Utiliza k3 para calcular el último paso.
    grilla_nueva = grilla_actual + (k1 + 2*k2 + 2*k3 + k4) / 6 ## Sumatoria ponderada de los coeficientes k1, k2, k3 y k4.
    return grilla_nueva


