from flask import Flask, render_template, request, redirect, send_from_directory, url_for
from video.stream import video_bp
import os
import config

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = config.UPLOAD_FOLDER

#app.register_blueprint(video_bp)

UPLOAD_BASE = "uploads"

@app.route('/')
def index():
    print(">>> Entraste a index.html desde:", os.path.abspath("templates/index.html"))
    return render_template('index.html')

@app.route('/semestre')
def seleccionar_semestre():
    carrera = request.args.get("carrera")
    if not carrera:
        return redirect(url_for("index"))
    return render_template("semestre.html", carrera=carrera)

@app.route("/materia")
def seleccionar_materia():
    carrera = request.args.get("carrera")
    semestre = request.args.get("semestre")

    if not carrera or not semestre:
        return redirect(url_for("index"))

    materias_por_carrera = {
        "computacion": ["Redes", "Estructuras de Datos", "POO", "Sistemas Operativos"],
        "industrial": ["Logística", "Producción", "Calidad", "Ergonomía"],
        "derecho": ["Derecho Penal", "Derecho Civil", "Constitucional", "Procesal"],
        "administracion": ["Contabilidad", "Marketing", "Finanzas", "Recursos Humanos"]
    }

    materias = materias_por_carrera.get(carrera, [])
    return render_template("materia.html", carrera=carrera, semestre=semestre, materias=materias)

@app.route("/archivos")
def ver_archivos():
    carrera = request.args.get("carrera")
    semestre = request.args.get("semestre")
    materia = request.args.get("materia")
    ruta = os.path.join(UPLOAD_BASE, carrera, semestre, materia)
    os.makedirs(ruta, exist_ok=True)
    archivos = os.listdir(ruta)
    return render_template("archivos.html", carrera=carrera, semestre=semestre, materia=materia, archivos=archivos)

@app.route("/subir", methods=["POST"])
def subir_archivo():
    archivo = request.files["archivo"]
    carrera = request.form["carrera"]
    semestre = request.form["semestre"]
    materia = request.form["materia"]

    ruta = os.path.join(UPLOAD_BASE, carrera, semestre, materia)
    os.makedirs(ruta, exist_ok=True)
    archivo.save(os.path.join(ruta, archivo.filename))

    return redirect(url_for("ver_archivos", carrera=carrera, semestre=semestre, materia=materia))

@app.route("/descargar/<archivo>")
def descargar_archivo(archivo):
    carrera = request.args.get("carrera")
    semestre = request.args.get("semestre")
    materia = request.args.get("materia")
    ruta = os.path.join(UPLOAD_BASE, carrera, semestre, materia)
    return send_from_directory(ruta, archivo, as_attachment=True)

if __name__ == '__main__':
    print(">>> Starting WebCraft...")
    print(">>> Flask está usando templates desde:", app.template_folder)
    app.run(host='0.0.0.0', port=5050)