from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__) 
USUARIOS_REGISTRADOS = {
    'daniel@correo.com':{
        'password': 'daniel',
        'nombre': 'daniel',
        }
}
app.config['SECRET_KEY'] = 'la_primera_es_la_primera'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/registro')
def registro():
    return render_template('registro.html')

@app.route('/educacion')
def educacion():
    return render_template('educacion.html')

@app.route('/registrar', methods=['GET', 'POST'])
def registrar():
    if request.method == 'POST':
        error = None
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        dia = request.form['dia']
        mes = request.form['mes']
        year = request.form['year']
        genero = request.form['genero']
        peso = request.form['peso']
        altura = request.form['altura']
        objetivo = request.form['objetivo']
        nivel_actividad = request.form['nivel_actividad']
        nivel_experiencia = request.form['nivel_experiencia']
        correo = request.form['correo']
        password = request.form['password']
        confirmPassword = request.form.get("confirmPassword")
        if password != confirmPassword:
            error = "Las contraseñas no coinciden"
        elif correo in USUARIOS_REGISTRADOS:
            error = "Este correo ya está registrado"
        
        if error is not None:
            flash(error, 'error')
            return render_template('registro.html')
        else:

            USUARIOS_REGISTRADOS[correo] = {
                'password': password,
                'nombre': f"{nombre} {apellido}",
            }
            flash(f"Registro exitoso: {nombre}. Ahora puedes iniciar sesión.", 'success')
            return redirect(url_for('iniciar'))
        
@app.route("/iniciar")
def iniciar():
    if session.get('logueado'):
        return render_template('index.html')
    return render_template('iniciar.html')

@app.route('/validaLogin', methods=['GET','POST'])
def validar():
    if request.method == "POST":
        correo = request.form.get("correo", '').strip()
        password = request.form.get("password", '')
        if not correo or not password:
            flash('Por favor ingresa email y contraseña', 'error')
            return render_template('iniciar.html')
        
        elif correo in USUARIOS_REGISTRADOS:
            usuario = USUARIOS_REGISTRADOS[correo]
            if usuario['password'] == password:
                session['logueado'] = True
                session['usuario'] = usuario['nombre']
                session['usuario_correo'] = correo
                flash(f'¡Bienvenido {usuario["nombre"]}!', 'success')
                return redirect(url_for('index'))
            else:
                flash('Contraseña incorrecta', 'error')
        else:
            flash('Usuario no encontrado', 'error')
        
        return render_template('iniciar.html')
    
    return redirect(url_for('iniciar'))

@app.route("/logout")
def logout():
    session.clear()
    flash('Has cerrado sesión correctamente', 'info')
    return redirect(url_for('index'))

@app.route('/herramientas')
def herramientas():
    return render_template('herramientas.html')


if __name__ == '__main__':
    app.run(debug=True)

