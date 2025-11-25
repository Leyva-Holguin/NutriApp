from flask import Flask, render_template, request, redirect, url_for, flash, session
import requests

API_KEY = "1320e414b5414686ac59e14362f5a2d3"
API_BASE = "https://api.spoonacular.com"

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

@app.route('/modulo3')
def modulo3():
    return render_template('modulo3.html')

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
        intolerante = request.form['intolerante']
        nivel_actividad = request.form['nivel_actividad']
        nivel_experiencia = request.form['nivel_experiencia']
        correo = request.form['correo']
        password = request.form['password']
        confirmPassword = request.form.get("confirmPassword")
        edad = 2025 - int(year)
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
                'dia': dia,
                'mes': mes,
                'year': year,
                'genero': genero,
                'peso': peso,
                'altura': altura,
                'objetivo': objetivo,
                'nivel_actividad': nivel_actividad,
                'correo': correo,
                'edad': edad,
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
    datos_usuario = None
    if session.get('logueado'):
        usuario_correo = session.get('usuario_correo')
        if usuario_correo in USUARIOS_REGISTRADOS:
            datos_usuario = USUARIOS_REGISTRADOS[usuario_correo]
    return render_template('herramientas.html', datos_usuario=datos_usuario)

@app.route('/cal_imc', methods=['POST'])
def cal_imc():
    datos_usuario = None
    if session.get('logueado'):
        usuario_correo = session.get('usuario_correo')
        if usuario_correo in USUARIOS_REGISTRADOS:
            datos_usuario = USUARIOS_REGISTRADOS[usuario_correo]
    resultado = None
    try:
        peso = float(request.form.get('peso_imc'))
        altura = float(request.form.get('altura_imc')) / 100
        imc = peso / (altura ** 2)
        if imc < 18.5:
            clasificacion = "Bajo peso"
        elif imc < 25:
            clasificacion = "Peso normal"
        elif imc < 30:
            clasificacion = "Sobrepeso"
        else:
            clasificacion = "Obesidad"
        resultado = f'Tu IMC es: {imc:.1f} - {clasificacion}'
    except (ValueError, ZeroDivisionError):
        resultado = 'Por favor ingresa valores numéricos válidos'
    return render_template('herramientas.html', datos_usuario=datos_usuario, resultado_imc=resultado)

@app.route('/cal_tmb', methods=['POST'])
def cal_tmb():
    datos_usuario = None
    if session.get('logueado'):
        usuario_correo = session.get('usuario_correo')
        if usuario_correo in USUARIOS_REGISTRADOS:
            datos_usuario = USUARIOS_REGISTRADOS[usuario_correo]
    resultado = None
    try:
        edad = int(request.form.get('edad_tmb'))
        peso = float(request.form.get('peso_tmb'))
        altura = float(request.form.get('altura_tmb'))
        genero = request.form.get('genero_tmb')
        if genero == 'hombre':
            tmb = (10 * peso) + (6.25 * altura) - (5 * edad) + 5
        else:
            tmb = (10 * peso) + (6.25 * altura) - (5 * edad) - 161
        resultado = f'Tu Tasa Metabólica Basal es: {tmb:.0f} calorías/día'
    except ValueError:
        resultado = 'Por favor ingresa valores numéricos válidos'
    return render_template('herramientas.html', datos_usuario=datos_usuario, resultado_tmb=resultado)

@app.route('/cal_gct', methods=['POST'])
def cal_gct():
    datos_usuario = None
    if session.get('logueado'):
        usuario_correo = session.get('usuario_correo')
        if usuario_correo in USUARIOS_REGISTRADOS:
            datos_usuario = USUARIOS_REGISTRADOS[usuario_correo]
    resultado = None
    try:
        tmb = float(request.form.get('tmb_gct'))
        actividad = request.form.get('actividad_gct')
        factores = {
            'sedentario': 1.2,
            'ligero': 1.375,
            'moderado': 1.55,
            'activo': 1.725,
            'atleta': 1.9
        }
        gct = tmb * factores.get(actividad, 1.2)
        resultado = f'Tu Gasto Calórico Total es: {gct:.0f} calorías/día'
    except ValueError:
        resultado = 'Por favor ingresa valores numéricos válidos'
    return render_template('herramientas.html', datos_usuario=datos_usuario, resultado_gct=resultado)

