from flask import Flask, render_template_string, request
import time
import base64

app = Flask(__name__)

def render_pagina_principal():
    """Devuelve el HTML + JS que dispara la cámara y envía la foto al servidor."""
    html = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
      <meta charset="UTF-8">
      <title>Captura de Foto</title>
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <style>
        body { font-family: sans-serif; text-align: center; padding: 2em; }
        video, canvas { max-width: 100%; height: auto; }
        button {
          padding: 1em 2em;
          font-size: 1.2em;
          border-radius: 8px;
          border: none;
          background: #007BFF;
          color: white;
          margin-top: 1em;
        }
        button:active {
          background: #0056b3;
        }
      </style>
    </head>
    <body>
      <h1>Captura de Foto</h1>
      <video id="video" autoplay playsinline></video>
      <br>
      <button id="capture">Tomar foto</button>
      <form id="fotoForm" action="/accion" method="post">
        <input type="hidden" name="imagen" id="imagen">
        <br>
        <button type="submit">Enviar foto</button>
      </form>
      <canvas id="canvas" style="display:none;"></canvas>

      <script>
        const video = document.getElementById('video');
        const canvas = document.getElementById('canvas');
        const captureBtn = document.getElementById('capture');
        const imagenInput = document.getElementById('imagen');

        // Solicita la cámara
        navigator.mediaDevices.getUserMedia({ video: true })
          .then(stream => {
            video.srcObject = stream;
          })
          .catch(err => {
            alert("Error accediendo a la cámara: " + err);
          });

        captureBtn.addEventListener('click', () => {
          const context = canvas.getContext('2d');
          canvas.width = video.videoWidth;
          canvas.height = video.videoHeight;
          context.drawImage(video, 0, 0, canvas.width, canvas.height);
          const dataURL = canvas.toDataURL('image/jpeg');
          imagenInput.value = dataURL;
          alert("Foto capturada, ahora envíala.");
        });
      </script>
    </body>
    </html>
    """
    return html

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
    return render_template_string(render_pagina_principal())

@app.route('/accion', methods=['POST'])
def accion():
    data_url = request.form.get('imagen')
    return procesar_foto_base64(data_url)

if __name__ == '__main__':
    app.run()