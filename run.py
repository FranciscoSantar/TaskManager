from app import create_app, db
from models import *
app = create_app()
with app.app_context():
    db.create_all()

if __name__=='__main__':
    app.run(host='0.0.0.0',port=8000, debug=True)