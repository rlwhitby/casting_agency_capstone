import enum

'''
    Class GenreEnum has been implemented to demonstrate how enums can be used
    to enforce what values are allowed in a field at the database level.
'''
# Ref 1: https://medium.com/the-andela-way/how-to-create-django-like-choices-field-in-flask-sqlalchemy-1ca0e3a3af9d
# Ref 2: https://hultner.se/quickbits/2018-03-12-python-json-serializable-enum.html
# Ref 3: https://www.imdb.com/feature/genre/
class GenreEnum(str, enum.Enum):
    Action = "Action"
    Adventure = "Adventure"
    Animation = "Animation"
    Biography = "Biography"
    Comedy = "Comedy"
    Crime = "Crime"
    Documentary = "Documentary"
    Drama = "Drama"
    Family = "Family"
    Fantasy = "Fantasy"
    History = "History"
    Horror = "Horror"
    Musical = "Musical"
    Romance = "Romance"
    Scifi = "Scifi"
