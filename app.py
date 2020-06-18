from flask import Flask, render_template, redirect, url_for, request
from flask_wtf import FlaskForm
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

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
Bootstrap(app)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
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
    remember = BooleanField('remember me')

class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
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
        return redirect(url_for('quiz'))
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
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('dashboard'))
        return "invalid username or password"
    return render_template('login.html', form=form)


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
            dict[i] = list
        elif (i==date_rmpast):
            list = list_entries(rmpast,i)
            dict[i] = list
        elif (i==date_pwcontrol):
            list = list_entries(pwcontrol,i)
            dict[i] = list
        elif (i==date_pwevidence):
            list = list_entries(pwevidence,i)
            dict[i] = list
        elif (i==date_nttrue):
            list = list_entries(nttrue,i)
            dict[i] = list
        elif (i==date_ntpositive):
            list = list_entries(ntpositive,i)
            dict[i] = list
        elif (i==date_scgood):
            list = list_entries(scgood,i)
            dict[i] = list
        elif (i==date_screword):
            list = list_entries(screword,i)
            dict[i] = list
        elif (i==date_scchange):
            list = list_entries(scchange,i)
            dict[i] = list
        elif (i==date_dmworst):
            list = list_entries(dmworst,i)
            dict[i] = list
        elif (i==date_dmnow):
            list = list_entries(dmnow,i)
            dict[i] = list

    print(dict)

    return render_template('records.html', q=dict)


@app.route('/dashboard')
@login_required
def dashboard():
    userid = current_user.id
    user = Stats.query.order_by(Stats.id.desc()).filter_by(user_id=userid).first()

    new_day = datetime.timedelta(days=1)
    latest_date = user.created_date
    target = new_day + latest_date
    today = date.today()
    target_date = target.date()
    str_today = str(today)
    str_target = str(target_date)

    q_entries = Stats.query.filter_by(user_id=userid).all()
    num_entries = len(q_entries)
    print(num_entries)
    if (num_entries > 1):
        difference = Stats.query.order_by(Stats.id.desc()).filter_by(user_id=userid).limit(2).all()

        id1 = difference[1].id
        id2 = difference[0].id

        user_id1 = Stats.query.filter_by(id=id1).first()
        user_id2 = Stats.query.filter_by(id=id2).first()

        overall_diff = user_id1.overall - user_id2.overall
        rm_diff = user_id1.rm - user_id2.rm
        pw_diff = user_id1.pw - user_id2.pw
        nt_diff = user_id1.nt - user_id2.nt
        sc_diff = user_id1.sc - user_id2.sc
        dm_diff = user_id1.dm - user_id2.dm
        c_diff = user_id1.c - user_id2.c
        el_diff = user_id1.el - user_id2.el
        s_diff = user_id1.s - user_id2.s

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
                                    overall_avg=overall_avg/len(average), rm_avg=rm_avg/len(average), pw_avg=pw_avg/len(average),\
                                    nt_avg=nt_avg/len(average), sc_avg=sc_avg/len(average), dm_avg=dm_avg/len(average),\
                                    c_avg=c_avg/len(average), el_avg=el_avg/len(average), s_avg=s_avg/len(average), \
                                    target_date=target_date, today=today, num_entries=num_entries)

    return render_template('dashboard.html', name=current_user.username, overall=user.overall, rm=user.rm,\
                            pw=user.pw, nt=user.nt, sc=user.sc, dm=user.dm, c=user.c, el=user.el, s=user.s,\
                            target_date=target_date, today=today, num_entries=num_entries)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


original_questions = {
    'I tend to dwell on my problems for a long period of time\
    and my worrying only gets worse.':['1', '2', '3', '4', '5'],
    'I often find myself thinking about what could go wrong in \
    the future even if those thoughts are somewhat irrational.':['1', '2', '3', '4', '5'],
    'If I do well on an assignment, I think it is because of luck \
    or fate and not because of my own skills that contributed to the \
    success.':['1', '2', '3', '4', '5'],
    'When you look at your friends social media, you feel jealous \
    and somewhat upset that your life is not as good.':['1', '2', '3', '4', '5'],
    'I often find myself dwelling on small decisions. For example, \
    I spend days trying to choose between two pairs of shoes and often \
    end up asking others for their opinion.':['1', '2', '3', '4', '5'],
    'I feel very creative and often have original thoughts.':['1', '2', '3', '4', '5'],
    'Most of the time, I feel drained and unmotivated to do anything.':['1', '2', '3', '4', '5'],
    'When trying to sleep, I find myself having the same negative thoughts \
    in a kind of loop that never ends.':['1', '2', '3', '4', '5'],
    'I go over embarrassing or awkward moments in my mind again and again.':['1', '2', '3', '4', '5'],
    'I often have “what-if” questions and make up negative scenarios about \
    the future.':['1', '2', '3', '4', '5'],
    'When something bad happens at work or school, I feel it is because of my \
    teams collective mistakes and not because of my own leadership.':['1', '2', '3', '4', '5'],
    'It is unacceptable for me to make mistakes even when I am learning \
    something new.':['1', '2', '3', '4', '5'],
    'When making any kind of choice, I find myself thinking of everything that \
    can go wrong and that causes me to follow others’ opinions and suggestions.':['1', '2', '3', '4', '5'],
    'When given the option to either watch a movie in bed or go out for a walk, \
    I often choose the former.':['1', '2', '3', '4', '5'],
    'I either sleep too less or too much.':['1', '2', '3', '4', '5'],
}


questions = copy.deepcopy(original_questions)

@app.route('/quiz', methods=['GET', 'POST'])
@login_required
def quiz():
    return render_template('quiz.html', q = questions)


@app.route('/quizresults', methods=['POST'])
@login_required
def quiz_results():
    rm = 0
    pw = 0
    nt = 0
    sc = 0
    dm = 0
    c = 0
    el = 0
    s = 0
    overall = 0
    for i in questions.keys():
        answered = request.form[i]
        q_index = list(original_questions.keys()).index(i)
        if (q_index==0) or (q_index==8):
            rm += int(answered)
        if (q_index==1) or (q_index==9):
            pw += int(answered)
        if (q_index==1) or (q_index==2) or (q_index==9) or (q_index==10):
            nt += int(answered)
        if (q_index==2) or (q_index==3) or (q_index==10) or (q_index==11):
            sc += int(answered)
        if (q_index==4) or (q_index==12):
            dm += int(answered)
        if (q_index==5):
            c += int(answered)
        if (q_index==6) or (q_index==13):
            el += int(answered)
        if (q_index==6) or (q_index==7) or (q_index==14):
            s += int(answered)

    rm = rm/10*100
    pw = pw/10*100
    nt = nt/20*100
    sc = sc/20*100
    dm = dm/10*100
    c = c/5*100
    el = el/10*100
    s = s/15*100
    overall = (rm+pw+nt+sc+dm)/5
    new_stat=Stats(overall=overall, rm=rm, pw=pw, nt=nt, sc=sc, dm=dm, c=c, el=el, s=s, user_id=current_user.id)
    db.session.add(new_stat)
    db.session.commit()
    return render_template('quizresults.html', rm=rm, pw=pw, nt=nt, sc=sc, dm=dm, c=c, el=el, s=s, overall=overall)


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