@app.route('/cal_peso_ideal', methods=['POST'])
def cal_peso_ideal():
    datos_usuario = None
    if session.get('logueado'):
        usuario_correo = session.get('usuario_correo')
        if usuario_correo in USUARIOS_REGISTRADOS:
            datos_usuario = USUARIOS_REGISTRADOS[usuario_correo]
    resultado = None
    try:
        altura = float(request.form.get('altura_pci'))
        genero = request.form.get('genero_pci')
        complexion = request.form.get('complexion_pci')
        if genero == 'hombre':
            peso_base = 50 + 0.91 * (altura - 152.4)
        else:
            peso_base = 45.5 + 0.91 * (altura - 152.4)
        peso_min = peso_base * 0.9
        peso_max = peso_base * 1.1
        resultado = f'Tu peso ideal aproximado: {peso_base:.1f} kg<br> Rango saludable: {peso_min:.1f} - {peso_max:.1f} kg'
    except ValueError:
        resultado = 'Por favor ingresa valores numéricos válidos'
    return render_template('herramientas.html', datos_usuario=datos_usuario, resultado_peso_ideal=resultado)

@app.route('/cal_macronutrientes', methods=['POST'])
def cal_macronutrientes():
    datos_usuario = None
    if session.get('logueado'):
        usuario_correo = session.get('usuario_correo')
        if usuario_correo in USUARIOS_REGISTRADOS:
            datos_usuario = USUARIOS_REGISTRADOS[usuario_correo]
    resultado = None
    try:
        calorias = float(request.form.get('calorias_macro'))
        objetivo = request.form.get('objetivo_macro')
        actividad = request.form.get('actividad_macro')
        if objetivo == 'perder':
            proteina = (calorias * 0.4) / 4
            carbohidratos = (calorias * 0.3) / 4
            grasa = (calorias * 0.3) / 9
        elif objetivo == 'mantener':
            proteina = (calorias * 0.3) / 4
            carbohidratos = (calorias * 0.4) / 4
            grasa = (calorias * 0.3) / 9
        else:
            proteina = (calorias * 0.35) / 4
            carbohidratos = (calorias * 0.45) / 4
            grasa = (calorias * 0.2) / 9
        resultado = f'Macronutrientes diarios:<br>• Proteína: {proteina:.0f}g<br>• Carbohidratos: {carbohidratos:.0f}g<br>• Grasas: {grasa:.0f}g'
    except ValueError:
        resultado = 'Por favor ingresa valores numéricos válidos'
    
    return render_template('herramientas.html', datos_usuario=datos_usuario, resultado_macronutrientes=resultado)

@app.route('/analizar_receta', methods=['POST'])
def analizar_receta():
    datos_usuario = None
    if session.get('logueado'):
        usuario_correo = session.get('usuario_correo')
        if usuario_correo in USUARIOS_REGISTRADOS:
            datos_usuario = USUARIOS_REGISTRADOS[usuario_correo]
    resultado = None
    try:
        titulo = request.form.get('titulo_receta', '').strip()
        texto_receta = request.form.get('texto_receta', '').strip()
        
        if not titulo or not texto_receta:
            resultado = 'Por favor ingresa tanto el título como los ingredientes'
        else:
            url = f"{API_BASE}/recipes/complexSearch"
            params = {
                'apiKey': API_KEY,
                'query': titulo,  
                'number': 1,
                'addRecipeInformation': True,
                'addRecipeNutrition': True,
                'instructionsRequired': True,
                'fillIngredients': True
            }
            
            response = requests.get(url, params=params)
            
            if response.status_code == 200:
                data = response.json()
                recetas = data.get('results', [])
                
                if recetas:
                    receta = recetas[0]
                    nutricion = receta.get('nutrition', {})
                    nutrientes = nutricion.get('nutrients', [])
                    
                    calorias, proteinas, carbohidratos, grasas = {}, {}, {}, {}
                    
                    for nutriente in nutrientes:
                        name = nutriente.get('name', '').lower()
                        if 'calorie' in name:
                            calorias = nutriente
                        elif 'protein' in name:
                            proteinas = nutriente
                        elif 'carbohydrate' in name:
                            carbohidratos = nutriente
                        elif 'fat' in name and 'saturated' not in name:
                            grasas = nutriente

                    resultado = f"""
                    <strong>Receta Similar Encontrada - {receta['title']}:</strong><br>
                    • Calorías: {calorias.get('amount', 'N/A'):.0f} {calorias.get('unit', '')}<br>
                    • Proteínas: {proteinas.get('amount', 'N/A'):.1f} {proteinas.get('unit', '')}<br>
                    • Carbohidratos: {carbohidratos.get('amount', 'N/A'):.1f} {carbohidratos.get('unit', '')}<br>
                    • Grasas: {grasas.get('amount', 'N/A'):.1f} {grasas.get('unit', '')}<br><br>
                    <em>Nota: Esta es una receta similar de la base de datos. Para análisis preciso de tus ingredientes específicos, usa ingredientes en inglés bien especificados.</em>
                    """
                else:
                    resultado = 'No se encontraron recetas similares. Intenta con un título más común en inglés.'
            else:
                resultado = f'Error en la búsqueda. Código: {response.status_code}. Intenta con otro título.'
                
    except Exception as e:
        resultado = f'Error: {str(e)}'
    
    return render_template('herramientas.html', datos_usuario=datos_usuario, resultado_receta=resultado)

