from flask_app import app
# from flask_app.controllers import dojos,ninjas
from flask_app.controllers import users , skills


if __name__ == "__main__":
    app.run(debug=True)