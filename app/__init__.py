import json

from scripts import extract_emails
from scripts.mongo import db

from flask import Flask, render_template, request, url_for, redirect, flash
from flask.ext.bootstrap import Bootstrap
from flask.ext.login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from bson.objectid import ObjectId

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
  def __init__(self, email, password, id, active=True):
    self.email = email
    self.password = password
    self.id = id
    self.active = active

  def is_active(self):
    account = db.accounts.find_one({ "email": self.email})
    if account is not None:
      if self.email != account['email'] or check_password(account['account']['password'], self.password) is False:
        self.active = False
    else:
      self.active = False
    return self.active

  def is_anonymous(self):
    return False

  def is_authenticated(self):
    return True

  def get_id(self):
    return str(db.accounts.find_one({'email': self.email})['_id'])

##############################################
##############################################
#######METHODS DEALING WITH LOGGING IN AND OUT
##############################################
##############################################
@login_manager.user_loader
def load_user(userid):
  user_rec = db.accounts.find_one({'_id': ObjectId(userid)})
  user = User(user_rec['email'] ,user_rec['account']['password'], user_rec['_id'])
  return user

@app.route("/logout", methods=["GET"])
@login_required
def logout():
  current_user.active = False
  logout_user()
  return render_template('login.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
  db_email = None
  db_password = None
  if request.method == 'POST':
    post_email = request.form['email']
    post_password = request.form['password']
    try:
      account = db.accounts.find_one({"email": post_email})
      db_password = account['account']['password']
      db_email = account['email']
    except:
      pass
    if db_email != post_email or check_password(db_password, post_password) is False:
      flash('Invalid Credentials, please try again')
    else:
      user = User(post_email, post_password, account['_id'])
      login_user(user)
      return redirect(url_for('home'))
  return render_template('login.html')

@app.route('/check_email', methods=['POST'])
def check_email():
  email = request.form['email']
  email = list(db.accounts.find({'email': email}))
  if email == []:
    return json.dumps(True)
  else:
    return json.dumps(False)

def set_password(password):
  pw_hash = generate_password_hash(password)
  return pw_hash

def check_password(dbpassword, password):
  return check_password_hash(dbpassword, password)

@app.route('/create_account', methods=['POST'])
def create_account():
  if request.method == 'POST':
    new_account = {}
    post_email = request.form['email']
    post_username = request.form['username']
    post_cellphone = request.form['phonenumber']
    post_password = request.form['password']
    # double check the account doens't exist
    dbemail = list(db.accounts.find({'email': post_email}))
    if dbemail != []:
      flash('The Email Already Exist')
      return redirect(url_for('login')) 
    # all the information was validated on the front end so it should be safe to passed it in
    # example object to pass into mongo
    new_account = {
      'username': post_username,
      'password': set_password(post_password),
      'cellphone': post_cellphone,
    }
    db.accounts.update({'email': post_email}, {'email': post_email, 'account': new_account}, upsert=True)
    flash('Account Created')
  return redirect(url_for('login'))

##############################################
##############################################
#######MAIN ROUTE
##############################################
##############################################
@app.route('/')
@login_required
def home():
  return render_template('index.html')

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
