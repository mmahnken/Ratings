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
	new = request.form['email']
	new_person = model.User(email= new, password = "password", age="age", zipcode="zipcode")
	model.session.add(new_person)
	model.session.commit()

	return render_template("save_user.html", newperson = new_person)

if __name__ == "__main__":
	app.run(debug  = True)

