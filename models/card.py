from init import db, ma
from marshmallow import fields, validates
from marshmallow.validate import Length, And, Regexp, OneOf
from marshmallow.exceptions import ValidationError

VALID_STATUSES = ('To Do', 'Done', 'Ongoing', 'Testing', 'Deployed')
VALID_PRIORITIES = ('Low', 'Medium', 'High', 'Urgent')


class Card(db.Model):
    __tablename__ = "cards"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.Text)
    date = db.Column(db.Date)  # Date created
    status = db.Column(db.String)
    priority = db.Column(db.String)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    user = db.relationship('User', back_populates='cards')
    comments = db.relationship(
        'Comment', back_populates='card', cascade='all, delete')


class CardSchema(ma.Schema):
    user = fields.Nested('UserSchema', only=['name', 'email'])
    comments = fields.List(fields.Nested('CommentSchema'), exclude=['card'])

    title = fields.String(required=True, validate=And(
        Length(min=2, error='Title must be at least 2 characters long'),
        Regexp('^[a-zA-Z0-9 ]+$',
               error='Only letters, spaces and numbers are allowed')
    ))

    status = fields.String(validate=OneOf(VALID_STATUSES))

    priority = fields.String(validate=OneOf(VALID_PRIORITIES))

    @validates('status')
    def validate_status(self, value):
        if value == VALID_STATUSES[2]:
            stmt = db.select(db.func.count()).select_from(
                Card).filter_by(status=VALID_STATUSES[2])
            count = db.session.scalar(stmt)
            if count > 0:
                raise ValidationError('You already have an ongoing card')

    class Meta:
        fields = ('id', 'title', 'description',
                  'date', 'status', 'priority', 'user', 'comments')
        ordered = True


card_schema = CardSchema()
cards_schema = CardSchema(many=True)
