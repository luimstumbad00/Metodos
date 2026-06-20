import sympy as sp

def integral_doble_numerica(expr_str, a, b, c, d, nx, ny, metodo="trapecio"):
    """
    Calcula integrales dobles sobre límites constantes [a,b] en x, y [c,d] en y.
    metodo: "trapecio" o "simpson13"
    nx, ny: Número de divisiones en x e y.
    """
    x, y = sp.symbols('x y')
    f = sp.lambdify((x, y), sp.sympify(expr_str), 'numpy')
    
    hx = (b - a) / nx
    hy = (d - c) / ny
    
    # Generar los puntos de la malla
    puntos_x = [a + i * hx for i in range(nx + 1)]
    puntos_y = [c + j * hy for j in range(ny + 1)]
    
    # Definición de pesos según el método
    def obtener_pesos(n, m_tipo):
        if m_tipo == "trapecio":
            return [1 if (i == 0 or i == n) else 2 for i in range(n + 1)]
        elif m_tipo == "simpson13":
            if n % 2 != 0:
                raise ValueError("Para Simpson 1/3, los subintervalos deben ser pares.")
            return [1 if (i == 0 or i == n) else (4 if i % 2 != 0 else 2) for i in range(n + 1)]
        else:
            raise ValueError("Método no reconocido.")

    pesos_x = obtener_pesos(nx, metodo)
    pesos_y = obtener_pesos(ny, metodo)
    
    suma = 0.0
    for i in range(nx + 1):
        for j in range(ny + 1):
            w = pesos_x[i] * pesos_y[j]
            suma += w * f(puntos_x[i], puntos_y[j])
            
    factor = (hx * hy) / (4 if metodo == "trapecio" else 9)
    return factor * suma