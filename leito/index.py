import sympy as sp

# ==========================================
# 1. IMPORTACIÓN / DEFINICIÓN DE LOS MÉTODOS
# ==========================================

def trapecio_compuesto(expr_str, a, b, n):
    x = sp.symbols('x')
    f = sp.lambdify(x, sp.sympify(expr_str), 'numpy')
    h = (b - a) / n
    suma = f(a) + f(b)
    for i in range(1, n):
        suma += 2 * f(a + i * h)
    return (h / 2) * suma

def simpson_13_compuesto(expr_str, a, b, n):
    if n % 2 != 0: raise ValueError("n debe ser par.")
    x = sp.symbols('x')
    f = sp.lambdify(x, sp.sympify(expr_str), 'numpy')
    h = (b - a) / n
    suma = f(a) + f(b)
    for i in range(1, n):
        suma += (2 if i % 2 == 0 else 4) * f(a + i * h)
    return (h / 3) * suma

def simpson_38_compuesto(expr_str, a, b, n):
    if n % 3 != 0: raise ValueError("n debe ser múltiplo de 3.")
    x = sp.symbols('x')
    f = sp.lambdify(x, sp.sympify(expr_str), 'numpy')
    h = (b - a) / n
    suma = f(a) + f(b)
    for i in range(1, n):
        suma += (2 if i % 3 == 0 else 3) * f(a + i * h)
    return (3 * h / 8) * suma

GAUSS_DATA = {
    2: ([-0.5773502691896257, 0.5773502691896257], [1.0, 1.0]),
    3: ([-0.7745966692414834, 0.0, 0.7745966692414834], [0.5555555555555556, 0.8888888888888888, 0.5555555555555556]),
    4: ([-0.8611363115940526, -0.3399810435848563, 0.3399810435848563, 0.8611363115940526], [0.3478548451374538, 0.6521451548625461, 0.6521451548625461, 0.3478548451374538]),
    5: ([-0.9061798459386640, -0.5384693101056831, 0.0, 0.5384693101056831, 0.9061798459386640], [0.2369268850561891, 0.4786286704993665, 0.5688888888888889, 0.4786286704993665, 0.2369268850561891])
}

def cuadratura_gaussiana(expr_str, a, b, puntos=3, n_subintervalos=1):
    if puntos not in GAUSS_DATA: raise ValueError("Puntos soportados: 2, 3, 4 o 5.")
    x = sp.symbols('x')
    f = sp.lambdify(x, sp.sympify(expr_str), 'numpy')
    nodos, pesos = GAUSS_DATA[puntos]
    h = (b - a) / n_subintervalos
    integral_total = 0.0
    for i in range(n_subintervalos):
        sub_a = a + i * h
        sub_b = sub_a + h
        suma_sub = 0.0
        for nodo, peso in zip(nodos, pesos):
            punto_transformado = 0.5 * ((sub_b - sub_a) * nodo + (sub_b + sub_a))
            suma_sub += peso * f(punto_transformado)
        integral_total += 0.5 * (sub_b - sub_a) * suma_sub
    return integral_total

def integral_doble_numerica(expr_str, a, b, c, d, nx, ny, metodo="trapecio"):
    x, y = sp.symbols('x y')
    f = sp.lambdify((x, y), sp.sympify(expr_str), 'numpy')
    hx, hy = (b - a) / nx, (d - c) / ny
    puntos_x = [a + i * hx for i in range(nx + 1)]
    puntos_y = [c + j * hy for j in range(ny + 1)]
    def obtener_pesos(n, m_tipo):
        if m_tipo == "trapecio": return [1 if (i == 0 or i == n) else 2 for i in range(n + 1)]
        if m_tipo == "simpson13":
            if n % 2 != 0: raise ValueError("Subintervalos deben ser pares.")
            return [1 if (i == 0 or i == n) else (4 if i % 2 != 0 else 2) for i in range(n + 1)]
    pesos_x, pesos_y = obtener_pesos(nx, metodo), obtener_pesos(ny, metodo)
    suma = 0.0
    for i in range(nx + 1):
        for j in range(ny + 1):
            suma += pesos_x[i] * pesos_y[j] * f(puntos_x[i], puntos_y[j])
    return (hx * hy / (4 if metodo == "trapecio" else 9)) * suma

