def euler(f, x0, y0, h):
    """
    Realiza una iteración del método de Euler para resolver ODEs.

    Args:
        f: Función derivada, f(x, y).
        x0: Valor inicial de x.
        y0: Valor inicial de y.
        h: Tamaño del paso.

    Returns:
        Nuevo valor de y después de un paso h.
    """
    return y0 + h * f(x0, y0)


def rk2(f, x0, y0, h):
    """
    Realiza una iteración del método de Runge-Kutta de segundo orden (RK2).

    Args:
        f: Función derivada, f(x, y).
        x0: Valor inicial de x.
        y0: Valor inicial de y.
        h: Tamaño del paso.

    Returns:
        Nuevo valor de y después de un paso h.
    """
    k1 = f(x0, y0)
    k2 = f(x0 + h, y0 + h * k1)
    return y0 + (h / 2) * (k1 + k2)


def rk4(f, x0, y0, h):
    """
    Realiza una iteración del método de Runge-Kutta de cuarto orden (RK4) para resolver ODEs.

    Args:
        f: Función derivada, f(x, y).
        x0: Valor inicial de x.
        y0: Valor inicial de y.
        h: Tamaño del paso.

    Returns:
        Nuevo valor de y después de un paso h.
    """
    k1 = f(x0, y0)
    k2 = f(x0 + h/2, y0 + h/2 * k1)
    k3 = f(x0 + h/2, y0 + h/2 * k2)
    k4 = f(x0 + h, y0 + h * k3)

    return y0 + (h/6) * (k1 + 2*k2 + 2*k3 + k4)
