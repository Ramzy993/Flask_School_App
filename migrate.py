import os
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from school_app import app, db

# migration_folder = os.path.abspath(os.path.dirname(__file__))
# migration_folder = os.path.join(migration_folder, 'migration')

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
