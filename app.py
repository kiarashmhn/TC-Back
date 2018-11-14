from flask_migrate import Migrate, MigrateCommand
from QP import app, db
from flask_script import Manager, prompt_bool
manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)


@manager.command
def initdb():
    db.create_all()
    print('Initialized the database')


@manager.command
def dropdb():
    if prompt_bool("Are you sure you want to lose all your data"):
        db.drop_all()
        print('Dropped the database')


if __name__ == '__main__':
    manager.run()
