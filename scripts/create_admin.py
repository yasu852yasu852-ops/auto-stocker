from models import init_db, get_db, User
from werkzeug.security import generate_password_hash
import sys

if __name__ == '__main__':
    init_db()
    db = get_db()
    username = sys.argv[1] if len(sys.argv)>1 else 'admin'
    password = sys.argv[2] if len(sys.argv)>2 else 'admin'
    if db.query(User).filter_by(username=username).first():
        print('user exists')
    else:
        user = User(username=username, password_hash=generate_password_hash(password))
        db.add(user)
        db.commit()
        print('created', username)
