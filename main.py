from flask import Flask, render_template, request
import time
import base64

app = Flask(__name__)

def procesar_foto_base64(data_url):
    """Decodifica el base64 y guarda la imagen en disco."""
    if data_url:
        header, encoded = data_url.split(",", 1)
        data = base64.b64decode(encoded)
        nombre_archivo = f"foto_{int(time.time())}.jpg"
        with open(nombre_archivo, "wb") as f:
            f.write(data)
        return f"¡Foto guardada como {nombre_archivo}!"
    return "No se recibió imagen."

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/accion', methods=['POST'])
def accion():
    data_url = request.form.get('imagen')
    return procesar_foto_base64(data_url)

if __name__ == '__main__':
    app.run()