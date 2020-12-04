from flask import Flask,render_template,request,redirect,url_for,session,flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key='lejuregbbrlj kefu'
app.config['SQLAlchemy_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQLAlchemy_TRACK_MODIFICATIONS'] = False
app.permanent_session_lifetime = timedelta(minutes=5)

db = SQLAlchemy(app)


class Users(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column("name",db.String(100))
    email = db.Column("email",db.String(100))

    def __init__(self,name,email):
        self.name = name
        self.email = email




@app.route('/', methods=['POST','GET'])
def home():
    return render_template('index.html')



@app.route('/view', methods=['POST','GET'])
def view():
    return render_template('view.html',values=Users.query.all())




@app.route('/login', methods=['POST','GET'])
def Login():
    if request.method == "POST":
        session.permanent  = True
        user = request.form["nm"]
        session['user'] = user

        found_user =  Users.query.filter_by(name=user).first()
        if found_user:
            session['email'] = found_user.email
        else:
            usr = Users(user, "")  # db
            db.session.add(usr)
            db.session.commit()

        flash('Login Successfull')
        return redirect(url_for("Info"))
    else:
        if "user" in session:
            flash('Already Logged in !')
            return redirect(url_for("Info"))

        return render_template('login.html')
    
 
@app.route('/user',methods=['POST','GET'])
def Info():
    email = None
    if "user" in session:
        user = session['user']

        if request.method == 'POST':
            email = request.form['email']
            session['email'] = email

            found_user =  Users.query.filter_by(name=user).first()
            found_user.email = email
            db.session.commit()

            flash("Email Was Saved")
        else:
            if "email" in session:
                email = session['email']

        return render_template('user.html',email=email)
    else:
        return redirect(url_for('Login'))


@app.route('/logout')
def Logout():
    if "user" in session:
        user = session['user']
        flash(f'U Have Been Logout {user}',"info")

    session.pop("user",None)
    session.pop("email",None)
    return redirect(url_for('Login'))


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True ) 




