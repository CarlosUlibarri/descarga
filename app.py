from flask import Flask, render_template, request
from pytube import YouTube
import os

app = Flask(__name__)

# Ruta para la página principal
@app.route('/')
def index():
    return render_template('index.html')

# Ruta para manejar la descarga del video
@app.route('/download', methods=['POST'])
def download():
    try:
        url = request.form['url']
        filename = request.form['filename']
        quality = request.form['quality']

        # Obtener el objeto YouTube
        video = YouTube(url)

        # Obtener el stream de acuerdo a la calidad seleccionada
        if quality == 'high':
            stream = video.streams.filter(res='1080p').first()
        elif quality == '4k':
            # Intentar obtener la resolución 2160p (4K)
            stream = video.streams.filter(res='2160p').first()
            if not stream:
                return render_template('index.html', message='El video no está disponible en resolución 4K.')
        elif quality == 'medium':
            stream = video.streams.filter(res='720p').first()
        elif quality == 'low':
            stream = video.streams.filter(res='360p').first()
        else:
            return render_template('index.html', message='Calidad seleccionada no válida.')

        if stream:
            # Directorio de descargas del usuario
            user_download_dir = os.path.join(os.path.expanduser('~'), 'Downloads')

            # Descargar el video en el directorio de descargas del usuario
            stream.download(output_path=user_download_dir, filename=filename + '.mp4')

            return render_template('index.html', message=f'Video {filename} descargado correctamente en la carpeta de Descargas.')
        else:
            return render_template('index.html', message=f'No se encontró un stream para la calidad seleccionada.')

    except KeyError:
        return render_template('index.html', message='Falta algún campo en el formulario.')

    except Exception as e:
        return render_template('index.html', message=f'Error al descargar el video: {str(e)}')

if __name__ == '__main__':
    app.run(debug=True)
