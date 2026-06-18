# Proyecto Semestral - Métodos Numéricos

## Requisitos Previos

Antes de ejecutar el proyecto, asegúrate de tener instalado:

* Python 3.11 o superior

Verificar instalación:

```bash
py --version
```

o

```bash
python --version
```

---

## Clonar el Proyecto

```bash
git clone <URL_DEL_REPOSITORIO>
cd Metodos
```

---

## Crear Entorno Virtual

### Windows

```bash
py -m venv venv
```

### Linux / macOS

```bash
python3 -m venv venv
```

---

## Activar Entorno Virtual

### Windows (CMD)

```bash
venv\Scripts\activate.bat
```

### Windows (PowerShell)

```powershell
.\venv\Scripts\Activate.ps1
```

Si PowerShell bloquea la ejecución:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

y volver a ejecutar:

```powershell
.\venv\Scripts\Activate.ps1
```

### Linux / macOS

```bash
source venv/bin/activate
```

---

## Instalar Dependencias

```bash
pip install -r requirements.txt
```

---

## Ejecutar la Aplicación

```bash
python app.py
```

El servidor iniciará en:

```text
http://127.0.0.1:5000
```

Abrir la dirección anterior en cualquier navegador web.

---

## Estructura del Proyecto

```text
Metodos/
│
├── app.py
├── requirements.txt
│
├── templates/
│   └── index.html
│
├── static/
│   ├── css/
│   └── js/
│
└── venv/
```

---

## Actualizar Dependencias

Si se instala una nueva librería:

```bash
pip freeze > requirements.txt
```

Posteriormente los demás integrantes podrán instalar todas las dependencias mediante:

```bash
pip install -r requirements.txt
```

---

## Tecnologías Utilizadas

* Python
* Flask
* HTML5
* CSS3
* JavaScript

---

## Integrantes

* Aguilar Torres Luis
* Gonzales Baldpomero Leonardo
* Marin Rangel Santiago Andres

---

## Descripción General

Aplicación web desarrollada para la asignatura de Métodos Numéricos. El sistema permite implementar y analizar diferentes algoritmos numéricos mediante una interfaz web interactiva, facilitando la visualización de resultados, iteraciones y convergencia de los métodos estudiados durante el curso.
