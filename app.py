from flask_migrate import Migrate, MigrateCommand
from QP import app, db
from QP.auth.models import User
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
    print('Initialized the database')


@manager.command
def dropdb():
    if prompt_bool("Are you sure you want to lose all your data"):
        db.drop_all()
        print('Dropped the database')


if __name__ == '__main__':
    manager.run()
