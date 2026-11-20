# 🧪 Proyecto Final - Framework de Automatización de Pruebas

![CI Status](https://github.com/Federico-Delgado//proyecto-final-automation-testing-Federico-Delgado/actions/workflows/ci.yml/badge.svg)
![Python](https://img.shields.io/badge/Python-3.11-blue)
![Pytest](https://img.shields.io/badge/Pytest-9.2-0A93F6)
![Selenium](https://img.shields.io/badge/Selenium-4.15-green)

Framework de testing automatizado en Python que combina pruebas de **UI** (Selenium + Page Object Model) y **API** (Requests), con reportes HTML, logging centralizado y un pipeline de **CI/CD** en GitHub Actions.

**Autor:** Federico Delgado  
**Proyecto:** Talento Tech - Automation Testing  
**Entrega Final:** Trabajo Integrador

---

## 📌 Propósito del Proyecto

Demostrar la capacidad de construir un framework de automatización completo, escalable y mantenible, aplicando las mejores prácticas de la industria del QA:

- ✅ Separación de responsabilidades mediante **Page Object Model (POM)**
- ✅ Cobertura integral de **UI + API** en un solo framework
- ✅ **Data-Driven Testing** con archivos CSV y JSON externos
- ✅ **Reportes HTML autocontenidos** con screenshots en fallos
- ✅ **Logging centralizado** con rotación de archivos
- ✅ **Integración Continua** con GitHub Actions (ejecución automática en la nube)
- ✅ **Control de versiones profesional** con ramas y Pull Requests

---

## 🛠️ Tecnologías Utilizadas

| Categoría | Herramienta | Versión |
|-----------|-------------|---------|
| Lenguaje | Python | 3.11.9 |
| Framework de testing | Pytest | 9.2.0 |
| Automatización UI | Selenium WebDriver | 4.15+ |
| Automatización API | Requests | 2.31+ |
| Reportes HTML | pytest-html | 4.2.0 |
| Generación de datos | Faker | 40.54.0 |
| Soft-asserts | pytest-check | 3.1.0 |
| Retries | pytest-rerunfailures | 16.7 |
| CI/CD | GitHub Actions | - |
| Control de versiones | Git / GitHub | - |

---

## 📁 Estructura del Proyecto

```text
proyecto-final-automation-testing-Federico-Delgado/
├── .github/
│   └── workflows/
│       └── ci.yml              # Pipeline de CI/CD (GitHub Actions)
├── pages/                       # Page Object Model (POM)
│   ├── login_page.py           # Página de login de SauceDemo
│   ├── inventory_page.py       # Página de inventario/productos
│   ├── cart_page.py            # Página del carrito
│   └── checkout_page.py        # Página de checkout
├── tests/                       # Tests de UI (Selenium)
│   └── test_ui_saucedemo.py    # 9 casos de prueba UI
├── tests_api/                   # Tests de API (Requests)
│   ├── conftest.py             # Fixtures de URLs base
│   ├── test_get_users.py       # Tests GET con validación avanzada
│   ├── test_create_user.py     # Tests POST parametrizados
│   └── test_post_lifecycle.py  # Ciclo CRUD completo (encadenado)
├── datos/                       # Datos externos (Data-Driven)
│   ├── usuarios_login.csv      # Credenciales para parametrizar login
│   └── productos.json          # Productos para parametrizar carrito
├── utils/                       # Utilidades
│   ├── datos.py                # Lectores de CSV/JSON
│   └── logger.py               # Logger centralizado con rotación
├── reports/                     # Reportes HTML generados (gitignore)
├── logs/                        # Logs de ejecución (gitignore)
├── conftest.py                  # Fixture global del driver + hook de screenshots
├── pytest.ini                   # Configuración de Pytest
├── requirements.txt             # Dependencias del proyecto
├── .gitignore                   # Archivos ignorados por Git
└── README.md                    # Este archivo
```
---

## 🚀 Instalación

#### **1. Clonar el repositorio**

```bash
git clone https://github.com/TU_USUARIO/proyecto-final-automation-testing-Federico-Delgado.git
cd proyecto-final-automation-testing-Federico-Delgado
```

#### **2. Crear y activar el entorno virtual**

**Windows**:

```bash
python -m venv .venv
.venv\Scripts\activate
```

**macOS/Linux**:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

#### **3. Instalar dependencias**

```bash
pip install -r requirements.txt
```

#### **4. Verificar la instalación**

```bash
pytest --collect-only
```

Deberías ver los tests recolectados sin errores.

---

## 🧪 Ejecución de Pruebas

#### **Suite completa (UI + API)**

```bash
pytest
```

#### **Solo tests de UI**

```bash
pytest tests/ -v --html=reports/reporte_ui.html --self-contained-html
```

#### **Solo tests de API**

```bash
pytest tests_api/ -v --html=reports/reporte_api.html --self-contained-html
```

#### **Ejecución selectiva por markers**

```bash
pytest -m smoke        # Solo pruebas críticas
pytest -m ui           # Solo pruebas de interfaz
pytest -m api          # Solo pruebas de API
pytest -m e2e          # Solo flujos completos end-to-end
pytest -m "api and not ui"  # Combinaciones avanzadas
```

#### **Ejecutar un test específico**

```bash
pytest tests/test_ui_saucedemo.py::test_flujo_checkout_completo -v
```

#### **Con reintentos automáticos (útil en CI)**

```bash
pytest --reruns 2 --reruns-delay 3
```

---

## 📊 Interpretación de Reportes

#### **Reporte HTML (reports/reporte_final.html)**

Al abrir el archivo en el navegador, verás:

| Sección | Qué muestra |
|:---|:---| 
| Summary | Totales de tests: passed / failed / error / skipped |
| Environment | Versión de Python, OS, plugins cargados |
| Tests | Tabla con cada test, su estado (verde/rojo) y duración|
| Detalles de fallo | Traceback completo + screenshot embebido si la prueba UI falló|

#### **Logs (logs/suite.log)**

Archivo rotativo (máx. 5 MB, 3 backups) con formato:

2026-11-21 14:30:15 | INFO     | automation_framework | Iniciando login con usuario: standard_user
2026-11-21 14:30:16 | INFO     | automation_framework | Completando credenciales...
2026-11-21 14:30:18 | ERROR    | automation_framework | Botón 'Checkout' no encontrado

Cuándo revisar qué:
- 📄 Reporte HTML → "¿Qué pasó?" (vista general para stakeholders)
- 📋 Logs → "¿Qué ocurrió exactamente y en qué orden?" (debugging post-mortem)

---

## 🔄 CI/CD con GitHub Actions

El pipeline se ejecuta automáticamente en cada push o Pull Request hacia main/develop.

**Flujo de trabajo:**

1. Checkout del código
2. Setup de Python 3.11 con caché de pip
3. Instalación de Chrome en el runner
4. Ejecución de pytest tests/ tests_api/
5. Subida de artefactos (reporte HTML + logs)

**Dónde ver los resultados:**

- Pestaña Actions del repositorio
- Sección Artifacts en el resumen de cada run (disponibles 30 días)

**Modo Headless automático:**

El framework detecta automáticamente si está en CI (variable GITHUB_ACTIONS=true) y activa --headless=new en Chrome, sin necesidad de cambios manuales.

---

## 🌿 Estrategia de Control de Versiones

El proyecto se desarrolló en 6 fases, cada una en su propia rama con Pull Request:

| Fase | Rama | Descripción |
|:---|:---|:---|
| 1 | main | Configuración inicial, estructura, POM base
| 2 | feature/fase-2-automatizacion-ui | Tests UI, parametrización, screenshots |
| 3 | feature/fase-3-automatizacion-api | Tests API (GET, POST, PATCH, PUT, DELETE) |
| 4 | feature/fase-4-generación-reportes-logging | Logger centralizado, mejora de reportes |
| 5 | feature/fase-5-integración-continua | GitHub Actions, modo headless en CI |
| 6 | feature/fase-6-documentacion | README.md profesional |

Cada rama fue fusionada a main mediante un Pull Request con revisión previa, garantizando que main siempre contenga código estable y funcional.

---

## 📈 Cobertura de Pruebas

**UI (SauceDemo) — 9 ejecuciones**

- ✅ 4 casos de login parametrizados (CSV): válidos, bloqueados, inválidos
- ✅ 3 casos de carrito parametrizados (JSON): Backpack, Bike Light, Bolt T-Shirt
- ✅ 1 flujo E2E completo: login → carrito → checkout → confirmación
- ✅ 1 caso de logout con espera explícita

**API (JSONPlaceholder) — 10 ejecuciones**

- ✅ 3 casos GET (lista, específico, 404 negativo)
- ✅ 3 casos POST parametrizados con validación de 5 niveles
- ✅ 4 casos de ciclo de vida CRUD encadenado (POST → PATCH → PUT → DELETE)

Total: 19 ejecuciones automatizadas

---

## 🎯 Desafíos Técnicos Superados

Durante el desarrollo se resolvieron problemas reales que demuestran dominio avanzado:

1. StaleElementReferenceException en React → Resuelto usando execute_script() para extraer textos de forma atómica, evitando re-renderizados de DOM.
2. Race condition en logout → Resuelto con esperas explícitas (visibility_of_element_located) al botón de login de destino.
3. Compatibilidad con pytest-html 4.x → Migración de report.extra a report.extras (API cambió en la v4).
4. SessionNotCreatedException en Linux CI → Resuelto con detección automática de entorno CI y activación de --headless=new + --disable-gpu.
5. Limitaciones de JSONPlaceholder → Adaptación de tests para usar IDs existentes (≤100) en operaciones PUT/PATCH, ya que el mock devuelve 404 para IDs mayores.

---

## 📝 Comandos Útiles de Referencia


```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar todo
pytest

# Ejecutar solo smoke
pytest -m smoke -v

# Generar reporte HTML específico
pytest --html=reports/mi_reporte.html --self-contained-html

# Ver qué tests existen sin ejecutarlos
pytest --collect-only

# Ejecutar con reintentos
pytest --reruns 2 --reruns-delay 3
```

---

## 👤 Autor

**Federico Delgado**
**Automation Tester - Talento Tech**
[GitHub](https://github.com/Federico-Delgado)

---

##  📄 Licencia

Proyecto educativo desarrollado como Trabajo Final Integrador del curso de Automation Testing de Talento Tech.

---

