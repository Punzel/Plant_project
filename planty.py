from flask import Flask, render_template, url_for, redirect, flash, request, session
import config
from forms import add_plant_form
from database import db_session
from models import Plants
from sqlalchemy import asc, func, desc
from flask_table import Table, Col

app = Flask(__name__)
app.debug = True
app.config.from_object(config)


@app.route('/')
def index():
    return render_template('index.jinja')
    
@app.route("/plants")
def plants():
    data = Plants.query.all()
#    print newest
    return render_template('plants.jinja', data=data)
    
@app.route("/add_plant", methods=["GET", "POST"])
def add_plant():
    form = add_plant_form()
    if form.validate_on_submit():
        print "duh"
        try:
            new_plant = Plants(name=form.name.data, german_name=form.german_name.data, latin_name=form.latin_name.data, plant_information=form.plant_information.data, light=form.light.data, watering=form.watering.data, placement=form.placement.data, insect_friendly=form.insect_friendly.data, other_information=form.other_information.data)
            db_session.add(new_plant)
            db_session.commit()
            print "New plant added"
            return redirect(url_for('plants'))
        except:
            flash('plant could not be added')
            print "could not be added. Error!"
    return render_template ('add_plant.jinja', form=form)
 
@app.route("/newest_plant", methods=["GET"])
def newest_plant():
    newest = db_session.query(Plants).filter(Plants.id == db_session.query(func.max(Plants.id)))
    return render_template ('newest_plant.jinja', newest=newest)

''' 
def user_add():
    form = NewUserForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data, password=make_hash(form.password.data), active=form.active.data)
        if new_user:
            db_session.add(new_user)
            db_session.commit()
            flash('Neuer Nutzer erfolgreich angelegt!')
            return redirect(url_for('logged_in'))
        else:
            flash('Neuer Nutzer konnte nicht angelegt werden!')
    return render_template('user_add.jinja', form=form)
    '''

if __name__ == "__main__":
    app.run()