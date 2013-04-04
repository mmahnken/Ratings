import model
import csv
import datetime


def load_users(session):
    # use u.user
    with open('seed_data/u.user') as f:
        reader = csv.reader(f, delimiter = "|")

        for row in reader:
            title = row
            id = title[0].decode("latin-1")
            age = title[1].decode("latin-1")
            zipcode = title[4].decode("latin-1")
            c = model.User(id=id, age=age, zipcode=zipcode)
            session.add(c)
        session.commit()


def load_movies(session):
    # use u.item
    with open('seed_data/u.item') as f:
        reader = csv.reader(f, delimiter = "|")

        for row in reader:
            title = row
            id = title[0].decode("latin-1")
            name = title[1].decode("latin-1")
            if title[2]:
                released_at = datetime.datetime.strptime(title[2], "%d-%b-%Y")
            else:
                released_at = datetime.datetime.strptime("01-Jan-1970", "%d-%b-%Y") 
            imdb_url = title[4]
            c = model.Movie(id=id, name=name, released_at=released_at, imdb_url=imdb_url)
            session.add(c)
        session.commit()

def load_ratings(session):
    # use u.data
    with open('seed_data/u.data') as f:
        reader = csv.reader(f, delimiter = "\t")
        for row in reader:
            title = row
            print title
            movie_id = title[1].decode("latin-1")
            user_id = title[0].decode("latin-1")
            rating = title[2].decode("latin-1")
            c = model.Ratings(movie_id=movie_id, user_id=user_id, rating=rating)
            session.add(c)
        session.commit()

    

def main(session):
    # You'll call each of the load_* functions with the session as an argument
    load_users(session)
    # load_movies(session) 
    # load_ratings(session)


if __name__ == "__main__":
    s= model.connect()
    main(s)
