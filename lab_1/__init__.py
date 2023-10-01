from flask import Flask
from .views import healthcheck
# import views


app = Flask(__name__)


@app.route('/')
def endpoint():
    return healthcheck()


if __name__ == "__main__":
    app.run(debug=True)
