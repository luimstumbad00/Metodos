import sympy as sp

def cuadratura_adaptativa(expr_str, a, b, tol=1e-6):
    """
    Método de Cuadratura Adaptativa basado en Simpson 1/3.
    """
    x = sp.symbols('x')
    f = sp.lambdify(x, sp.sympify(expr_str), 'numpy')
    
    def simpson_eval(fa, fb, fc, sub_a, sub_b):
        # f(a), f(b) y f(punto_medio) evaluados previamente
        return (abs(sub_b - sub_a) / 6) * (fa + 4 * fc + fb)
        
    def paso_adaptativo(sub_a, sub_b, tol_actual, fa, fb, fc):
        c = (sub_a + sub_b) / 2
        d = (sub_a + c) / 2
        e = (c + sub_b) / 2
        
        fd = f(d)
        fe = f(e)
        
        s1 = simpson_eval(fa, fb, fc, sub_a, sub_b)
        s2 = simpson_eval(fa, fc, fd, sub_a, c) + simpson_eval(fc, fb, fe, c, sub_b)
        
        # Comprobar el criterio de parada (tolerancia)
        if abs(s2 - s1) <= 15 * tol_actual:
            return s2 + (s2 - s1) / 15
        else:
            # Si no se cumple, dividir el intervalo a la mitad de forma recursiva
            return (paso_adaptativo(sub_a, c, tol_actual / 2, fa, fc, fd) + 
                    paso_adaptativo(c, sub_b, tol_actual / 2, fc, fb, fe))

    fa, fb = f(a), f(b)
    c = (a + b) / 2
    fc = f(c)
    
    return paso_adaptativo(a, b, tol, fa, fb, fc)