from flask import Flask
from routes.ProductRoutes import notes_bp
from routes.UserRoutes import auth_bp
from routes.CategoryRoutes import cate_bp
from flask_jwt_extended import JWTManager

app = Flask(__name__, static_folder='static')

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.register_blueprint(notes_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(cate_bp)
app.config['JWT_SECRET_KEY'] = 'ZIN!moe@002580'  # Change this to a random secret key
jwt = JWTManager(app)

if __name__ == '__main__':
    app.run(port=5000, debug=True)