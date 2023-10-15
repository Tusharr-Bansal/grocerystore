from applications.database import db

from flask import Flask

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///.\database.db"
app.secret_key = '1234'
db.init_app(app)
app.app_context().push()



from applications.controllers import *



if __name__== '__main__':
    db.create_all()
    app.debug=True
    app.run()







