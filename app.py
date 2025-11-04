
app = Flask(__name__)

@app.route('/')
def inicio():
    return 'index.html'

if __name__ == '__main__':
    app.run(debug=True)

