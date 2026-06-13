from flask import Flask
from flask_login import LoginManager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
import config

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = config.SECRET_KEY

# DB
engine = create_engine(config.DB_URL, future=True)
SessionLocal = scoped_session(sessionmaker(bind=engine))

# Login
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    from models import get_db, User
    db = get_db()
    return db.query(User).filter_by(id=int(user_id)).first()

# Import blueprints
from controllers.product_controller import bp as product_bp
from controllers.stock_controller import bp as stock_bp
from controllers.queue_controller import bp as queue_bp
from controllers.recovery_controller import bp as recovery_bp
from auth import auth_bp

app.register_blueprint(product_bp, url_prefix='/api/products')
app.register_blueprint(stock_bp, url_prefix='/api/stock')
app.register_blueprint(queue_bp, url_prefix='/api/queue')
app.register_blueprint(recovery_bp, url_prefix='/api/recovery')
app.register_blueprint(auth_bp, url_prefix='/auth')

@app.route('/')
def index():
    from flask import render_template
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
