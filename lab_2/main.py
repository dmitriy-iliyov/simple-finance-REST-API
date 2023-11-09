from flask import Flask, request

from models.user import User

app = Flask(__name__)



if __name__ == "__main__":
    app.run(debug=True)





