from flask import Flask, render_template, request, redirect, send_from_directory, url_for, session
import os
import config
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = config.UPLOAD_FOLDER
UPLOAD_BASE = "uploads"
app.secret_key = "clave_super_secreta"  # cámbiala en producción

# --- FUNCIÓN PARA ENVIAR CORREO ---
def enviar_correo(destinatario):
    remitente = "juan.lupe.sacame@gmail.com"  # ✅ CAMBIA ESTO
    contraseña = "fimy fuee pbzq hqfu"         # ✅ CONTRASEÑA DE APLICACIÓN

    asunto = "Gracias por entrar a CETYSCatálogo"
    cuerpo = "Hola, gracias por visitar CETYSCatálogo. ¡Esperamos que te sea útil!"

    msg = MIMEMultipart()
    msg["From"] = remitente
    msg["To"] = destinatario
    msg["Subject"] = asunto
    msg.attach(MIMEText(cuerpo, "plain"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(remitente, contraseña)
        server.send_message(msg)
        server.quit()
        print("✅ Correo enviado a", destinatario)
    except Exception as e:
        print("❌ Error enviando correo:", e)

# --- RUTA DE REGISTRO ---
@app.route('/registro', methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        correo = request.form.get("correo")
        if correo:
            session["correo"] = correo
            enviar_correo(correo)
            return redirect(url_for("index"))
    return render_template("registro.html")

# --- RUTA PARA CERRAR SESIÓN ---
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("registro"))

# --- VISTA PRINCIPAL ---
@app.route('/')
def index():
 
    if "correo" not in session:
        return redirect(url_for("registro"))
    return render_template("index.html")

@app.route('/semestre')
def seleccionar_semestre():
    if "correo" not in session:
        return redirect(url_for("registro"))
    carrera = request.args.get("carrera")
    if not carrera:
        return redirect(url_for("index"))
    return render_template("semestre.html", carrera=carrera)

@app.route("/materia")
def seleccionar_materia():
    if "correo" not in session:
        return redirect(url_for("registro"))
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
    if "correo" not in session:
        return redirect(url_for("registro"))
    carrera = request.args.get("carrera")
    semestre = request.args.get("semestre")
    materia = request.args.get("materia")

    ruta = os.path.join(UPLOAD_BASE, carrera, semestre, materia)
    os.makedirs(ruta, exist_ok=True)
    archivos = os.listdir(ruta)
    return render_template("archivos.html", carrera=carrera, semestre=semestre, materia=materia, archivos=archivos)

@app.route("/subir", methods=["POST"])
def subir_archivo():
    if "correo" not in session:
        return redirect(url_for("registro"))
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
    if "correo" not in session:
        return redirect(url_for("registro"))
    carrera = request.args.get("carrera")
    semestre = request.args.get("semestre")
    materia = request.args.get("materia")

    ruta = os.path.join(UPLOAD_BASE, carrera, semestre, materia)
    return send_from_directory(ruta, archivo, as_attachment=True)

if __name__ == '__main__':
    print(">>> Starting WebCraft...")
    app.run(host='0.0.0.0', port=5050)
