import os
from datetime import datetime
from flask import Flask, jsonify, render_template_string
from src.scraper import extract_laptops

app = Flask(__name__)

# Configuración mediante variables de entorno del servidor
APP_ENV = os.getenv("APP_ENV", "production")
PORT = int(os.getenv("PORT", 5000))

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Monitor de Precios - Laptops E-Commerce</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #f4f6f9; margin: 0; padding: 20px; color: #333; }
        .container { max-width: 1000px; margin: auto; background: #fff; padding: 25px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
        h1 { color: #1a73e8; margin-bottom: 5px; }
        .meta { font-size: 0.9em; color: #666; margin-bottom: 20px; }
        table { width: 100%; border-collapse: collapse; margin-top: 15px; }
        th, td { padding: 12px; border-bottom: 1px solid #ddd; text-align: left; }
        th { background-color: #1a73e8; color: white; }
        tr:hover { background-color: #f1f5fb; }
        .price { font-weight: bold; color: #188038; }
        a.btn { background: #1a73e8; color: #fff; padding: 6px 10px; text-decoration: none; border-radius: 4px; font-size: 0.85em; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Catálogo Automatizado de Portátiles (CI/CD)</h1>
        <div class="meta">
            Entorno: <strong>{{ env }}</strong> | Última consulta: <strong>{{ timestamp }}</strong> | Total extraídos: <strong>{{ productos|length }}</strong>
        </div>
        <table>
            <thead>
                <tr>
                    <th>Modelo</th>
                    <th>Precio</th>
                    <th>Especificaciones</th>
                    <th>Detalle</th>
                </tr>
            </thead>
            <tbody>
                {% for item in productos %}
                <tr>
                    <td><strong>{{ item.Titulo }}</strong></td>
                    <td class="price">{{ item.Precio }}</td>
                    <td>{{ item.Descripcion }}</td>
                    <td><a class="btn" href="{{ item.Enlace }}" target="_blank">Ver producto</a></td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
</body>
</html>
"""

@app.route("/")
def index():
    productos = extract_laptops()
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    return render_template_string(HTML_TEMPLATE, productos=productos, env=APP_ENV, timestamp=timestamp)

@app.route("/api/laptops")
def api_laptops():
    productos = extract_laptops()
    return jsonify({"status": "ok", "total": len(productos), "data": productos})

@app.route("/health")
def health():
    return jsonify({"status": "healthy", "environment": APP_ENV}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
