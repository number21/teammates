from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy


builtin_list = list


db = SQLAlchemy()


def init_app(app):
    db.init_app(app)


def from_sql(row):
    """Translates a SQLAlchemy model instance into a dictionary"""
    data = row.__dict__.copy()
    data['id'] = row.id
    data.pop('_sa_instance_state')
    return data


# [START model]
class Mate(db.Model):
    __tablename__ = 'mates'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    author = db.Column(db.String(255))
    publishedDate = db.Column(db.String(255))
    imageUrl = db.Column(db.String(255))
    description = db.Column(db.String(255))
    createdBy = db.Column(db.String(255))
    createdById = db.Column(db.String(255))

    def __repr__(self):
        return "<Mate(title='%s', author=%s)" % (self.title, self.author)
# [END model]


# [START list]
def list(limit=10, cursor=None):
    cursor = int(cursor) if cursor else 0
    query = (Mate.query
             .order_by(Mate.title)
             .limit(limit)
             .offset(cursor))
    mates = builtin_list(map(from_sql, query.all()))
    next_page = cursor + limit if len(mates) == limit else None
    return (mates, next_page)
# [END list]


# [START read]
def read(id):
    result = Mate.query.get(id)
    if not result:
        return None
    return from_sql(result)
# [END read]


# [START create]
def create(data):
    mate = Mate(**data)
    db.session.add(mate)
    db.session.commit()
    return from_sql(mate)
# [END create]


# [START update]
def update(data, id):
    mate = Mate.query.get(id)
    for k, v in data.items():
        setattr(mate, k, v)
    db.session.commit()
    return from_sql(mate)
# [END update]


def delete(id):
    Mate.query.filter_by(id=id).delete()
    db.session.commit()


def _create_database():
    """
    If this script is run directly, create all the tables necessary to run the
    application.
    """
    app = Flask(__name__)
    app.config.from_pyfile('../config.py')
    init_app(app)
    with app.app_context():
        db.create_all()
    print("All tables created")


if __name__ == '__main__':
    _create_database()
