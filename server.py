from flask import Flask, redirect

app = Flask(__name__)

@app.route("/")
def hello():
    return redirect('https://cs61a.org')

if __name__ == "__main__":
    app.run()