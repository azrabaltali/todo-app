from flask import Flask

app = Flask(__name__)

@app.route("/")
def ana_sayfa():
    return "<h1>Merhaba Flask!</h1><p>İlk Python web uygulamam.</p>"

if __name__ == "__main__":
    app.run(debug=True)