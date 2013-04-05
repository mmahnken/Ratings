from flask import Flask, render_template, redirect, request
import model
app = Flask(__name__)

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
		return render_template("user_home.html")
	else:
		return render_template("user_not_found.html")

	




if __name__ == "__main__":
	app.run(debug  = True)

