from flask import Flask, render_template, url_for, redirect, flash, request, session
import config
from forms import add_plant_form, add_picture_form, edit_form
from database import db_session
from models import Plants, Pictures
from sqlalchemy import asc, func, desc, update
from flask_table import Table, Col
import os
from werkzeug.utils import secure_filename
from flask import send_from_directory

#sets upload folder and what picture files are allowed
UPLOAD_FOLDER = "./static/pictures"
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__)
app.debug = True
app.config.from_object(config)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#sets upload folder and what picture files are allowed
UPLOAD_FOLDER = "./static/pictures"
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])


#sets upload folder and what picture files are allowed
#UPLOAD_FOLDER = "./static/pictures"
#ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

#index
@app.route('/')
def index():
    return render_template('index.jinja')
 
 
# plants page. Shows all plants in database 
@app.route("/plants")
def plants():
    data = Plants.query.all()
    pictures = Pictures.query.all()
    return render_template('plants.jinja', data=data, pictures=pictures)

# form for adding plants. later going to be possible in admin mode only
@app.route("/add_plant", methods=["GET", "POST"])
def add_plant():
    form = add_plant_form()
    if form.validate_on_submit():
        print ("duh")
        try:
            new_plant = Plants(name=form.name.data, german_name=form.german_name.data, latin_name=form.latin_name.data, plant_information=form.plant_information.data, light=form.light.data, watering=form.watering.data, placement=form.placement.data, insect_friendly=form.insect_friendly.data, other_information=form.other_information.data)
            db_session.add(new_plant)
            db_session.commit()
            print ("New plant added")
            return redirect(url_for('plants'))
        except:
            flash('plant could not be added')
            print ("could not be added. Error!")
    return render_template ('add_plant.jinja', form=form)
    
    
#shows the latest added plant
@app.route("/newest_plant", methods=["GET"])
def newest_plant():
    newest = db_session.query(Plants).filter(Plants.id == db_session.query(func.max(Plants.id)))
    return render_template ('newest_plant.jinja', newest=newest)

# checks for allowed files for the picture upload
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


#picture upload
@app.route("/upload_picture/<id>", methods=["GET", "POST"])
def upload_picture(id):
    picture_add = db_session.query(Plants).filter(Plants.id == id)
    
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            print (filename)
            for item in picture_add:
                id_plant = item.id
                print (id_plant)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            add_picture = Pictures(plant_id=id_plant, picturepath=filename)
            db_session.add(add_picture)
            db_session.commit()
            return redirect(url_for('plants', filename=filename))
    return render_template ('upload_picture.jinja', picture_add=picture_add)    


#admin function for an overview and the option to edit data 
@app.route("/plants_admin", methods=["GET", "POST"])      
def plants_admin():
    data = Plants.query.all()
    pictures = Pictures.query.all()
    return render_template('plants_admin.jinja', data=data, pictures=pictures)
 
 #edit data on pre-popluated form
@app.route("/edit/<id>", methods=["GET", "POST"])
def edit(id):
    plant_edit = Plants.query.filter_by(id=id).first()
    form = edit_form(obj=plant_edit)
    if form.validate_on_submit():
        form.populate_obj(plant_edit)
        edited_plant = Plants(name=form.name.data, german_name=form.german_name.data, latin_name=form.latin_name.data, plant_information=form.plant_information.data, light=form.light.data, watering=form.watering.data, placement=form.placement.data, insect_friendly=form.insect_friendly.data, other_information=form.other_information.data)
        try:
            db_session.add(plant_edit)
            db_session.commit()
            print ("plant edited")
            return redirect(url_for('plants'))
        except:
            print ("error")
            return redirect(url_for('plants'))
    return render_template('edit.jinja', form=form, plant_edit=plant_edit)


# call main
if __name__ == "__main__":
    app.run()