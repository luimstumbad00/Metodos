import sympy as sp

def trapecio_compuesto(expr_str, a, b, n):
    """
    Método de Integración del Trapecio Compuesto.
    expr_str: String de la función (ej. "x**2")
    a, b: Límites de integración
    n: Número de subintervalos
    """
    x = sp.symbols('x')
    f = sp.lambdify(x, sp.sympify(expr_str), 'numpy')
    
    h = (b - a) / n
    suma = f(a) + f(b)
    
    for i in range(1, n):
        suma += 2 * f(a + i * h)
        
    return (h / 2) * suma

# Ejemplo de uso independiente:
# print(trapecio_compuesto("x**2", 0, 1, 100))