def cuadratura_adaptativa(expr_str, a, b, tol=1e-6):
    x = sp.symbols('x')
    f = sp.lambdify(x, sp.sympify(expr_str), 'numpy')
    def simpson_eval(fa, fb, fc, sub_a, sub_b): return (abs(sub_b - sub_a) / 6) * (fa + 4 * fc + fb)
    def paso_adaptativo(sub_a, sub_b, tol_actual, fa, fb, fc):
        c = (sub_a + sub_b) / 2
        d, e = (sub_a + c) / 2, (c + sub_b) / 2
        fd, fe = f(d), f(e)
        s1 = simpson_eval(fa, fb, fc, sub_a, sub_b)
        s2 = simpson_eval(fa, fc, fd, sub_a, c) + simpson_eval(fc, fb, fe, c, sub_b)
        if abs(s2 - s1) <= 15 * tol_actual: return s2 + (s2 - s1) / 15
        else: return (paso_adaptativo(sub_a, c, tol_actual / 2, fa, fc, fd) + 
                    paso_adaptativo(c, sub_b, tol_actual / 2, fc, fb, fe))
    fa, fb = f(a), f(b)
    return paso_adaptativo(a, b, tol, fa, fb, f((a + b) / 2))

# ==========================================
# 2. INTERFAZ DE USUARIO (INDEX / MENÚ)
# ==========================================

def menu():
    while True:
        print("\n" + "="*50)
        print("    SISTEMA DE INTEGRACIÓN NUMÉRICA (MÉTODOS)")
        print("="*50)
        print("1. Trapecio Compuesto")
        print("2. Simpson 1/3 Compuesto")
        print("3. Simpson 3/8 Compuesto")
        print("4. Cuadratura Gaussiana (Simple o Compuesta)")
        print("5. Integrales Dobles (Trapecio / Simpson 1/3)")
        print("6. Cuadratura Adaptativa")
        print("7. Salir")
        print("="*50)
        
        opcion = input("Selecciona una opción (1-7): ")
        if opcion == "7":
            print("\n¡Nos vemos, éxito en la materia!")
            break
            
        if opcion not in ["1", "2", "3", "4", "5", "6"]:
            print("Opción no válida. Intenta de nuevo.")
            continue

        try:
            # Captura de datos comunes para integrales simples
            if opcion in ["1", "2", "3", "4", "6"]:
                expr = input("Introduce la función f(x) (ej. x**2, sin(x), exp(x)): ")
                a = float(input("Límite inferior (a): "))
                b = float(input("Límite superior (b): "))

            if opcion == "1":
                n = int(input("Número de subintervalos (n): "))
                res = trapecio_compuesto(expr, a, b, n)
                print(f"\n✨ Resultado (Trapecio Compuesto): {res}")
                
            elif opcion == "2":
                n = int(input("Número de subintervalos (n - debe ser PAR): "))
                res = simpson_13_compuesto(expr, a, b, n)
                print(f"\n✨ Resultado (Simpson 1/3): {res}")
                
            elif opcion == "3":
                n = int(input("Número de subintervalos (n - múltiplo de 3): "))
                res = simpson_38_compuesto(expr, a, b, n)
                print(f"\n✨ Resultado (Simpson 3/8): {res}")
                
            elif opcion == "4":
                pts = int(input("Puntos de Gauss (2, 3, 4 o 5): "))
                sub = int(input("Subintervalos (Escribe 1 para método SIMPLE, o >1 para COMPUESTO): "))
                res = cuadratura_gaussiana(expr, a, b, pts, sub)
                print(f"\n✨ Resultado (Gauss-Legendre): {res}")
                
            elif opcion == "5":
                expr = input("Introduce f(x, y) (ej. x*y, x**2 + y**2): ")
                a = float(input("Límite inferior de X (a): "))
                b = float(input("Límite superior de X (b): "))
                c = float(input("Límite inferior de Y (c): "))
                d = float(input("Límite superior de Y (d): "))
                nx = int(input("Subintervalos en X: "))
                ny = int(input("Subintervalos en Y: "))
                m_tipo = input("Método ('trapecio' o 'simpson13'): ").strip().lower()
                res = integral_doble_numerica(expr, a, b, c, d, nx, ny, m_tipo)
                print(f"\n✨ Resultado (Integral Doble): {res}")
                
            elif opcion == "6":
                tol_str = input("Tolerancia (Presiona Enter para usar 1e-6 por defecto): ")
                tol = float(tol_str) if tol_str.strip() != "" else 1e-6
                res = cuadratura_adaptativa(expr, a, b, tol)
                print(f"\n✨ Resultado (Cuadratura Adaptativa): {res}")

        except Exception as e:
            print(f"\n❌ Error en los datos o cálculo: {e}")

if __name__ == "__main__":
    menu()