from flask import Flask, render_template_string, request, jsonify
import sympy as sp

# IMPORTAMOS TUS MÉTODOS DESDE LA CARPETA LEITO
from leito.Trapecio_Compuesto import trapecio_compuesto
from leito.Simpson1_3_Compuesto import simpson_13_compuesto
from leito.Simpson3_8_Compuesto import simpson_38_compuesto
from leito.Cuadratura_Gaussiana import cuadratura_gaussiana
from leito.Integrales_Dobles import integral_doble_numerica
from leito.Cuadratura_Adaptativa import cuadratura_adaptativa

app = Flask(__name__)

# =======================================================
# INTERFAZ WEB COMPLETA CON TODOS LOS MÉTODOS Y CAMPOS
# =======================================================
HTML_INTERFACE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Integración Numérica - ESCOM</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #f4f7f6; margin: 30px; }
        .container { max-width: 650px; background: white; padding: 25px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); margin: auto; }
        h2 { text-align: center; color: #333; margin-bottom: 20px; }
        label { font-weight: bold; display: block; margin-top: 15px; color: #444; }
        input, select { width: 100%; padding: 10px; margin-top: 5px; box-sizing: border-box; border: 1px solid #ccc; border-radius: 6px; font-size: 16px; }
        
        /* Teclado Matemático */
        .keyboard { display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px; margin-top: 15px; background: #eaeaea; padding: 10px; border-radius: 8px; }
        .btn { padding: 12px; background: #fff; border: 1px solid #bbb; border-radius: 6px; cursor: pointer; font-weight: bold; font-size: 15px; text-align: center; user-select: none; }
        .btn:hover { background: #ddd; }
        .btn.op { background: #2196F3; color: white; border: none; }
        .btn.op:hover { background: #0b7dda; }
        .btn.clear { background: #f44336; color: white; border: none; }
        .btn.clear:hover { background: #da190b; }
        
        /* Contenedores dinámicos */
        .grid-3 { display: flex; gap: 10px; }
        .grid-3 > div { flex: 1; }
        .dinamico { display: none; margin-top: 10px; background: #f9f9f9; padding: 10px; border-radius: 6px; border: 1px dashed #bbb; }
        
        button.calcular { width: 100%; padding: 14px; background: #4CAF50; color: white; border: none; border-radius: 6px; margin-top: 20px; font-size: 18px; cursor: pointer; font-weight: bold; }
        button.calcular:hover { background: #45a049; }
        #resultado { margin-top: 25px; padding: 15px; background: #e7f3fe; border-left: 6px solid #2196F3; border-radius: 4px; font-size: 18px; font-weight: bold; display: none; color: #0c5460; word-break: break-all; }
    </style>
</head>
<body>

<div class="container">
    <h2>🧮 Integrador Numérico Completo</h2>
    
    <label>Selecciona el Método Numérico:</label>
    <select id="metodo" onchange="ajustarFormulario()">
        <option value="trapecio">Trapecio Compuesto</option>
        <option value="simpson13">Simpson 1/3 Compuesto</option>
        <option value="simpson38">Simpson 3/8 Compuesto</option>
        <option value="gauss">Cuadratura Gaussiana (Simple/Compuesta)</option>
        <option value="dobles">Integrales Dobles (Malla Rectangular)</option>
        <option value="adaptativa">Cuadratura Adaptativa</option>
    </select>

    <label id="label_expr">Función f(x):</label>
    <input type="text" id="expr" placeholder="Ingresa la función..." readonly>

    <div class="keyboard">
        <div class="btn" onclick="add('x')">x</div>
        <div class="btn" onclick="add('y')" id="btn_y" style="display:none; background:#fff3cd;">y</div>
        <div class="btn" onclick="add('sin(')">sin</div>
        <div class="btn" onclick="add('cos(')">cos</div>
        <div class="btn clear" onclick="clearExpr()">C</div>
        
        <div class="btn" onclick="add('+')">+</div>
        <div class="btn" onclick="add('-')">−</div>
        <div class="btn" onclick="add('*')">×</div>
        <div class="btn" onclick="add('/')">÷</div>
        
        <div class="btn" onclick="add('**2')">x²</div>
        <div class="btn" onclick="add('**')">xʸ</div>
        <div class="btn" onclick="add('exp(')">eˣ</div>
        <div class="btn" onclick="add('log(')">ln</div>
        
        <div class="btn" onclick="add('(')">(</div>
        <div class="btn" onclick="add(')')">)</div>
        <div class="btn" onclick="add('pi')">π</div>
        <div class="btn op" onclick="backspace()">⌫</div>
    </div>

    <div class="grid-3" id="limites_estandar">
        <div>
            <label id="label_a">Límite inferior (a):</label>
            <input type="number" id="lim_a" value="0" step="any">
        </div>
        <div>
            <label id="label_b">Límite superior (b):</label>
            <input type="number" id="lim_b" value="1" step="any">
        </div>
        <div id="box_n">
            <label>Subintervalos (n):</label>
            <input type="number" id="n_val" value="10">
        </div>
    </div>

    <div id="campos_gauss" class="dinamico">
        <div class="grid-3">
            <div>
                <label>Puntos de Gauss:</label>
                <select id="gauss_puntos">
                    <option value="2">2 Puntos</option>
                    <option value="3" selected>3 Puntos</option>
                    <option value="4">4 Puntos</option>
                    <option value="5">5 Puntos</option>
                </select>
            </div>
            <div>
                <label>Subintervalos (Compuesto):</label>
                <input type="number" id="gauss_sub" value="1" min="1">
            </div>
        </div>
    </div>

    <div id="campos_dobles" class="dinamico">
        <div class="grid-3">
            <div>
                <label>Límite inf Y (c):</label>
                <input type="number" id="lim_c" value="0" step="any">
            </div>
            <div>
                <label>Límite sup Y (d):</label>
                <input type="number" id="lim_d" value="1" step="any">
            </div>
            <div>
                <label>Subintervalos Y (ny):</label>
                <input type="number" id="ny_val" value="10">
            </div>
        </div>
        <label style="margin-top:10px;">Algoritmo Base de la Malla:</label>
        <select id="doble_metodo_base">
            <option value="trapecio">Trapecio</option>
            <option value="simpson13">Simpson 1/3</option>
        </select>
    </div>

    <div id="campos_adaptativa" class="dinamico">
        <label>Tolerancia de error (TOL):</label>
        <input type="number" id="tol_val" value="0.000001" step="any">
    </div>

    <button class="calcular" onclick="enviarDatos()">Calcular Integral</button>

    <div id="resultado"></div>
</div>

<script>
    const exprInput = document.getElementById('expr');

    function add(val) { exprInput.value += val; }
    function clearExpr() { exprInput.value = ''; }
    function backspace() { exprInput.value = exprInput.value.slice(0, -1); }

    // Función mágica para ocultar/mostrar inputs según el método seleccionado
    function ajustarFormulario() {
        const metodo = document.getElementById('metodo').value;
        
        // Ocultar todas las secciones extra por defecto
        document.querySelectorAll('.dinamico').forEach(el => el.style.display = 'none');
        document.getElementById('box_n').style.display = 'block';
        document.getElementById('btn_y').style.display = 'none';
        document.getElementById('label_expr').innerText = "Función f(x):";
        document.getElementById('label_a').innerText = "Límite inferior (a):";
        document.getElementById('label_b').innerText = "Límite superior (b):";

        if (metodo === 'gauss') {
            document.getElementById('box_n').style.display = 'none';
            document.getElementById('campos_gauss').style.display = 'block';
        } else if (metodo === 'dobles') {
            document.getElementById('btn_y').style.display = 'block';
            document.getElementById('campos_dobles').style.display = 'block';
            document.getElementById('label_expr').innerText = "Función f(x, y):";
            document.getElementById('label_a').innerText = "Límite inf X (a):";
            document.getElementById('label_b').innerText = "Límite sup X (b):";
        } else if (metodo === 'adaptativa') {
            document.getElementById('box_n').style.display = 'none';
            document.getElementById('campos_adaptativa').style.display = 'block';
        }
    }

    function enviarDatos() {
        const metodo = document.getElementById('metodo').value;
        const datos = {
            metodo: metodo,
            expr: exprInput.value,
            a: parseFloat(document.getElementById('lim_a').value),
            b: parseFloat(document.getElementById('lim_b').value),
            n: parseInt(document.getElementById('n_val').value)
        };

        // Agregar parámetros específicos según el caso
        if (metodo === 'gauss') {
            datos.puntos = parseInt(document.getElementById('gauss_puntos').value);
            datos.subintervalos = parseInt(document.getElementById('gauss_sub').value);
        } else if (metodo === 'dobles') {
            datos.c = parseFloat(document.getElementById('lim_c').value);
            datos.d = parseFloat(document.getElementById('lim_d').value);
            datos.ny = parseInt(document.getElementById('ny_val').value);
            datos.metodo_base = document.getElementById('doble_metodo_base').value;
        } else if (metodo === 'adaptativa') {
            datos.tol = parseFloat(document.getElementById('tol_val').value);
        }

        fetch('/calcular', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(datos)
        })
        .then(res => res.json())
        .then(res => {
            const resDiv = document.getElementById('resultado');
            resDiv.style.display = 'block';
            if(res.status === 'ok') {
                resDiv.style.background = '#e7f3fe';
                resDiv.style.borderLeftColor = '#2196F3';
                resDiv.innerHTML = `✨ Resultado: ${res.resultado}`;
            } else {
                resDiv.style.background = '#f8d7da';
                resDiv.style.borderLeftColor = '#f44336';
                resDiv.innerHTML = `❌ Error: ${res.message}`;
            }
        });
    }
</script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_INTERFACE)

@app.route('/calcular', methods=['POST'])
def calcular():
    data = request.json
    try:
        metodo = data['metodo']
        expr = data['expr']
        a = data['a']
        b = data['b']
        
        # Evaluar según el método seleccionado
        if metodo == 'trapecio':
            res = trapecio_compuesto(expr, a, b, data['n'])
            
        elif metodo == 'simpson13':
            res = simpson_13_compuesto(expr, a, b, data['n'])
            
        elif metodo == 'simpson38':
            res = simpson_38_compuesto(expr, a, b, data['n'])
            
        elif metodo == 'gauss':
            res = cuadratura_gaussiana(expr, a, b, data['puntos'], data['subintervalos'])
            
        elif metodo == 'dobles':
            # Nota: En dobles, data['n'] actúa como nx
            res = integral_doble_numerica(expr, a, b, data['c'], data['d'], data['n'], data['ny'], data['metodo_base'])
            
        elif metodo == 'adaptativa':
            res = cuadratura_adaptativa(expr, a, b, data['tol'])
            
        else:
            return jsonify({'status': 'error', 'message': 'Método no soportado.'})
            
        return jsonify({'status': 'ok', 'resultado': float(res)})
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

if __name__ == '__main__':
    app.run(debug=True)