@app.route('/buscar_receta', methods=['POST'])
def buscar_receta():
    datos_usuario = None
    if session.get('logueado'):
        usuario_correo = session.get('usuario_correo')
        if usuario_correo in USUARIOS_REGISTRADOS:
            datos_usuario = USUARIOS_REGISTRADOS[usuario_correo]
    resultado = None
    try:
        ingrediente = request.form.get('ingrediente_receta', '').strip().lower()
        if not ingrediente:
            resultado = 'Por favor ingresa un ingrediente'
        else:
            url = f"{API_BASE}/recipes/complexSearch"
            params = {
                'apiKey': API_KEY,
                'query': ingrediente,
                'number': 3,
                'addRecipeNutrition': True,
                'language': 'en'
            }
            response = requests.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                recetas = data.get('results', [])
                if recetas:
                    resultado = "<strong>Recetas encontradas:</strong><br>"
                    for i, receta in enumerate(recetas, 1):
                        calorias_receta = {}
                        nutricion = receta.get('nutrition')
                        if nutricion:
                            for nutriente in nutricion.get('nutrients', []):
                                if nutriente['name'] == 'Calories':
                                    calorias_receta = nutriente
                                    break 
                        calorias_str = f"{calorias_receta.get('amount', 'N/A'):.0f} calorías" if isinstance(calorias_receta.get('amount'), (int, float)) else "Calorías N/A"
                        resultado += f"""
                        {i}. <strong>{receta['title']}</strong><br>
                            {calorias_str}<br>
                        """
                else:
                    resultado = 'No se encontraron recetas con ese ingrediente'     
                return render_template('herramientas.html', datos_usuario=datos_usuario, resultado_busqueda_receta=resultado)
            else:
                error_info = f'Error de API.'
                resultado = f'Error al buscar recetas: {error_info}'
    except Exception as e:
        resultado = f'Error inesperado: {str(e)}'
    return render_template('herramientas.html', datos_usuario=datos_usuario, resultado_busqueda_receta=resultado)

@app.route('/buscar_receta2', methods=['POST'])
def buscar_receta2():
    datos_usuario = None
    resultado = None
    try:
        excluido = None
        maxima = request.form.get('maxima', '').strip().lower
        minima= request.form.get('minima', '').strip()
        dieta = request.form.get('dieta', '').strip().lower
        tiempo= request.form.get('tiempo', '').strip()
        ingrediente = request.form.get('ingrediente_receta', '').strip().lower()
        if not ingrediente:
            resultado = 'Por favor ingresa un ingrediente'
        else:
            url = f"{API_BASE}/recipes/complexSearch"
            params = {
                'apiKey': API_KEY,
                'query': ingrediente,
                'number': 3,
                'addRecipeNutrition': True,
                'language': 'en',
                # "maxReadyTime": tiempo,  
                #"diet": dieta,
                #"excludeIngredients": excluido,
                #"maxCalories": maxima,
                #"minCalories": minima,
            }
            response = requests.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                recetas = data.get('results', [])
                if recetas:
                    resultado = "<strong>Recetas encontradas:</strong><br>"
                    i = 1
                    for receta in recetas:
                        calorias_receta = {}
                        nutricion = receta.get('nutrition')
                        if nutricion:
                            for nutriente in nutricion.get('nutrients', []):
                                if nutriente['name'] == 'Calories':
                                    calorias_receta = nutriente
                                    break 
                        calorias_str = f"{calorias_receta.get('amount', 'N/A'):.0f} calorías" if isinstance(calorias_receta.get('amount'), (int, float)) else "Calorías N/A"
                        resultado += f"""
                        {i}. <strong>{receta['title']}</strong><br>
                            {calorias_str}<br>
                        """
                        i += 1
                else:
                    resultado = 'No se encontraron recetas con ese ingrediente'     
                return render_template('modulo3.html', datos_usuario=datos_usuario, resultado_busqueda_receta=resultado)
            else:
                error_info = f'Error de API.'
                resultado = f'Error al buscar recetas: {error_info}'
    except Exception as e:
        resultado = f'Error inesperado: {str(e)}'
    return render_template('modulo3.html', datos_usuario=datos_usuario, resultado_busqueda_receta=resultado)
if __name__ == '__main__':
    app.run(debug=True)
