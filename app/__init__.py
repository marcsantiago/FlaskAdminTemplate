import json
import os 

from datetime import datetime

from flask import Flask, render_template, request, url_for, redirect
from flask.ext.bootstrap import Bootstrap
from flask.ext.login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user

from bson.objectid import ObjectId

from lib.mongo import db
from scripts.twitter_stats import ratio_of_wiki_links
from scripts.electric_bill_calculator import ElectricBill

app = Flask(__name__)
app.config["SECRET_KEY"] = ''
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
bootstrap = Bootstrap(app)


##############################################
##############################################
#######USER CLASS FOR LOGGING IN AND OUT
##############################################
##############################################
class User(UserMixin):
  def __init__(self, name, password, id, active=True):
    self.name = name
    self.password = password
    self.id = id
    self.active = active

  def is_active(self):
    account = db.users.find_one({ "username": self.name})
    if account is not None:
      if not account['username'] == self.name and account['password'] == self.password:
        self.active = False
    else:
      self.active = False
    return self.active

  def is_anonymous(self):
    return False

  def is_authenticated(self):
    return True
  
  def get_id(self):
    return str(db.users.find_one({'username': self.name})['_id'])

##############################################
##############################################
#######METHODS DEALING WITH LOGGING IN AND OUT
##############################################
##############################################
@login_manager.user_loader
def load_user(userid):
  user_rec = db.users.find_one({'_id': ObjectId(userid)})
  user = User(user_rec['username'], user_rec['password'], user_rec['_id'])
  return user

@app.route("/logout", methods=["GET"])
@login_required
def logout():
  current_user.active = False 
  logout_user()
  return render_template('login.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
  error = None
  db_username = None
  db_password = None
  if request.method == 'POST':
    post_username = request.form['username']
    post_password = request.form['password']
    try:
      account = db.users.find_one({ "username": post_username})
      db_password = account['password']
      db_username = account['username']
    except:
      pass
    if post_username != db_username or post_password != db_password:
      error = 'Invalid Credentials, please try again'
    else:
      user = User(post_username, post_password, account['_id'])
      login_user(user)
      return redirect(url_for('home'))
  return render_template('login.html', error=error)

##############################################
##############################################
#######MAIN ROUTE
##############################################
##############################################
@app.route('/')
@login_required
def home():
  pass


##############################################
##############################################
#######ERROR HANDLING METHODS
##############################################
##############################################
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_not_found(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
  app.run(debug=True, threaded=True)
