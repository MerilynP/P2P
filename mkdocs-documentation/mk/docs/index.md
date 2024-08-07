# MODELO DE TIGHT BINDING DE OCUPACIÓN SIMPLE CON POTENCIAL DEFINIDO: DINÁMICA
**Coordinador**: Marlon Brenes

El modelo de tight binding es uno de los modelos más fundamentales en ciencia de materiales, con capacidad de predicción en sistemas de, e.g., grafeno. El Hamiltoniano unidimensional fermiónico para particulas sin espín con condiciones no periódicas está dado por
$$\hat{H} = \sum_{i=1}^{N-1} t_i (c^\dagger_i c_{i+1} + c^\dagger_{i+1} c_i) + \sum_{i=1}^{N} \epsilon_i c^\dagger_i c_i $$

donde los $\hat{c_i}$ son operadores de destrucción fermiónica y los $\hat{c_i}^\dagger$ operadores de creación para el sitio de la grilla i. Para el caso
de un solo fermión en la grilla, este Hamiltoniano es una matriz de dimensión N de carácter tridiagonal. El comportamiento del sistema depende de los parámetros energéticos $t_i$ y $\epsilon_i$. La idea del proyecto es analizar la dinámica del sistema utilizando la misma de metodología del Proyecto: Modelo de Ising Cuántico Unidimensional en una Grilla de N Espines: Dinámica de Muchos Cuerpos.
Su metodología es la siguiente:
La dinámica de un estado puro para un sistema cuántico aislado se rige bajo la ecuación Schrödinger ( $\hbar = 1$ ):

$$
\frac{\partial |\psi(t)\rangle}{\partial t} = -i\hat{H} |\psi(t)\rangle,
$$

cuya solución formal está dada por

$$
|\psi(t)\rangle = e^{-i\hat{H}(t-t(_0))} |\psi(t = t(_0))\rangle.
$$

Es decir, la solución involucra resolver de manera numérica la ecuación diferencial o evaluar de alguna forma la exponencial de la matriz Eq. La idea del proyecto es evaluar la dinámica del modelo de Ising empezando de algún estado inicial.


## Milestones:
- Con base en argumentos numéricos, evaluar cual de las dos metodologías es mejor implementar para la solución numérica
- Construir la matriz Hamiltoniana
- Resolver el sistema y visualizar su dinámica
- Variar los parámetros energéticos y analizar la solución
- Implementar la solución en Python
- Encontrar una forma de paralelizar el algoritmo y evaluar la aceleración

