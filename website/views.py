from io import BytesIO

from flask import Blueprint, render_template, request, flash, jsonify, send_file
from flask_login import login_required, current_user
from .models import Note, Resume, Upload
from . import db
import json
from .generatecoverletter import export
from .coverletter import fill_invatiation
views = Blueprint('views',__name__)


@views.route('/')
def defaultpath():
    return render_template("about.html", user=current_user)


@views.route('/home')
@login_required
def home():
    return render_template("home.html", user=current_user)

@views.route('/about')
def about():
    return render_template("about.html", user=current_user)





@views.route('/notes', methods=['GET', 'POST'])
@login_required
def notes():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('note is too short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added', category='success')
    return render_template("notes.html", user=current_user)

@views.route('/account', methods=['GET', 'POST'])
@login_required
def resume():
    resumecheck = Resume.query.filter_by(user_id=current_user.id).first()
    if resumecheck:
        isbutton = False
    else:
        isbutton = True
    print(isbutton)
    if request.method == 'POST':
        resume = request.form.get('resume')
        if len(resume) < 10:
            flash('resume is too short!', category='error')
    
        else:
            new_resume = Resume(data=resume, user_id=current_user.id)
            db.session.add( new_resume )
            db.session.commit()
            flash('Resume added!', category='success')
            isbutton = False

    
    upload2 = Upload.query.filter_by(user_id=current_user.id).first()
    print(upload2)
    if upload2:
        filename = upload2.filename
    else:
        filename = ""
    
    return render_template("account.html", user=current_user, filename=filename,isbutton=isbutton)

@views.route('/coverletter', methods=['GET', 'POST'])
@login_required
def create_letter():
    
    if request.method == 'POST':
        jobdescription = request.form.get('coverletter')
        Date = request.form.get('Date')
        Company = request.form.get('Company')
        Location = request.form.get('Location')
        City = request.form.get('City')
        JobTitle = request.form.get('Jobtitle')
        if len(jobdescription) < 10:
            flash('job Description is too short!', category='error')
    
        else:
        
            resume = Resume.query.filter_by(user_id=current_user.id).first()
            upload = Upload.query.filter_by(user_id=current_user.id).first()
            if resume and upload:
                generatedtext = export(resume.data,jobdescription)
    
                coverletter = BytesIO(upload.data)
                with open("output.docx", "wb") as f:
                    f.write(coverletter.getbuffer())
                
                fill_invatiation(Date,Company,Location,City,JobTitle,generatedtext)
                
                return send_file('output2.docx', download_name="YourNewCoverLetter.docx", as_attachment=True)
                pass
                
            else:
                flash('You have not submitted a Resume or Coverletter yet, Please go to Account to upload one', category='error')

            
            
            
            

    
    return render_template("coverletter.html", user=current_user)

@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})

@views.route('/delete-resume', methods=['POST'])
def delete_resume():
    resume = json.loads(request.data)
    resumeId = resume['resumeId']
    resume = Resume.query.get(resumeId)
    if resume:
        if resume.user_id == current_user.id:
            db.session.delete(resume)
            db.session.commit()

    return jsonify({})


@views.route('/template', methods=['GET','POST'])
@login_required
def template():
    
    upload2 = Upload.query.filter_by(user_id=current_user.id).first()
    if upload2:
        filename = upload2.filename
        isuploaded = True
    else:
        isuploaded = False
        filename = ""
    if request.method == 'POST':
        
        if 'file' not in request.files:
            flash('error', category='error')
        file = request.files['file']
        if file.filename =='':
            flash('error no file', category='error')
        
        upload = Upload.query.filter_by(user_id=current_user.id).first()
        if upload:
            flash('file already uploaded', category='error')
            return render_template("account.html", user=current_user, filename=filename,isuploaded=isuploaded)
        else:
            if file:
                checkfile = file.filename.split(".")
                if checkfile[1] != 'docx':
                    flash('file not supported', category='error')
                    
                else:
                    filename=file.filename
                    upload = Upload(filename=filename, data=file.read(),user_id=current_user.id)
                    db.session.add(upload)
                    db.session.commit()

                    flash(f'Sucessfully Uploaded {file.filename}', category="success")
                    
            
    return render_template("account.html", user=current_user, filename=filename, isuploaded=isuploaded,)
        
        
@views.route('/remove-template', methods=['GET','POST'])
@login_required
def remove_template():
    if request.method == "POST":
        upload = Upload.query.filter_by(user_id=current_user.id).first()
        if upload:
            db.session.delete(upload)
            db.session.commit()
    return render_template("account.html", user=current_user, filename="",isuploaded=False,)

    
    