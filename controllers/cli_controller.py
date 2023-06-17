from flask import Blueprint
from init import db, bcrypt
from models.user import User

db_commands = Blueprint('db', __name__)


@db_commands.cli.command('create')
def create_db():
    db.create_all()
    print("Tables Created")


@db_commands.cli.command('drop')
def drop_db():
    db.drop_all()
    print("Tables dropped")


@db_commands.cli.command('seed')
def seed_db():
    users = [
        User(
            email="admin@admin.com",
            password=bcrypt.generate_password_hash('admin123').decode('utf-8'),
            is_admin=True
        ),
        User(
            name='User User1',
            email="user1@email.com",
            password=bcrypt.generate_password_hash('user1pw').decode('utf-8')
        )
    ]

    db.session.add_all(users)
    db.session.commit()

    print('Tables seeded')
