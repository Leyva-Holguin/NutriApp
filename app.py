from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__) 

app.config['SECRET_KEY'] = 'la_primera_es_la_primera'

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

