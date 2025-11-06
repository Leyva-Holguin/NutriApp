from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__) 

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

if __name__ == '__main__':
    app.run(debug=True)

