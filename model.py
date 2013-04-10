import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy import ForeignKey
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.orm import relationship, backref
import correlation

engine = None
session = None

engine = create_engine("sqlite:///ratings.db", echo=False)
session = scoped_session(sessionmaker(bind=engine, autocommit=False, autoflush=False))

Base = declarative_base()
Base.query = session.query_property()

### Class declarations go here
class User(Base):
	__tablename__ = "Users"

	id = Column(Integer, primary_key = True)
	email = Column(String(64), nullable = True)
	password = Column(String(64), nullable = True)
	age = Column(Integer, nullable = True)
	zipcode = Column(String(15), nullable = True)

	def similarity(self, other):
		u_ratings = {}
		paired_ratings = []
		for r in self.ratings:
			u_ratings[r.movie_id] = r 

		for r in other.ratings:
			u_r = u_ratings.get(r.movie.id)
			if u_r:
				paired_ratings.append( (u_r.rating, r.ratings) )

		if paired_ratings:
			return correlation.pearson(paired_ratings)
		else:
			return 0.0    o


class Movie(Base):
	__tablename__ = "Movies"

	id = Column(Integer, primary_key = True)
	name = Column(String(64), nullable = True)
	released_at = Column(Date, nullable = True)
	imdb_url = Column(String(64), nullable = True)

class Rating(Base):
	__tablename__ = "Ratings"

	id = Column(Integer, primary_key = True)
	movie_id = Column(Integer, ForeignKey('Movies.id'))
	user_id = Column(Integer, ForeignKey('Users.id'))
	rating = Column(Integer, nullable = True)

	user = relationship("User", 
			backref=backref("ratings", order_by=id))

### End class declarations


def main():
    """In case we need this for something"""
    pass


if __name__ == "__main__":
    main()
