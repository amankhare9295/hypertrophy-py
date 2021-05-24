from flask import Flask, render_template, json, request, session, redirect,url_for
from flask_sqlalchemy import SQLAlchemy
app= Flask(__name__)
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123456@localhost/User'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']   = False

@app.route("/")
def main():
    return render_template('login.html')

@app.route("/SignUp")
def SignUp():
    return render_template('SignUp.html')

@app.route("/submit",methods=["POST"])
def submit():
    if request.method == "POST":

        UserID=request.form['UserID']
        password=request.form['password']
        Email=request.form['Email']
        if (UserID=='') &  (password==''):
            return render_template('SignUp.html', message='Please enter required fields')
        if db.session.query(user_info).filter(user_info.UserID == UserID).count() == 0:
            data= user_info(UserID,Email,password)
            db.session.add(data)
            db.session.commit()
            return render_template('SignUp.html', message='Account Created')
        return  render_template('SignUp.html', message='UserID already exists')


class user_info(db.Model):
    __tablename__='user_info'
    UserID=db.Column(db.String(25),primary_key=True)
    Email=db.Column(db.String(25))
    password=db.Column(db.String(25))
    def __init__(self,UserID,Email,password):
        self.UserID=UserID
        self.Email=Email
        self.password=password
@app.route("/login")
def login():
    return render_template('login.html')

@app.route("/loginattempt",methods=["POST"])
def loginattempt():
    if request.method == "POST":
        UserID=request.form['UserID']
        password=request.form['password']
        user=user_info.query.filter_by(UserID=UserID).first()

        if (user.UserID==UserID) & (user.password==password):
            db.session.close()
            return render_template('index.html', message=f'{UserID} has logged in')

        return  render_template('login.html', message='login unauthenticated')

@app.route("/logout")
def Signout():
    db.session.close()
    return render_template('login.html',message='Successfully logged out')






if __name__=='__main__':
    app.debug= True
    app.run()
