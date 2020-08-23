from flask import Flask, render_template, redirect, url_for, request
from flask_wtf import FlaskForm, CsrfProtect
from flask_bootstrap import Bootstrap
from wtforms import StringField, PasswordField, BooleanField, IntegerField, TextField, RadioField
from wtforms.validators import InputRequired, Email, Length
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import random, copy
import sqlite3
import datetime
from datetime import date
from sqlite3 import Error
import uuid
from flask_mail import Mail, Message

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'shantimentalhealthapp@gmail.com'
app.config['MAIL_PASSWORD'] = 'shanti2020'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
Bootstrap(app)
db = SQLAlchemy(app)
mail = Mail(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(80))
    profile = db.relationship('UserProfile', backref='user')
    stats = db.relationship('Stats', backref='user')
    rmchange = db.relationship('rmchange', backref='user')
    rmpast = db.relationship('rmpast', backref='user')
    pwcontrol = db.relationship('pwcontrol', backref='user')
    pwevidence = db.relationship('pwevidence', backref='user')
    nttrue = db.relationship('nttrue', backref='user')
    ntpositive = db.relationship('ntpositive', backref='user')
    scgood = db.relationship('scgood', backref='user')
    screword = db.relationship('screword', backref='user')
    scchange = db.relationship('scchange', backref='user')
    dmworst = db.relationship('dmworst', backref='user')

class UserProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    age = db.Column(db.Integer)
    sex = db.Column(db.String(50))
    hobbies = db.Column(db.Text)
    interests = db.Column(db.Text)
    imp = db.Column(db.Text)

