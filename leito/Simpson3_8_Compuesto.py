import sympy as sp

def simpson_38_compuesto(expr_str, a, b, n):
    """
    Método de Simpson 3/8 Compuesto.
    Nota: 'n' debe ser obligatoriamente un múltiplo de 3.
    """
    if n % 3 != 0:
        raise ValueError("El número de subintervalos (n) debe ser múltiplo de 3 para el método de Simpson 3/8.")
        
    x = sp.symbols('x')
    f = sp.lambdify(x, sp.sympify(expr_str), 'numpy')
    
    h = (b - a) / n
    suma = f(a) + f(b)
    
    for i in range(1, n):
        # Si el índice es múltiplo de 3, el peso es 2; si no, el peso es 3
        if i % 3 == 0:
            suma += 2 * f(a + i * h)
        else:
            suma += 3 * f(a + i * h)
            
    return (3 * h / 8) * suma