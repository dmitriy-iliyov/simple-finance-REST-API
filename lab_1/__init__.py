from flask import Flask

app = Flask(__name__)

import views as vs


@app.route('/')
def endpoint():
    return vs.healthcheck()


if __name__ == "__main__":
    app.run(debug=True)
