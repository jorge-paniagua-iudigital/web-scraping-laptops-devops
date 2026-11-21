# Monitor de Precios de Portátiles — Pipeline DevOps & Despliegue Continuo (CI/CD)

## 1. Introducción
Este proyecto integra técnicas de extracción automatizada de datos (*Web Scraping*) con prácticas modernas de ingeniería de software bajo la cultura **DevOps**. Dando continuidad a las fases previas de análisis comparativo de scrapers (Evidencia 1) y control de versiones con integración continua (Evidencia 2), esta solución encapsula el motor de extracción en una **aplicación web desarrollada con Flask**, respaldada por pruebas unitarias automatizadas (`pytest`), un flujo de **CI/CD en GitHub Actions** y despliegue continuo en la nube.

El sistema consulta el catálogo de computadores portátiles de [WebScraper E-Commerce](https://webscraper.io/test-sites/e-commerce/static/computers/laptops), estructura los atributos principales (modelo, precio, especificaciones técnicas y enlace) y los expone tanto en una interfaz web HTML como en una API REST JSON.

---

## 2. Estructura del Proyecto

```text
web-scraping-laptops-devops/
├── .github/
│   └── workflows/
│       └── ci-cd.yml          # Flujo automatizado de CI/CD en GitHub Actions
├── src/
│   ├── __init__.py            # Inicializador del paquete Python
│   └── scraper.py             # Lógica de extracción con BeautifulSoup y variables de entorno
├── tests/
│   ├── test_app.py            # Pruebas unitarias de los endpoints de la aplicación web Flask
│   └── test_scraper.py        # Pruebas unitarias de extracción y esquema de datos
├── app.py                     # Aplicación web y API REST (Flask + Gunicorn)
├── requirements.txt           # Dependencias del proyecto
├── .gitignore                 # Exclusiones del control de versiones
└── README.md                  # Documentación técnica del proyecto


---

## 3. Instalación

### Requisitos Previos
* Python 3.11 o superior
* Git

### Pasos de Instalación Local
1. Clonar el repositorio:
   ```bash
   git clone https://github.com/jorge-paniagua-iudigital/web-scraping-laptops-devops.git
   cd web-scraping-laptops-devops
   ```
2. Crear y activar un entorno virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```
3. Instalar las dependencias requeridas:
   ```bash
   pip install -r requirements.txt
   ```

---

## 4. Uso y Variables de Entorno

### Variables de Entorno Configurables
La aplicación lee las siguientes variables del sistema operativo (con valores por defecto seguros para ejecución local):

| Variable | Descripción | Valor por Defecto |
| :--- | :--- | :--- |
| `TARGET_URL` | URL del catálogo de portátiles a extraer | `https://webscraper.io/test-sites/e-commerce/static/computers/laptops` |
| `APP_ENV` | Entorno de ejecución (`development` / `production`) | `production` |
| `PORT` | Puerto HTTP en el que escucha el servidor web | `5000` |

### Ejecución Local
* **Iniciar el servidor web:**
  ```bash
  python app.py
  ```
* **Ejecutar la suite de pruebas automatizadas:**
  ```bash
  PYTHONPATH=. pytest tests/
  ```

### Endpoints Disponibles
* `GET /`: Interfaz visual web en HTML con la tabla actualizada de portátiles.
* `GET /api/laptops`: Servicio REST que retorna los datos extraídos en formato JSON.
* `GET /health`: Endpoint de monitoreo (*health check*) para verificar el estado del servicio en la nube.

---

## 5. Automatización (CI/CD con GitHub Actions)

El flujo de trabajo definido en `.github/workflows/ci-cd.yml` automatiza el ciclo de vida del software ante cada `push` o `pull_request` hacia la rama `main`:

1. **Integración Continua (CI):**
   * Configura un entorno limpio en `ubuntu-latest` con Python 3.11.
   * Instala las dependencias especificadas en `requirements.txt`.
   * Ejecuta todas las pruebas unitarias (`pytest tests/`) validando tanto el scraper como los endpoints de Flask. Si alguna prueba falla, el flujo se detiene bloqueando el despliegue.
2. **Generación de Artefactos:**
   * Ejecuta `src/scraper.py` y publica el archivo resultante `laptops_extracted.csv` como un artefacto descargable en GitHub Actions.
3. **Entrega/Despliegue Continuo (CD):**
   * Si las pruebas son exitosas en la rama `main`, dispara un *Deploy Hook* hacia el servidor en la nube para actualizar la aplicación en producción automáticamente.

---

## 6. Despliegue en la Nube

La aplicación está diseñada para ejecutarse en plataformas PaaS (como **Render**) utilizando el servidor WSGI de producción **Gunicorn**:

* **Comando de construcción (*Build Command*):** `pip install -r requirements.txt`
* **Comando de inicio (*Start Command*):** `gunicorn app:app`
* **URL de Producción:** *(Se actualizará con el enlace activo tras completar el despliegue)*
