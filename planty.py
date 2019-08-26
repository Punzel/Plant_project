from flask import Flask, render_template, url_for, redirect, flash, request, session
import config
from forms import add_plant_form, add_picture_form, edit_form
from database import db_session
from models import Plants, Pictures
from sqlalchemy import asc, func, desc
from flask_table import Table, Col
import os
from werkzeug.utils import secure_filename
from flask import send_from_directory

UPLOAD_FOLDER = "./static"
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__)
app.debug = True
app.config.from_object(config)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#sets upload folder and what picture files are allowed
UPLOAD_FOLDER = "./static"
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

#index
@app.route('/')
def index():
    return render_template('index.jinja')
 
 
# plants page. Shows all plants in database 
@app.route("/plants")
def plants():
    data = Plants.query.all()
    return render_template('plants.jinja', data=data)

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
    plant_edit = db_session.query(Plants).filter(Plants.id == id)
    form = edit_form()
    pre_poplate = []
    for item in plant_edit:
        print (item.name)     
    #this populates the form
    if request.method == 'GET':
        for item in plant_edit:
            form.name.data = item.name
            form.german_name.data = item.german_name
            form.latin_name.data = item.latin_name
            form.plant_information.data = item.plant_information
            form.light.data = item.light
            form.watering.data = item.watering
            form.placement.data = item.placement
            form.insect_friendly.data = item.insect_friendly
            form.other_information.data = item.other_information

    return render_template ('edit.jinja', plant_edit=plant_edit, form=form) 


    
'''
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

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
# call main
if __name__ == "__main__":
    app.run()