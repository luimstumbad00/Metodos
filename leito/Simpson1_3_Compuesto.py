import sympy as sp

def simpson_13_compuesto(expr_str, a, b, n):
    """
    Método de Simpson 1/3 Compuesto.
    n debe ser un número par.
    """
    if n % 2 != 0:
        raise ValueError("El número de subintervalos 'n' debe ser par para Simpson 1/3.")
        
    x = sp.symbols('x')
    f = sp.lambdify(x, sp.sympify(expr_str), 'numpy')
    
    h = (b - a) / n
    suma = f(a) + f(b)
    
    for i in range(1, n):
        if i % 2 == 0:
            suma += 2 * f(a + i * h)
        else:
            suma += 4 * f(a + i * h)
            
    return (h / 3) * suma