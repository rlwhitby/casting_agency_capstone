from application import db
from application.enums import GenreEnum

# ----------------------------------------------------------------------------#
# Association Table - many-to-many relationship
# ----------------------------------------------------------------------------#
#TODO
# Using association table as only the actor id and movie id columns are used
# Ref: https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html#relationship-patterns
actors_movies = db.Table('actors_movies',
                                     db.Column(
                                         "actor_id",
                                          db.Integer,
                                          db.ForeignKey("actors.id"),
                                          primary_key=True),
                                     db.Column(
                                         "movie_id",
                                         db.Integer,
                                         db.ForeignKey("movies.id"),
                                         primary_key=True)
                                     )

# ----------------------------------------------------------------------------#
# Actor Model
# ----------------------------------------------------------------------------#
class Actor(db.Model):
    __tablename__ = "actors"
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(), nullable=False)
    age = db.Column(db.Integer(), nullable=False)
    gender = db.Column(db.String(), nullable=False)
    movies = db.relationship(
            'Movie',
            secondary="actors_movies",
            back_populates="actors"
    #     lazy=True,
    #     # Ref: https://knowledge.udacity.com/questions/637391#637486
    #TODO is delete needed to remove movie from actor if deleted and visa versa?
    #     cascade="all, delete"
    )

    '''
    insert()
        inserts a new model into a database
        the model must have a unique id or null id
        EXAMPLE
            actor = Actor(name=req_name, age=27, gender=Male)
            actor.insert()
    '''

    def insert(self):
        db.session.add(self)
        db.session.commit()

    '''
    update()
        updates a model in a database
        the model must exist in the database
        EXAMPLE
            actor = Actor.query.filter(Actor.id == id).one_or_none()
            actor.name = 'Tom Cruise'
            actor.update()
    '''

    def update(self):
        db.session.commit()

    '''
    delete()
        deletes a model from database
        the model must exist in the database
        EXAMPLE
            actor = Actor(name=req_name, age=27, gender=Male)
            actor.delete()
    '''

    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def format(self):
        # Ref: https://www.geeksforgeeks.org/python-ways-to-find-length-of-list/?ref=lbp
        if len(self.movies) == 0:
            movies = "This actor has not been cast in any movies"
        elif len(self.movies) == 1:
            movies = "This actor has been cast in "+ str(len(self.movies)) +" movie"
        else:
            movies = "This actor has been cast in "+ str(len(self.movies)) +" movies"
        return {
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "gender": self.gender,
            "movies": movies

        }
    
    #TODO: is this needed?
    def __repr__(self):
        return f'Actor: {self.id}, {self.name}, {self.age}, {self.gender}'

# ----------------------------------------------------------------------------#
# Movie Model
# ----------------------------------------------------------------------------#
class Movie(db.Model):
    __tablename__ = "movies"

    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(), nullable=False)
    #TODO - check default is correct
    # default=datetime.now()
    release_date = db.Column(db.DateTime(), nullable=False)
    genre = db.Column(db.Enum(GenreEnum), nullable=False)
    # Ref: https://knowledge.udacity.com/questions/510080#510112
    # The backref is now considered legacy
    # Ref: https://docs.sqlalchemy.org/en/20/orm/backref.html
    actors = db.relationship(
            'Actor',
            secondary="actors_movies",
            back_populates="movies"
    #     lazy=True,
    #     # Ref: https://knowledge.udacity.com/questions/637391#637486
    #     cascade="all, delete"
    )

    '''
    insert()
        inserts a new model into a database
        the model must have a unique id or null id
        EXAMPLE
            actor = Actor(name=req_name, age=27, gender=Male)
            actor.insert()
    '''

    def insert(self):
        db.session.add(self)
        db.session.commit()

    '''
    update()
        updates a model in a database
        the model must exist in the database
        EXAMPLE
            actor = Actor.query.filter(Actor.id == id).one_or_none()
            actor.name = 'Tom Cruise'
            actor.update()
    '''

    def update(self):
        db.session.commit()

    '''
    delete()
        deletes a model from database
        the model must exist in the database
        EXAMPLE
            actor = Actor(name=req_name, age=27, gender=Male)
            actor.delete()
    '''

    def delete(self):
        db.session.delete(self)
        db.session.commit()
    

    def format(self):
        # Ref: https://www.geeksforgeeks.org/python-ways-to-find-length-of-list/?ref=lbp
        if len(self.actors) == 0:
            actors = "This movie has no actors"
        elif len(self.actors) == 1:
            actors = "This movie has "+ str(len(self.actors)) +" actor"
        else:
            actors = "This movie has "+ str(len(self.actors)) +" actors"
        return {
            "id": self.id,
            "title": self.title,
            "release date": self.release_date,
            "genre": self.genre,
            "actors": actors
        }
    #TODO: is this needed?
    def __repr__(self):
        return f'Actor: {self.id}, {self.title}, {self.release_date}'