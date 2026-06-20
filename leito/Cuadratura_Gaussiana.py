import sympy as sp

# Pesos y nodos estándar en el intervalo [-1, 1]
GAUSS_DATA = {
    2: ([-0.5773502691896257, 0.5773502691896257], [1.0, 1.0]),
    3: ([-0.7745966692414834, 0.0, 0.7745966692414834], [0.5555555555555556, 0.8888888888888888, 0.5555555555555556]),
    4: ([-0.8611363115940526, -0.3399810435848563, 0.3399810435848563, 0.8611363115940526], 
        [0.3478548451374538, 0.6521451548625461, 0.6521451548625461, 0.3478548451374538]),
    5: ([-0.9061798459386640, -0.5384693101056831, 0.0, 0.5384693101056831, 0.9061798459386640],
        [0.2369268850561891, 0.4786286704993665, 0.5688888888888889, 0.4786286704993665, 0.2369268850561891])
}

def cuadratura_gaussiana(expr_str, a, b, puntos=3, n_subintervalos=1):
    """
    Cuadratura Gauss-Legendre.
    puntos: 2, 3, 4 o 5.
    n_subintervalos: Si es 1 es Simple, si es > 1 es Compuesta.
    """
    if puntos not in GAUSS_DATA:
        raise ValueError("Puntos soportados: 2, 3, 4 o 5.")
        
    x = sp.symbols('x')
    f = sp.lambdify(x, sp.sympify(expr_str), 'numpy')
    
    nodos, pesos = GAUSS_DATA[puntos]
    h = (b - a) / n_subintervalos
    integral_total = 0.0
    
    # Iterar sobre cada subintervalo (Compuesto)
    for i in range(n_subintervalos):
        sub_a = a + i * h
        sub_b = sub_a + h
        
        # Cambio de variable de [-1, 1] a [sub_a, sub_b]
        suma_sub = 0.0
        for nodo, peso in zip(nodos, pesos):
            punto_transformado = 0.5 * ((sub_b - sub_a) * nodo + (sub_b + sub_a))
            suma_sub += peso * f(punto_transformado)
            
        integral_total += 0.5 * (sub_b - sub_a) * suma_sub
        
    return integral_total