class Stats(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_date = db.Column(db.DateTime, default=datetime.datetime.now().date())
    overall = db.Column(db.Integer)
    rm = db.Column(db.Integer)
    pw = db.Column(db.Integer)
    nt = db.Column(db.Integer)
    sc = db.Column(db.Integer)
    dm = db.Column(db.Integer)
    c = db.Column(db.Integer)
    el = db.Column(db.Integer)
    s = db.Column(db.Integer)

class rmchange(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_date = db.Column(db.DateTime, default=datetime.datetime.now().date())
    thought = db.Column(db.Text)
    suggestion = db.Column(db.Text)
    add = db.Column(db.Boolean, default=False)

class rmpast(db.Model):
    id =db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_date = db.Column(db.DateTime, default=datetime.datetime.now().date())
    thought = db.Column(db.Text)
    add =db.Column(db.Boolean, default=False)

class pwcontrol(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_date = db.Column(db.DateTime, default=datetime.datetime.now().date())
    thought = db.Column(db.Text)
    suggestion = db.Column(db.Text)
    control = db.Column(db.Boolean, default=False)
    add = db.Column(db.Boolean, default=True)

class pwevidence(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_date = db.Column(db.DateTime, default=datetime.datetime.now().date())
    thought = db.Column(db.Text)
    suggestion = db.Column(db.Text)
    control = db.Column(db.Boolean, default=False)
    add = db.Column(db.Boolean, default=True)

class nttrue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_date = db.Column(db.DateTime, default=datetime.datetime.now().date())
    thought = db.Column(db.Text)
    suggestion = db.Column(db.Text)
    control = db.Column(db.Boolean, default=False)
    add = db.Column(db.Boolean, default=True)

class ntpositive(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_date = db.Column(db.DateTime, default=datetime.datetime.now().date())
    thought = db.Column(db.Text)
    suggestion = db.Column(db.Text)
    add = db.Column(db.Boolean, default=True)

class scgood(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_date = db.Column(db.DateTime, default=datetime.datetime.now().date())
    thought = db.Column(db.Text)
    add = db.Column(db.Boolean, default=True)

class screword(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_date = db.Column(db.DateTime, default=datetime.datetime.now().date())
    thought = db.Column(db.Text)
    suggestion = db.Column(db.Text)
    add = db.Column(db.Boolean, default=False)

class scchange(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_date = db.Column(db.DateTime, default=datetime.datetime.now().date())
    thought = db.Column(db.Text)
    suggestion = db.Column(db.Text)
    control = db.Column(db.Boolean, default=False)
    add = db.Column(db.Boolean, default=True)

class dmworst(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_date = db.Column(db.DateTime, default=datetime.datetime.now().date())
    thought = db.Column(db.Text)
    suggestion = db.Column(db.Text)
    add = db.Column(db.Boolean, default=False)

class dmnow(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_date = db.Column(db.DateTime, default=datetime.datetime.now().date())
    thought = db.Column(db.Text)
    suggestion = db.Column(db.Text)
    add = db.Column(db.Boolean, default=False)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    #remember = BooleanField('remember me')

class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=255)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])

class UserProfileForm(FlaskForm):
    first_name = StringField('first_name', validators=[InputRequired()])
    last_name = StringField('last_name', validators=[InputRequired()])
    age = IntegerField('age', validators=[InputRequired()])
    sex = StringField('sex', validators=[InputRequired()])
    hobbies = TextField('hobbies', validators=[InputRequired()])
    interests = TextField('interests', validators=[InputRequired()])
    imp = TextField('imp', validators=[InputRequired()])

class rmchangeForm(FlaskForm):
    thought = TextField('Thoughts', validators=[InputRequired()])
    suggestion = TextField('Suggestion', validators=[InputRequired()])
    add = BooleanField('Add')

class rmpastForm(FlaskForm):
    thought = TextField('Thought', validators=[InputRequired()])
    add = BooleanField('add')

class pwcontrolForm(FlaskForm):
    thought = TextField('Thought', validators=[InputRequired()])
    suggestion = TextField('Suggestion', validators=[InputRequired()])
    control = BooleanField('Control')
    add = BooleanField('Add')

class pwevidenceForm(FlaskForm):
    thought = TextField('Thought', validators=[InputRequired()])
    suggestion = TextField('Suggestion', validators=[InputRequired()])
    control = BooleanField('Evidence')
    add = BooleanField('Add')

class nttrueForm(FlaskForm):
    thought = TextField('Thought', validators=[InputRequired()])
    suggestion = TextField('Suggestion', validators=[InputRequired()])
    control = BooleanField('True')
    add = BooleanField('Add')

class ntpositiveForm(FlaskForm):
    thought = TextField('Thoughts', validators=[InputRequired()])
    suggestion = TextField('Suggestion', validators=[InputRequired()])
    add = BooleanField('Add')

class scgoodForm(FlaskForm):
    thought = TextField('Thought', validators=[InputRequired()])
    add = BooleanField('add')

class screwordForm(FlaskForm):
    thought = TextField('Thoughts', validators=[InputRequired()])
    suggestion = TextField('Suggestion', validators=[InputRequired()])
    add = BooleanField('Add')

class scchangeForm(FlaskForm):
    thought = TextField('Thought', validators=[InputRequired()])
    suggestion = TextField('Suggestion', validators=[InputRequired()])
    control = BooleanField('Change')
    add = BooleanField('Add')

class dmworstForm(FlaskForm):
    thought = TextField('Thoughts', validators=[InputRequired()])
    suggestion = TextField('Suggestion', validators=[InputRequired()])
    add = BooleanField('Add')

class dmnowForm(FlaskForm):
    thought = TextField('Thoughts', validators=[InputRequired()])
    suggestion = TextField('Suggestion', validators=[InputRequired()])
    add = BooleanField('Add')

class forgotForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])

class resetPasswordForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    password = PasswordField('new password', validators=[InputRequired(), Length(min=8, max=80)])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=["GET", "POST"])
def signup():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for('initialuserprofile'))
    return render_template('signup.html', form=form)


@app.route('/initialuserprofile', methods=["GET", "POST"])
def initialuserprofile():
    form = UserProfileForm()
    if form.validate_on_submit():
        new_user_profile = UserProfile(user_id=current_user.id, first_name=form.first_name.data,\
        last_name=form.last_name.data, age=form.age.data, sex=form.sex.data, \
        hobbies=form.hobbies.data, interests=form.interests.data, imp=form.imp.data)
        db.session.add(new_user_profile)
        db.session.commit()
        return redirect(url_for('dashboard'))
    return render_template('initialuserprofile.html', form=form)


@app.route('/userprofile', methods=["GET", "POST"])
def userprofile():
    userid = current_user.id
    user = UserProfile.query.order_by(UserProfile.id.desc()).filter_by(user_id=userid).first()
    return render_template('userprofile.html', first_name=user.first_name, last_name=user.last_name,\
                            username=current_user.username, email=current_user.email, age=user.age,\
                            gender=user.sex, hobbies=user.hobbies,interests=user.interests, imp=user.imp)


@app.route('/login', methods=["GET", "POST"])
def login():
    print("login method")
    form = LoginForm()
    print(form.username.data)
    print(form.password.data)
    print(request.method)
    if form.validate_on_submit():
        print("form was validated")
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            print("user was found")
            if check_password_hash(user.password, form.password.data):
                print("password is matched to user")
                login_user(user)
                print("there is a match")
                return redirect(url_for('dashboard'))
        print("password did not match")
    return render_template('login.html', form=form)


@app.route('/forgot', methods=["GET", "POST"])
def forgot():
    form = forgotForm()
    if form.validate_on_submit():
        user_email = form.email.data
        msg = Message('Password Reset Email', sender='shantimentalhealthapp@gmail.com', recipients=[user_email])
        msg.body = "Hello. We have recieved a request to reset your password. To reset your password, please click on this link: http://127.0.0.1:5000/resetpassword "
        mail.send(msg)
        return "We have have sent an email to the address provided."
    return render_template('forgot.html', form=form)


@app.route('/resetpassword', methods=["GET", "POST"])
def resetpassword():
    form = resetPasswordForm()
    if form.validate_on_submit():
        user_email=form.email.data
        user=User.query.filter_by(email=user_email).first()
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        user.password = hashed_password
        db.session.commit()
        login_user(user)
        return redirect(url_for('dashboard'))

    return render_template('resetpassword.html', form=form)



def last_entry_date(database):
    last_entry = database.query.order_by(database.id.desc()).filter_by(user_id=current_user.id).first()
    if last_entry is not None:
        entry_date = last_entry.created_date
        return entry_date
    else:
        return None

def list_entries(database,i):
    all_entries = database.query.filter_by(user_id=current_user.id, created_date=i).all()
    return all_entries


@app.route('/records', methods=["GET", "POST"])
@login_required
def records():
    dict = {}
    all_tests = Stats.query.filter_by(user_id=current_user.id).all()
    test_dates = []
    for i in all_tests:
        date = i.created_date
        #str_date = str(date)
        #print(str_date)
        test_dates.append(date)

    print(test_dates)

    for i in test_dates:
        date_rmchange = last_entry_date(rmchange)
        date_rmpast = last_entry_date(rmpast)
        date_pwcontrol = last_entry_date(pwcontrol)
        date_pwevidence = last_entry_date(pwevidence)
        date_nttrue = last_entry_date(nttrue)
        date_ntpositive = last_entry_date(ntpositive)
        date_scgood = last_entry_date(scgood)
        date_screword = last_entry_date(screword)
        date_scchange = last_entry_date(scchange)
        date_dmworst = last_entry_date(dmworst)
        date_dmnow = last_entry_date(dmnow)

        if (i==date_rmchange):
            list = list_entries(rmchange,i)
            list.insert(0,'rmchange')
            dict[i] = list
        elif (i==date_rmpast):
            list = list_entries(rmpast,i)
            list.insert(0,'rmpast')
            dict[i] = list
        elif (i==date_pwcontrol):
            list = list_entries(pwcontrol,i)
            list.insert(0,'pwcontrol')
            dict[i] = list
        elif (i==date_pwevidence):
            list = list_entries(pwevidence,i)
            list.insert(0,'pwevidence')
            dict[i] = list
        elif (i==date_nttrue):
            list = list_entries(nttrue,i)
            list.insert(0,'nttrue')
            dict[i] = list
        elif (i==date_ntpositive):
            list = list_entries(ntpositive,i)
            list.insert(0,'ntpositive')
            dict[i] = list
        elif (i==date_scgood):
            list = list_entries(scgood,i)
            list.insert(0,'scgood')
            dict[i] = list
        elif (i==date_screword):
            list = list_entries(screword,i)
            list.insert(0,'screword')
            dict[i] = list
        elif (i==date_scchange):
            list = list_entries(scchange,i)
            list.insert(0,'scchange')
            dict[i] = list
        elif (i==date_dmworst):
            list = list_entries(dmworst,i)
            list.insert(0,'dmworst')
            dict[i] = list
        elif (i==date_dmnow):
            list = list_entries(dmnow,i)
            list.insert(0,'dmnow')
            dict[i] = list

    print("The dict is:")
    print(dict)

    return render_template('records.html', q=dict)


@app.route('/dashboard')
@login_required
def dashboard():
    userid = current_user.id
    user = Stats.query.order_by(Stats.id.desc()).filter_by(user_id=userid).first()

    new_day = datetime.timedelta(days=1)
    latest_date = user.created_date
    last_day = latest_date.date()
    target = new_day + latest_date
    today = date.today()
    target_date = target.date()
    str_today = str(today)
    str_target = str(target_date)
    print(last_day)
    print(today)

    q_entries = Stats.query.filter_by(user_id=userid).all()
    num_entries = len(q_entries)
    print(num_entries)

    quiz_num= None

    for x in range(1):
        quiz_num = random.randint(1,5)

    print(quiz_num)

    activity = None
    max_stat = max(user.rm, user.pw, user.nt, user.sc, user.dm)
    print(max_stat)
    if (max_stat == user.rm):
        activity = user.rm
    elif (max_stat == user.pw):
        activity = user.pw
    elif (max_stat == user.nt):
        activity = user.nt
    elif (max_stat== user.sc):
        activity = user.sc
    elif (max_stat == user.dm):
        activity = user.dm

    print(activity)


    if (num_entries > 1):
        difference = Stats.query.order_by(Stats.id.desc()).filter_by(user_id=userid).limit(2).all()

        id1 = difference[1].id
        id2 = difference[0].id

        user_id1 = Stats.query.filter_by(id=id1).first()
        user_id2 = Stats.query.filter_by(id=id2).first()

        overall_diff = user_id1.overall - user_id2.overall
        rm_diff = round(user_id1.rm - user_id2.rm)
        pw_diff = round(user_id1.pw - user_id2.pw)
        nt_diff = round(user_id1.nt - user_id2.nt)
        sc_diff = round(user_id1.sc - user_id2.sc)
        dm_diff = round(user_id1.dm - user_id2.dm)
        c_diff = round(user_id1.c - user_id2.c)
        el_diff = round(user_id1.el - user_id2.el)
        s_diff = round(user_id1.s - user_id2.s)


        diff = [rm_diff, pw_diff, nt_diff, sc_diff, dm_diff, c_diff, el_diff, s_diff]
        num_positive = 0
        for i in diff:
            if (i > 0):
                num_positive += 1

        print("the number of stats that are positive are: ")
        print(num_positive)

        first = None
        middle = None
        last = None
        if (num_positive > 6):
            first = "You’re making great progress! Your stats show great improvement, \
            keep smiling and being happy! Remember, the key to keeping this progress is \
            to clear your mind and keep your thoughts organized. An organized mind is a healthy mind! "
        elif (num_positive > 4):
            first = "You’re in great shape! There is a good amount of progress that keeps \
            you on the way to a healthier mind! Keep logging your thoughts and doing the \
            recommended activities for healthier thoughts. You’re doing well! "
        elif (num_positive > 2):
            first = "Slow progress is still some progress! Baby steps! Always keep in mind that\
             getting to a healthier mindset takes time and practice. It’s about changing the way \
             you think and how those thoughts affect you. "
        else:
            first = "Hmmmm, looks like there hasn’t been much progress. Don’t let this get you down - \
            there is still so much we can do! "

        if (rm_diff < 0):
            middle = "To fight rumination, identify which thoughts you repeatedly think about and plan\
             to take action. Distract yourself by watching tv, reading a book, or doing something physical. \
             Take the mistakes you have made in the past as lessons so you won’t repeat them again. \
             You are human and it is okay to make mistakes. "

        if (pw_diff < 0):
            middle += "Persistently worrying about something can take a huge toll on mental energy. Don’t worry\
             about the things you can’t control. Don’t let your irrational fears and thoughts run amuck, keep \
             yourself grounded to what you know is true. And lastly, talk to a friend or someone you trust to \
             let some of that worrying go. "

        if (nt_diff < 0):
            middle += "A lot of us have negative thoughts but not many of us take steps to combat it. \
            The first step is to recognize when you have negative thoughts and to stop the actions \
            leading up to those thoughts. Try to find the root of those negative thoughts so you can \
            understand where they are coming from and try to stop them. Most importantly, don’t let your \
            negative thoughts negatively affect your confidence! "

        if (sc_diff < 0):
            middle += "Being self critical is human nature, don’t be ashamed of it! Don’t criticize your \
            actions. If you are unhappy about something, get proactive and try to change it. Comparing \
            yourself to others is also another big no! You are unique! Remember to laugh at yourself, \
            keep your confidence up, and acknowledge your strengths. "

        if (dm_diff < 0):
            middle += "Anxiety and poor mental health often hurt your decision making abilities. \
            When making decisions, keep in mind that you don’t need to make the right choice every time. \
            Make the choice that goes more naturally to you and the one you will feel most proud of. \
            Besides, you always have tomorrow to fix your mistakes. "

        if (c_diff < 0):
            last = "Poor mental health eats at your creativity. Try doing creative activities like puzzles,\
             drawing, and writing. "
        elif (el_diff < 0):
            last = "Constantly worrying and having negative thoughts can make you exhausted. Try going \
            for a quick bike ride or doing a small workout. It will keep you energized and distracted \
            from the thoughts. "
        elif (s_diff < 0):
            last = "Sleep is so important! If you have trouble falling asleep, listen to music or \
            meditate before you sleep. Not enough sleep means not enough energy. "

        final_message = first + middle + last


        average = Stats.query.order_by(Stats.id.desc()).filter_by(user_id=userid).limit(7).all()

        overall_avg = 0
        rm_avg = 0
        pw_avg = 0
        nt_avg = 0
        sc_avg = 0
        dm_avg = 0
        c_avg = 0
        el_avg = 0
        s_avg = 0
        for i in average:
            id = i.id
            user_id = Stats.query.filter_by(id=id).first()
            overall_avg += user_id.overall
            rm_avg += user_id.rm
            pw_avg += user_id.pw
            nt_avg += user_id.nt
            sc_avg += user_id.sc
            dm_avg += user_id.dm
            c_avg += user_id.c
            el_avg += user_id.el
            s_avg += user_id.s


        return render_template('dashboard.html', name=current_user.username, overall=user.overall, rm=user.rm,\
                                pw=user.pw, nt=user.nt, sc=user.sc, dm=user.dm, c=user.c, el=user.el, s=user.s,\
                                overall_diff=overall_diff, rm_diff=rm_diff, pw_diff=pw_diff, nt_diff=nt_diff,\
                                sc_diff=sc_diff, dm_diff=dm_diff, c_diff=c_diff, el_diff=el_diff, s_diff=s_diff,\
                                overall_avg=round(overall_avg/len(average)), rm_avg=round(rm_avg/len(average)), pw_avg=round(pw_avg/len(average)),\
                                nt_avg=round(nt_avg/len(average)), sc_avg=round(sc_avg/len(average)), dm_avg=round(dm_avg/len(average)),\
                                c_avg=round(c_avg/len(average)), el_avg=round(el_avg/len(average)), s_avg=round(s_avg/len(average)), \
                                target_date=target_date, today=today, num_entries=num_entries, quiz_num=quiz_num, activity=activity, last_day=last_day, final_message=final_message)

    return render_template('dashboard.html', name=current_user.username, overall=user.overall, rm=user.rm,\
                            pw=user.pw, nt=user.nt, sc=user.sc, dm=user.dm, c=user.c, el=user.el, s=user.s,\
                            target_date=target_date, today=today, num_entries=num_entries, quiz_num=quiz_num, activity=activity, last_day=last_day)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


quiz1_questions = {
    'I tend to dwell on my problems for a long period of time and my \
    worrying only gets worse.':['1','2','3','4','5'],
    'I often find myself thinking about what could go wrong in the\
    future even if those thoughts are somewhat irrational.':['1','2','3','4','5'],
    'If I do well on an assignment, I think it is because of luck or\
    fate and not because of my own skills that contributed to the success.':['1','2','3','4','5'],
    'When you look at your friends’ social media, you feel jealous and\
    somewhat upset that your life is not as good.':['1','2','3','4','5'],
    'I often find myself dwelling on small decisions. For example, I\
    spend days trying to choose between two pairs of shoes and often\
    end up asking others for their opinion.':['1','2','3','4','5'],
    'I feel very creative and often have original thoughts.':['1','2','3','4','5'],
    'I often have “what-if” questions and make up negative\
    scenarios about the future.':['1','2','3','4','5'],
    'When something bad happens at work or school, I feel it is because\
    of my teams collective mistakes and not because of my own leadership.':['1','2','3','4','5'],
    'When given the option to either watch a movie in bed or go out for a\
    walk, I often choose the former.':['1','2','3','4','5'],
    'I either sleep too less or too much.':['1','2','3','4','5']
}

quiz2_questions = {
    'I dwell about bad things that might happen in the future.':['1','2','3','4','5'],
    'When making a major decision, I often pick the first choice to avoid\
    having to think it through.':['1','2','3','4','5'],
    'I keep replaying my anger or sadness in my mind for a very long time.':['1','2','3','4','5'],
    'You make a suggestion at work or in school but the boss or teacher does\
    not like it. You immediately feel you are bad at your job or schoolwork.':['1','2','3','4','5'],
    'I find it hard to motivate myself.':['1','2','3','4','5'],
    'I like taking part in activities that challenge my creativity.':['1','2','3','4','5'],
    'I have irrational and negative thoughts about the future. I imagine\
    scenarios in which the worst often happens.':['1','2','3','4','5'],
    'When I am not chosen for an assignment of any sort, I feel it is because\
    I am unskilled as a person overall.':['1','2','3','4','5'],
    'I believe that it is important to try even if it means I might fail \
    and embarrass myself.':['1','2','3','4','5'],
    'Embarrassing thoughts and negative thoughts often keep me up at night.':['1','2','3','4','5']
}


quiz3_questions = {
    'I feel terrible about myself when my eating gets out of control.':['1','2','3','4','5'],
    'When someone of higher authority wants to speak to me, I automatically assume\
    they want to discuss something negative.':['1','2','3','4','5'],
    'When I feel sad or angry, I keep thinking about how bad I feel.':['1','2','3','4','5'],
    'When trying to sleep, I often feel overwhelmed by negative thoughts.':['1','2','3','4','5'],
    'When making any kind of choice, I find myself thinking of everything that can go\
    wrong and that causes me to follow others’ opinions and suggestions.':['1','2','3','4','5'],
    'I often dwell on one thought or a string of the same thoughts for hours at a time.':['1','2','3','4','5'],
    'Most of the time, I feel drained and unmotivated to do anything.':['1','2','3','4','5'],
    'I like to or often participate in activities that require creativity.':['1','2','3','4','5'],
    'When something does not go right, you feel this is a temporary setback and believe\
    you can fix things.':['1','2','3','4','5'],
    'I am a perfectionist.':['1','2','3','4','5']
}


quiz4_questions = {
    'When trying to sleep, I find myself having the same negative thoughts in a kind of loop\
    that never ends.':['1','2','3','4','5'],
    'I go over embarrassing or awkward moments in my mind again and again.':['1','2','3','4','5'],
    'I find it hard to sleep and find it hard to wake up.':['1','2','3','4','5'],
    'When someone comes to you for advice on a decision, you often fail to give a decisive and\
    clear answer stating your opinion.':['1','2','3','4','5'],
    'It is unacceptable for me to make mistakes even when I am learning something new.':['1','2','3','4','5'],
    'I always worry and judge things in the present by my past experiences.':['1','2','3','4','5'],
    'I would say I usually have lots of energy.':['1','2','3','4','5'],
    'I like and often excel at drawing pictures and imagining things.':['1','2','3','4','5'],
    'Minor things and mistakes usually become a big deal for me and I worry about them excessively.':['1','2','3','4','5'],
    'It usually takes a long time for me to forgive myself.':['1','2','3','4','5']
}


quiz5_questions = {
    'If someone disagrees with you, you believe he/she doesn’t like you.':['1','2','3','4','5'],
    'After accomplishing a goal I have worked towards for a long time, I congratulate myself\
    and give the credit and respect I deserve.':['1','2','3','4','5'],
    'When making decisions, I must always choose the right one or everything will not turn out\
    how I want it.':['1','2','3','4','5'],
    'My sleep is broken due to thoughts keeping me up at night.':['1','2','3','4','5'],
    'My friends and family would describe me as a creative person.':['1','2','3','4','5'],
    'My past mistakes, embarrassments, and bad decisions run in my mind for hours at a time.':['1','2','3','4','5'],
    'While working on an assignment or project, I worry about all the things that might go wrong.\
    This can sometimes even stop me from trying my hardest.':['1','2','3','4','5'],
    'I would say that I spend at least a couple of hours a day doing something active and energetic.':['1','2','3','4','5'],
    'I find myself constantly worrying and I can feel it draining my energy.':['1','2','3','4','5'],
    'I have a tendency to blame myself for anything that goes wrong.':['1','2','3','4','5']
}



questions_one = copy.deepcopy(quiz1_questions)
questions_two = copy.deepcopy(quiz2_questions)
questions_three = copy.deepcopy(quiz3_questions)
questions_four = copy.deepcopy(quiz4_questions)
questions_five = copy.deepcopy(quiz5_questions)

@app.route('/quiz1', methods=['GET', 'POST'])
@login_required
def quiz1():
    return render_template('quiz1.html', q=questions_one)

@app.route('/quiz2', methods=['GET','POST'])
@login_required
def quiz2():
    return render_template('quiz2.html', q=questions_two)

@app.route('/quiz3', methods=['GET', 'POST'])
@login_required
def quiz3():
    return render_template('quiz3.html', q=questions_three)

@app.route('/quiz4', methods=['GET', 'POST'])
@login_required
def quiz4():
    return render_template('quiz4.html', q=questions_four)

@app.route('/quiz5', methods=['GET', 'POST'])
@login_required
def quiz5():
    return render_template('quiz5.html', q=questions_five)


@app.route('/quizresults1', methods=['POST'])
@login_required
def quizresults1():
    rm = 0
    pw = 0
    nt = 0
    sc = 0
    dm = 0
    c = 0
    el = 0
    s = 0
    overall = 0
    for i in questions_one.keys():
        answered = request.form[i]
        q_index = list(quiz1_questions.keys()).index(i)
        if (q_index==0) or (q_index==4):
            rm += int(answered)
        if (q_index==0) or (q_index==1) or (q_index==6):
            pw += int(answered)
        if (q_index==2) or (q_index==1) or (q_index==6):
            nt += int(answered)
        if (q_index==2) or (q_index==3):
            sc += int(answered)
        if (q_index==4):
            dm += int(answered)
        if (q_index==5):
            c += int(answered)
        if (q_index==8):
            if (int(answered)==1):
                el += 5
            if (int(answered)==2):
                el += 4
            if (int(answered)==3):
                el+=3
            if (int(answered)==4):
                el+=2
            if (int(answered)==5):
                el+=1
        if (q_index==9):
            if (int(answered)==1):
                s += 5
                el += 5
            if (int(answered)==2):
                s += 4
                el += 4
            if (int(answered)==3):
                s+=3
                el+=3
            if (int(answered)==4):
                s+=2
                el+=2
            if (int(answered)==5):
                s+=1
                el+=1
        if (q_index==7):
            if (int(answered)==1):
                sc += 5
                nt+=5
            if (int(answered)==2):
                sc += 4
                nt+=4
            if (int(answered)==3):
                sc+=3
                nt+=3
            if (int(answered)==4):
                sc+=2
                nt+=2
            if (int(answered)==5):
                sc+=1
                nt+=1

    rm = rm*10
    pw = round(pw*6.6)
    nt = nt*5
    sc = round(sc*6.6)
    dm = dm*20
    c = c*20
    el = el*10
    s = s*20
    overall = round((rm+pw+nt+sc+dm)/5)
    new_stat=Stats(overall=overall, rm=rm, pw=pw, nt=nt, sc=sc, dm=dm, c=c, el=el, s=s, user_id=current_user.id)
    db.session.add(new_stat)
    db.session.commit()
    return render_template('quizresults1.html', rm=rm, pw=pw, nt=nt, sc=sc, dm=dm, c=c, el=el, s=s, overall=overall)


@app.route('/quizresults2', methods=['POST'])
@login_required
def quizresults2():
    rm = 0
    pw = 0
    nt = 0
    sc = 0
    dm = 0
    c = 0
    el = 0
    s = 0
    overall = 0
    for i in questions_two.keys():
        answered = request.form[i]
        q_index = list(quiz2_questions.keys()).index(i)
        if (q_index==0) or (q_index==2) or (q_index==9):
            rm += int(answered)
        if (q_index==0) or (q_index==5):
            pw += int(answered)
        if (q_index==3) or (q_index==6) or (q_index==7):
            nt += int(answered)
        if (q_index==3) or (q_index==7):
            sc += int(answered)
        if (q_index==8):
            if (int(answered)==1):
                sc += 5
            if (int(answered)==2):
                sc += 4
            if (int(answered)==3):
                sc+=3
            if (int(answered)==4):
                sc+=2
            if (int(answered)==5):
                sc+=1
        if (q_index==1):
            dm += int(answered)
        if (q_index==5):
            c += int(answered)
        if (q_index==4) or (q_index==2):
            if (int(answered)==1):
                el += 5
            if (int(answered)==2):
                el += 4
            if (int(answered)==3):
                el+=3
            if (int(answered)==4):
                el+=2
            if (int(answered)==5):
                el+=1
        if (q_index==9):
            if (int(answered)==1):
                s += 5
            if (int(answered)==2):
                s += 4
            if (int(answered)==3):
                s+=3
            if (int(answered)==4):
                s+=2
            if (int(answered)==5):
                s+=1

    rm = round(rm*6.6)
    pw = pw*10
    nt = round(nt*6.6)
    sc = round(sc*6.6)
    dm = dm*20
    c = c*20
    el = el*10
    s = s*20
    overall = round((rm+pw+nt+sc+dm)/5)
    new_stat=Stats(overall=overall, rm=rm, pw=pw, nt=nt, sc=sc, dm=dm, c=c, el=el, s=s, user_id=current_user.id)
    db.session.add(new_stat)
    db.session.commit()
    return render_template('quizresults2.html', rm=rm, pw=pw, nt=nt, sc=sc, dm=dm, c=c, el=el, s=s, overall=overall)


@app.route('/quizresults3', methods=['POST'])
@login_required
def quizresults3():
    rm = 0
    pw = 0
    nt = 0
    sc = 0
    dm = 0
    c = 0
    el = 0
    s = 0
    overall = 0
    for i in questions_three.keys():
        answered = request.form[i]
        q_index = list(quiz3_questions.keys()).index(i)
        if (q_index==2) or (q_index==5):
            rm += int(answered)
        if (q_index==4) or (q_index==5):
            pw += int(answered)
        if (q_index==1):
            nt += int(answered)
        if (q_index==0) or (q_index==1) or (q_index==9):
            sc += int(answered)
        if (q_index==4):
            dm += int(answered)
        if (q_index==7):
            c += int(answered)
        if (q_index==6):
            if (int(answered)==1):
                s += 5
                el+=5
            if (int(answered)==2):
                s += 4
                el+=4
            if (int(answered)==3):
                s+=3
                el+=3
            if (int(answered)==4):
                s+=2
                el+=2
            if (int(answered)==5):
                s+=1
                el+=1
        if (q_index==3):
            if (int(answered)==1):
                nt += 5
                s += 5
            if (int(answered)==2):
                nt += 4
                s += 4
            if (int(answered)==3):
                nt+=3
                s+=3
            if (int(answered)==4):
                nt+=2
                s+=2
            if (int(answered)==5):
                nt+=1
                s+=1
        if (q_index==8):
            if (int(answered)==1):
                sc += 5
                nt+=5
            if (int(answered)==2):
                sc += 4
                nt+=4
            if (int(answered)==3):
                sc+=3
                nt+=3
            if (int(answered)==4):
                sc+=2
                nt+=2
            if (int(answered)==5):
                sc+=1
                nt+=1

    rm = rm*10
    pw = pw*10
    nt = round(nt*6.6)
    sc = sc*5
    dm = dm*20
    c = c*20
    el = el*20
    s = s*10
    overall = round((rm+pw+nt+sc+dm)/5)
    new_stat=Stats(overall=overall, rm=rm, pw=pw, nt=nt, sc=sc, dm=dm, c=c, el=el, s=s, user_id=current_user.id)
    db.session.add(new_stat)
    db.session.commit()
    return render_template('quizresults3.html', rm=rm, pw=pw, nt=nt, sc=sc, dm=dm, c=c, el=el, s=s, overall=overall)


@app.route('/quizresults4', methods=['POST'])
@login_required
def quizresults4():
    rm = 0
    pw = 0
    nt = 0
    sc = 0
    dm = 0
    c = 0
    el = 0
    s = 0
    overall = 0
    for i in questions_four.keys():
        answered = request.form[i]
        q_index = list(quiz4_questions.keys()).index(i)
        if (q_index==1) or (q_index==5):
            rm += int(answered)
        if (q_index==0) or (q_index==8):
            pw += int(answered)
        if (q_index==1) or (q_index==5):
            nt += int(answered)
        if (q_index==4) or (q_index==9):
            sc += int(answered)
        if (q_index==3):
            dm += int(answered)
        if (q_index==7):
            c += int(answered)
        if (q_index==6):
            el += int(answered)
        if (q_index==0) or (q_index==2):
            s += int(answered)

    rm = rm*10
    pw = pw*10
    nt = nt*10
    sc = sc*10
    dm = dm*20
    c = c*20
    el = el*20
    s = s*10
    overall = round((rm+pw+nt+sc+dm)/5)
    new_stat=Stats(overall=overall, rm=rm, pw=pw, nt=nt, sc=sc, dm=dm, c=c, el=el, s=s, user_id=current_user.id)
    db.session.add(new_stat)
    db.session.commit()
    return render_template('quizresults4.html', rm=rm, pw=pw, nt=nt, sc=sc, dm=dm, c=c, el=el, s=s, overall=overall)

@app.route('/quizresults5', methods=['POST'])
@login_required
def quizresults5():
    rm = 0
    pw = 0
    nt = 0
    sc = 0
    dm = 0
    c = 0
    el = 0
    s = 0
    overall = 0
    for i in questions_five.keys():
        answered = request.form[i]
        q_index = list(quiz5_questions.keys()).index(i)
        if (q_index==5):
            rm += int(answered)
        if (q_index==6) or (q_index==8):
            pw += int(answered)
        if (q_index==2):
            nt += int(answered)
        if (q_index==0) or (q_index==9):
            sc += int(answered)
        if (q_index==2):
            dm += int(answered)
        if (q_index==4):
            c += int(answered)
        if (q_index==8):
            el += int(answered)
        if (q_index==1):
            if (int(answered)==1):
                sc += 5
                nt+=5
            if (int(answered)==2):
                sc += 4
                nt+=4
            if (int(answered)==3):
                sc+=3
                nt+=3
            if (int(answered)==4):
                sc+=2
                nt+=2
            if (int(answered)==5):
                sc+=1
                nt+=1
        if (q_index==3):
            if (int(answered)==1):
                s += 5
                rm+=5
            if (int(answered)==2):
                s += 4
                rm+=4
            if (int(answered)==3):
                s+=3
                rm+=3
            if (int(answered)==4):
                s+=2
                rm+=2
            if (int(answered)==5):
                s+=1
                rm+=1
        if (q_index==7):
            if (int(answered)==1):
                el += 5
            if (int(answered)==2):
                el += 4
            if (int(answered)==3):
                el+=3
            if (int(answered)==4):
                el+=2
            if (int(answered)==5):
                el+=1

    print(s)
    rm = rm*10
    pw = pw*10
    nt = nt*10
    sc = round(sc*6.6)
    dm = dm*20
    c = c*20
    el = el*10
    s = s*20
    overall = round((rm+pw+nt+sc+dm)/5)
    new_stat=Stats(overall=overall, rm=rm, pw=pw, nt=nt, sc=sc, dm=dm, c=c, el=el, s=s, user_id=current_user.id)
    db.session.add(new_stat)
    db.session.commit()
    return render_template('quizresults5.html', rm=rm, pw=pw, nt=nt, sc=sc, dm=dm, c=c, el=el, s=s, overall=overall)



def my_list(database):
    l_thoughts = database.query.filter_by(user_id=current_user.id, suggestion=" ").all()
    list_thoughts = []
    for i in l_thoughts:
        date1 = str(i.created_date.date())
        date2 = str(date.today())
        if date1 == date2:
            list_thoughts.append(i)
    return list_thoughts


def my_list_control(database):
    l_thoughts = database.query.filter_by(user_id=current_user.id, suggestion=" ", control=True).all()
    list_thoughts = []
    for i in l_thoughts:
        date1 = str(i.created_date.date())
        date2 = str(date.today())
        if date1 == date2:
            list_thoughts.append(i)
    return list_thoughts


@app.route('/whatwentwrong', methods=["POST","GET"])
@login_required
def whatwentwrong():
    form = rmchangeForm()
    if request.method == "POST":
        new = rmchange(user_id=current_user.id, thought=form.thought.data, suggestion=" ", add=form.add.data)
        db.session.add(new)
        db.session.commit()
        last_thought = rmchange.query.order_by(rmchange.id.desc()).filter_by(user_id=current_user.id).first()
        add = last_thought.add
        if (add == True):
            return redirect(url_for('whatwentwrong', form=form))
        else:
            return redirect(url_for('whatwouldichange'))
    return render_template('whatwentwrong.html', form=form)


@app.route('/whatwouldichange', methods=["POST","GET"])
@login_required
def whatwouldichange():
    form = rmchangeForm()
    l = my_list(rmchange)
    thought = None
    id = None

    for i in l:
        thought = i.thought
        id = i
        break

    if request.method == "POST":
        id.suggestion = form.suggestion.data
        db.session.commit()
        l = my_list(rmchange)
        if len(l) != 0:
            for i in l:
                thought = i.thought
                id = i
                break
            return redirect(url_for('whatwouldichange', q=thought, form=form))
        else:
            return redirect(url_for('dashboard'))
    return render_template('whatwouldichange.html', q=thought, form=form)


@app.route('/rightinthepast', methods=["POST","GET"])
@login_required
def rightinthepast():
    form = rmpastForm()
    if request.method == "POST":
        new = rmpast(user_id=current_user.id, thought=form.thought.data, add=form.add.data)
        db.session.add(new)
        db.session.commit()
        last_thought = rmpast.query.order_by(rmpast.id.desc()).filter_by(user_id=current_user.id).first()
        add = last_thought.add
        if (add == True):
            return redirect(url_for('rightinthepast', form=form))
        else:
            return redirect(url_for('dashboard'))
    return render_template('rightinthepast.html', form=form)


@app.route('/doihavecontrol', methods=["POST","GET"])
@login_required
def doihavecontrol():
    form = pwcontrolForm()
    if request.method == 'POST':
        new_pw = pwcontrol(user_id=current_user.id, thought=form.thought.data, suggestion=" ", \
        add=form.add.data, control=form.control.data)
        db.session.add(new_pw)
        db.session.commit()
        last_thought = pwcontrol.query.order_by(pwcontrol.id.desc()).filter_by(user_id=current_user.id).first()
        add = last_thought.add
        control = last_thought.control
        if (add == True and control == True):
            return redirect(url_for('doihavecontrol', form=form))
        elif (add == True and control == False):
            return redirect(url_for('doihavecontrol', form=form))
        else:
            return redirect(url_for('whatcanido'))
    return render_template('doihavecontrol.html', form=form)


@app.route('/whatcanido', methods=["POST","GET"])
@login_required
def whatcanido():
    l = my_list_control(pwcontrol)
    form = pwcontrolForm()
    thought = None
    id = None

    for i in l:
        thought = i.thought
        id = i
        break

    if request.method == "POST":
        id.suggestion = form.suggestion.data
        db.session.commit()
        l = my_list_control(pwcontrol)
        if len(l) != 0:
            for i in l:
                thought = i.thought
                id = i
                break
            return redirect(url_for('whatcanido', q=thought, form=form))
        else:
            return redirect(url_for('dashboard'))
    return render_template('whatcanido.html', q=thought, form=form)


@app.route('/howlikelytohappen', methods=["POST","GET"])
@login_required
def howlikelytohappen():
    form = pwevidenceForm()
    if request.method == 'POST':
        new_pw = pwevidence(user_id=current_user.id, thought=form.thought.data, suggestion=" ", \
        add=form.add.data, control=form.control.data)
        db.session.add(new_pw)
        db.session.commit()
        last_thought = pwevidence.query.order_by(pwevidence.id.desc()).filter_by(user_id=current_user.id).first()
        add = last_thought.add
        control = last_thought.control
        if (add == True and control == True):
            return redirect(url_for('howlikelytohappen', form=form))
        elif (add == True and control == False):
            return redirect(url_for('howlikelytohappen', form=form))
        else:
            return redirect(url_for('evidence'))
    return render_template('howlikelytohappen.html', form=form)


@app.route('/evidence', methods=["POST","GET"])
@login_required
def evidence():
    form = pwevidenceForm()
    l = my_list_control(pwevidence)
    thought = None
    id = None

    for i in l:
        thought = i.thought
        id = i
        break

    if request.method == "POST":
        id.suggestion = form.suggestion.data
        db.session.commit()
        l = my_list_control(pwevidence)
        if len(l) != 0:
            for i in l:
                thought = i.thought
                id = i
                break
            return redirect(url_for('evidence', q=thought, form=form))
        else:
            return redirect(url_for('dashboard'))
    return render_template('evidence.html', q=thought, form=form)


@app.route('/isittrue', methods=["POST","GET"])
@login_required
def isittrue():
    form = nttrueForm()
    if request.method == 'POST':
        new_nt = nttrue(user_id=current_user.id, thought=form.thought.data, suggestion=" ", \
        add=form.add.data, control=form.control.data)
        db.session.add(new_nt)
        db.session.commit()
        last_thought = nttrue.query.order_by(nttrue.id.desc()).filter_by(user_id=current_user.id).first()
        add = last_thought.add
        control = last_thought.control
        if (add == True and control == True):
            return redirect(url_for('isittrue', form=form))
        elif (add == True and control == False):
            return redirect(url_for('isittrue', form=form))
        else:
            return redirect(url_for('whyisittrue'))
    return render_template('isittrue.html', form=form)


@app.route('/whyisittrue', methods=["POST","GET"])
@login_required
def whyisittrue():
    l = my_list_control(nttrue)
    form = nttrueForm()
    thought = None
    id = None

    for i in l:
        thought = i.thought
        id = i
        break

    if request.method == "POST":
        id.suggestion = form.suggestion.data
        db.session.commit()
        l = my_list_control(nttrue)
        if len(l) != 0:
            for i in l:
                thought = i.thought
                id = i
                break
            return redirect(url_for('whyisittrue', q=thought, form=form))
        else:
            return redirect(url_for('dashboard'))
    return render_template('whyisittrue.html', q=thought, form=form)


@app.route('/negativethoughts', methods=["POST","GET"])
@login_required
def negativethoughts():
    form = ntpositiveForm()
    if request.method == "POST":
        new = ntpositive(user_id=current_user.id, thought=form.thought.data, suggestion=" ", add=form.add.data)
        db.session.add(new)
        db.session.commit()
        last_thought = ntpositive.query.order_by(ntpositive.id.desc()).filter_by(user_id=current_user.id).first()
        add = last_thought.add
        if (add == True):
            return redirect(url_for('negativethoughts', form=form))
        else:
            return redirect(url_for('positivespin'))
    return render_template('negativethoughts.html', form=form)


@app.route('/positivespin', methods=["POST","GET"])
@login_required
def positivespin():
    form = ntpositiveForm()
    l = my_list(ntpositive)
    thought = None
    id = None

    for i in l:
        thought = i.thought
        id = i
        break

    if request.method == "POST":
        id.suggestion = form.suggestion.data
        db.session.commit()

        l = my_list(ntpositive)
        if len(l) != 0:
            for i in l:
                thought = i.thought
                id = i
                break
            return redirect(url_for('positivespin', q=thought, form=form))
        else:
            return redirect(url_for('dashboard'))
    return render_template('positivespin.html', q=thought, form=form)


@app.route('/goodqualities', methods=["POST","GET"])
@login_required
def goodqualities():
    form = scgoodForm()
    if request.method == "POST":
        new = scgood(user_id=current_user.id, thought=form.thought.data, add=form.add.data)
        db.session.add(new)
        db.session.commit()
        last_thought = scgood.query.order_by(scgood.id.desc()).filter_by(user_id=current_user.id).first()
        add = last_thought.add
        if (add == True):
            return redirect(url_for('goodqualities', form=form))
        else:
            return redirect(url_for('dashboard'))
    return render_template('goodqualities.html', form=form)


@app.route('/selfcriticism', methods=["POST","GET"])
@login_required
def selfcriticism():
    form = screwordForm()
    if request.method == "POST":
        new = screword(user_id=current_user.id, thought=form.thought.data, suggestion=" ", add=form.add.data)
        db.session.add(new)
        db.session.commit()
        last_thought = screword.query.order_by(screword.id.desc()).filter_by(user_id=current_user.id).first()
        add = last_thought.add
        if (add == True):
            return redirect(url_for('selfcriticism', form=form))
        else:
            return redirect(url_for('reword'))
    return render_template('selfcriticism.html', form=form)


@app.route('/reword', methods=["POST","GET"])
@login_required
def reword():
    form = screwordForm()
    l = my_list(screword)
    thought = None
    id = None

    for i in l:
        thought = i.thought
        id = i
        break

    if request.method == "POST":
        id.suggestion = form.suggestion.data
        db.session.commit()

        l = my_list(screword)
        if len(l) != 0:
            for i in l:
                thought = i.thought
                id = i
                break
            return redirect(url_for('reword', q=thought, form=form))
        else:
            return redirect(url_for('dashboard'))
    return render_template('reword.html', q=thought, form=form)


@app.route('/canichangeit', methods=["POST","GET"])
@login_required
def canichangeit():
    form = scchangeForm()
    if request.method == 'POST':
        new_pw = scchange(user_id=current_user.id, thought=form.thought.data, suggestion=" ", \
        add=form.add.data, control=form.control.data)
        db.session.add(new_pw)
        db.session.commit()
        last_thought = scchange.query.order_by(scchange.id.desc()).filter_by(user_id=current_user.id).first()
        add = last_thought.add
        control = last_thought.control
        if (add == True and control == True):
            return redirect(url_for('canichangeit', form=form))
        elif (add == True and control == False):
            return redirect(url_for('canichangeit', form=form))
        else:
            return redirect(url_for('howcanichangeit'))
    return render_template('canichangeit.html', form=form)


@app.route('/howcanichangeit', methods=["POST","GET"])
@login_required
def howcanichangeit():
    l = my_list_control(scchange)
    form = scchangeForm()
    thought = None
    id = None

    for i in l:
        thought = i.thought
        id = i
        break

    if request.method == "POST":
        id.suggestion = form.suggestion.data
        db.session.commit()

        l = my_list_control(scchange)
        if len(l) != 0:
            for i in l:
                thought = i.thought
                id = i
                break
            return redirect(url_for('howcanichangeit', q=thought, form=form))
        else:
            return redirect(url_for('dashboard'))
    return render_template('howcanichangeit.html', q=thought, form=form)


@app.route('/decisions', methods=["POST","GET"])
@login_required
def decisions():
    form = dmworstForm()
    if request.method == "POST":
        new = dmworst(user_id=current_user.id, thought=form.thought.data, suggestion=" ", add=form.add.data)
        db.session.add(new)
        db.session.commit()
        last_thought = dmworst.query.order_by(dmworst.id.desc()).filter_by(user_id=current_user.id).first()
        add = last_thought.add
        if (add == True):
            return redirect(url_for('decisions', form=form))
        else:
            return redirect(url_for('worstthatcanhappen'))
    return render_template('decisions.html', form=form)


@app.route('/worstthatcanhappen', methods=["POST","GET"])
@login_required
def worstthatcanhappen():
    form = dmworstForm()
    l = my_list(dmworst)
    thought = None
    id = None

    for i in l:
        thought = i.thought
        id = i
        break

    if request.method == "POST":
        id.suggestion = form.suggestion.data
        db.session.commit()
        l = my_list(dmworst)
        if len(l) != 0:
            for i in l:
                thought = i.thought
                id = i
                break
            return redirect(url_for('worstthatcanhappen', q=thought, form=form))
        else:
            return redirect(url_for('dashboard'))
    return render_template('worstthatcanhappen.html', q=thought, form=form)


@app.route('/canihelpnow', methods=["POST","GET"])
@login_required
def canihelpnow():
    form = dmnowForm()
    if request.method == "POST":
        new = dmnow(user_id=current_user.id, thought=form.thought.data, suggestion=" ", add=form.add.data)
        db.session.add(new)
        db.session.commit()
        last_thought = dmnow.query.order_by(dmnow.id.desc()).filter_by(user_id=current_user.id).first()
        add = last_thought.add
        if (add == True):
            return redirect(url_for('canihelpnow', form=form))
        else:
            return redirect(url_for('howcanihelp'))
    return render_template('canihelpnow.html', form=form)


@app.route('/howcanihelp', methods=["POST","GET"])
@login_required
def howcanihelp():
    form = dmnowForm()
    l = my_list(dmnow)
    thought = None
    id = None

    for i in l:
        thought = i.thought
        id = i
        break

    if request.method == "POST":
        id.suggestion = form.suggestion.data
        db.session.commit()
        l = my_list(dmnow)
        if len(l) != 0:
            for i in l:
                thought = i.thought
                id = i
                break
            return redirect(url_for('howcanihelp', q=thought, form=form))
        else:
            return redirect(url_for('dashboard'))
    return render_template('howcanihelp.html', q=thought, form=form)


if __name__ == '__main__':
    app.run(debug=True)
