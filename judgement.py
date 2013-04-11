from flask import Flask, render_template, redirect, request, session, g
import model
app = Flask(__name__)

@app.before_request
def before_request():
	if 'id' in session:
		g.user = session.query(Users).get(session['id'])
	else:
		return render_template("login.html")

@app.route("/all_users")
def all_users():
	user_list = model.session.query(model.User).limit(5).all()
	return render_template("user_list.html", users=user_list)

#takes in new user info
@app.route("/new_user")
def create_new():
	return render_template("new_user_form.html")

#accepts, adds, and commits new user info
@app.route("/save_user", methods=["POST"])
def save_new_user():
	new_person = model.User(email=request.form["email"], password=request.form["password"], age=request.form["age"], zipcode=request.form["zipcode"])
	model.session.add(new_person)
	model.session.commit()
	q = new_person.email
	return render_template("save_user.html", newperson = q)

@app.route("/login", methods=["POST", "GET"])
def login():
	return render_template("login.html")

@app.route("/authenticate", methods=["POST"])
def authenticate():
	user_email = request.form["email"]
	user_password = request.form["password"]
	u = model.session.query(model.User).filter_by(email = user_email).first()
	if u.password == user_password:
		session['id'] = u.id
		return render_template("user_home.html")
	else:
		return render_template("user_not_found.html")

@app.route("/movie/<int:id>", methods =["GET"])
def view_movie(id):
	movie = db_session.query(Movie).get(id)
	ratings = movie.ratings
	rating_nums = []
	user_rating = None
	for r in ratings:
		if r.user_id == session['user_id']:
			user_rating = r
		rating_nums.append(r.rating)
	avg_rating = float(sum(rating_nums))/len(rating_nums)

	#prediction code: only predict if the user hasn't rated it.
	user = db_session.query(User).get(session['user_id'])
	prediction = None
	if not user_rating:
		prediction = user.predict_rating(movie)
		effective_rating = prediction
	else:
		effective_rating = user_rating.rating

	the_eye = db_session.query(User).filter_by(email="theeye@ofjudgement.com").one()
	eye_rating = db_session.query(Rating).filter_by(user_id=the_eye.id, movie_id=movie_id).first()

	if not eye_rating:
		eye_rating = the_eye.predict_rating(movie)
	else:
		eye_rating = eye_rating.rating

	difference = abs(eye_rating - effective_rating)
	#End prediction

	return render_template("movie.html", movie=movie,
		average=avg_rating, user_rating=user_rating,
		prediction=prediction)

	messages = [ "I suppose you don't have such bad taste after all.",
             "I regret every decision that I've ever made that has brought me to listen to your opinion.",
             "Words fail me, as your taste in movies has clearly failed you.",
             "That movie is great. For a clown to watch. Idiot."]

	beratement = messages[int(difference)]
	




if __name__ == "__main__":
	app.run(debug  = True)

