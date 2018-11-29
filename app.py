from flask import request, abort
from flask_migrate import Migrate, MigrateCommand
from QP import app, db
from QP.auth.models import User
from QP.car.models import Car
from flask_script import Manager, prompt_bool
manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)


@manager.command
def initdb():
    db.create_all()
    user = User(name="admin", username="admin", password="admin", role="admin")
    db.session.add(user)
    db.session.commit()
    car = Car(name="peykan", factory="bmw", kilometer=0, year=1931, color="sefid yakhchali",
              description="mashin e khafan", automate=True, user_id=1, price=1000, image_url="peykan.jpg")
    carr = Car(name="peykan", factory="bmw", kilometer=0, year=1931, color="sefid yakhchali",
               description="mashin e khafan", automate=True, user_id=1, price=1000, image_url="peykan.jpg")
    carrr = Car(name="peykan", factory="bmw", kilometer=0, year=1931, color="sefid yakhchali",
                description="mashin e khafan", automate=True, user_id=1, price=1000, image_url="peykan.jpg")
    db.session.add(car)
    db.session.add(carr)
    db.session.add(carrr)

    db.session.commit()
    print('Initialized the database')


@manager.command
def dropdb():
    if prompt_bool("Are you sure you want to lose all your data"):
        db.drop_all()
        print('Dropped the database')


@manager.command
def run():
    app.run(debug=True, host='0.0.0.0')


@app.before_request
def before_request():
    if not request.is_json and request.method == 'POST':
        return abort(400, "Bad request")


if __name__ == '__main__':
    manager.run()
