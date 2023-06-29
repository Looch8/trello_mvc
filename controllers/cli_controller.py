from flask import Blueprint
from init import db, bcrypt
from models.user import User
from models.card import Card
from models.comment import Comment
from datetime import date

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
            email='admin@admin.com',
            password=bcrypt.generate_password_hash('admin123').decode('utf-8'),
            is_admin=True
        ),
        User(
            name='User User1',
            email='user1@email.com',
            password=bcrypt.generate_password_hash('user1pw').decode('utf-8')
        )
    ]

    db.session.add_all(users)

    cards = [
        Card(
            title='Card 1',
            description='Card 1 description',
            status='To Do',
            priority='High',
            date=date.today(),
            user=users[0]
        ),
        Card(
            title='Card 2',
            description='Card 2 description',
            status='Ongoing',
            priority='Medium',
            date=date.today(),
            user=users[0]
        ),
        Card(
            title='Card 3',
            description='Card 3 description',
            status='Done',
            priority='Low',
            date=date.today(),
            user=users[1]
        ),
        Card(
            title='Card 4',
            description='Card 4 description',
            status='To Do',
            priority='Medium',
            date=date.today(),
            user=users[1]
        )
    ]

    db.session.add_all(cards)

    comments = [
        Comment(
            message="Comment 1",
            user=users[0],
            card=cards[0]
        ),
        Comment(
            message="Comment 2",
            user=users[1],
            card=cards[2]
        ),
        Comment(
            message="Comment 3",
            user=users[1],
            card=cards[3]
        ),
        Comment(
            message="Comment 4",
            user=users[0],
            card=cards[3]
        )
    ]

    db.session.add_all(comments)

    db.session.commit()

    print("Tables seeded")
